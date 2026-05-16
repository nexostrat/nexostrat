# Plan 01b — Mirrors + warm-standby

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **For humans:** plain-language partner (`-explicado.md`) deferred to execution-start.

**Goal:** Stand up the off-site git mirror network (GitHub + Codeberg) via host-side systemd path-watchers, provision the warm-standby clone, and verify the warm-rsync timer actually works end-to-end. After 01b, a single-machine failure recovers in 15-30 min and an off-site loss costs nothing.

**Architecture:** Two parallel concerns —
1. **Mirror replication** is event-driven via systemd `.path` units that watch Gitea's bare repo `refs/heads/main` and fire a `.service` unit (running as `ricardo`, the user with the age key) that runs `git push` to GitHub then Codeberg. Replaces the original Plan-01 design of an in-Gitea `post-receive` hook (C4 fix: that hook can't decrypt secrets).
2. **Warm-standby** is a second Linux Mint machine receiving nightly rsync from the HP server (per spec §3 backup ladder). Services are pulled but stopped at rest; failover is `docker-compose up` + DNS swap.

**Tech Stack:** systemd 248+ (`.path` units, `.timer` units, `OnCalendar=` with TZ), bash, git, rsync, age (for PAT decryption), Docker (for image pre-pull on standby), Tailscale (for cross-host SSH).

**Plan-level success criteria:**
- A test commit on HP origin appears on GitHub `nexostrat/nexostrat` within 60s of `git push origin main`.
- Same commit appears on Codeberg `nexostrat/nexostrat` within 60s.
- `systemctl status nexostrat-warm-rsync.service` after manual trigger returns `status=0/SUCCESS` with file-transferred count > 0.
- HP-down failover runbook dry-run completes in <30 min and the standby boots services cleanly.
- Repo tagged `v0.1b-mirrors`.

**Coordination gates:**
- **GitHub + Codeberg accounts** must exist as `nexostrat` org/user with SSH keys registered (terrain-prep work — VERIFY at pre-flight). PATs (`GITHUB_MIRROR_PAT`, `CODEBERG_MIRROR_PAT`) get added to `secrets.env.age` during this plan.
- **Warm-standby host** must be physically available + have Linux Mint installed + Tailscale joined to the tailnet. If not yet provisioned, Tasks 7-12 (warm-standby cluster) pause until the host is ready; Tasks 1-6 (mirror cluster) run unblocked.

**Spec references:** §1 (Replication topology), §3 (Backup ladder + recovery procedures), §5 (Per-machine profiles — `hp-standby.yaml` filled out at provisioning), §9.4 (Python agents — note: mirror agents live in `infra/systemd/`, not Python, per ADR-029 + C4). ADRs 002, 006, 023, 029.

**Audit-finding inheritance:** This plan resolves C4 (Gitea hook can't decrypt — replace with host-side path-watcher), F7 (Codeberg mirror), F22-subset (Gitea bare-repo on-disk path verification — n8n verification dropped per "drop n8n entirely"), F24 (warm-rsync false-positive smoke test — replace with `systemctl start && grep status=0/SUCCESS`), F25 (Gitea repo at org `nexostrat`).

---

## File Structure

**Created in this plan:**

```
/srv/Nexostrat/
├─ infra/
│   ├─ systemd/                                                     (populated this plan)
│   │   ├─ nexostrat-mirror-github.path
│   │   ├─ nexostrat-mirror-github.service
│   │   ├─ nexostrat-mirror-codeberg.path
│   │   ├─ nexostrat-mirror-codeberg.service
│   │   ├─ nexostrat-warm-rsync.timer
│   │   └─ nexostrat-warm-rsync.service
│   ├─ scripts/
│   │   ├─ mirror-push.sh                                           (called by mirror .service units)
│   │   ├─ warm-rsync.sh                                            (called by warm-rsync .service)
│   │   └─ install-systemd-units.sh                                 (host-side installer)
│   └─ machines/
│       └─ hp-standby.yaml                                          (MODIFIED — placeholders filled at provisioning)
│
├─ secrets.env.age                                                  (MODIFIED — adds GITHUB_MIRROR_PAT + CODEBERG_MIRROR_PAT)
├─ infra/secrets/MANIFEST.md                                        (MODIFIED — Last rotated dates filled)
│
├─ 00_GOVERNANCE/
│   └─ system_map.md                                                (CREATED — Gitea path + mirror units + standby info)
│
└─ docs/runbooks/
    └─ hp_down.md                                                   (CREATED — failover procedure)
```

---

## Pre-flight checks (before Task 1)

- [ ] **Confirm Plan 01a tag exists**

```bash
git tag | grep v0.1a-foundation
# Expected: v0.1a-foundation
```

If missing, Plan 01a is not done — STOP and complete 01a first.

- [ ] **Confirm Gitea origin still pushing**

```bash
git push origin main
# Expected: "Everything up-to-date"
```

- [ ] **Confirm GitHub `nexostrat/nexostrat` repo exists**

Use the GitHub web UI or `gh repo view nexostrat/nexostrat` (if `gh` CLI is authenticated). If it doesn't exist:
- Create org `nexostrat` (if not exists) — Ricardo's manual step via github.com/organizations/new.
- Create empty private repo `nexostrat/nexostrat` — `gh repo create nexostrat/nexostrat --private --description "Nexostrat — AI consulting firm"`.

- [ ] **Confirm Codeberg `nexostrat/nexostrat` repo exists**

Same posture for Codeberg (codeberg.org). Manual UI step if needed; Codeberg has no first-party CLI.

- [ ] **Confirm SSH keys are registered at both providers**

```bash
ssh -T git@github.com
# Expected: "Hi nexostrat! You've successfully authenticated..."

ssh -T git@codeberg.org
# Expected: "Hi there, nexostrat! You've successfully authenticated..."
```

If either fails, register the SSH pubkey at the respective provider (terrain prep should have done this — verify it's still there).

- [ ] **Confirm `systemctl --user` works for ricardo (or systemd is system-wide)**

This plan installs unit files at the **system level** (`/etc/systemd/system/`) because the mirror push runs as `ricardo` but is triggered by Gitea's bare-repo path which lives in a Docker volume root-readable. System-level units with `User=ricardo` is the cleanest pattern.

```bash
systemctl --version | head -1
# Expected: systemd 248 or later (TZ-aware OnCalendar requires 248+)

sudo systemctl status
# Expected: clean exit; we'll need sudo for unit install
```

- [ ] **Confirm `rsync` is installed on HP**

```bash
rsync --version | head -1
# Expected: rsync version
```

- [ ] **Confirm Tailscale is up**

```bash
tailscale status | head -5
# Expected: tailnet info; HP shows as 100.64.121.80
```

---

## Task 1: Verify Gitea bare-repo on-disk path + draft `00_GOVERNANCE/system_map.md` (F22, F25)

**Goal:** Confirm where Gitea actually stores the bare repo for `nexostrat/nexostrat` so the systemd path-watcher (Task 4) can target it precisely. Per terrain-prep notes, the path is `/srv/gitea/data/git/repositories/nexostrat/nexostrat.git`. This task verifies that and writes the first version of the system map.

**Files:**
- Create: `00_GOVERNANCE/system_map.md`

- [ ] **Step 1: Confirm Gitea container is running**

```bash
docker ps --filter name=gitea --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
# Expected: a running container named gitea*
```

- [ ] **Step 2: Verify the bind-mount path on the host**

```bash
docker inspect "$(docker ps -q --filter name=gitea | head -1)" \
  --format '{{json .Mounts}}' | python3 -m json.tool
```

Look for the mount whose `Destination` is `/data` (Gitea's standard internal path). The `Source` is the host-side absolute path. Per terrain prep: `/srv/gitea/data`.

- [ ] **Step 3: Verify the bare repo exists at the expected on-disk path**

```bash
GITEA_HOST_DATA="$(docker inspect "$(docker ps -q --filter name=gitea | head -1)" \
  --format '{{range .Mounts}}{{if eq .Destination "/data"}}{{.Source}}{{end}}{{end}}')"
echo "Gitea host data: $GITEA_HOST_DATA"
# Expected: /srv/gitea/data (or wherever the actual mount is)

BARE_REPO="$GITEA_HOST_DATA/git/repositories/nexostrat/nexostrat.git"
ls -la "$BARE_REPO" 2>&1 | head -10
# Expected: bare-repo contents (HEAD, config, hooks/, objects/, refs/, etc.)

ls -la "$BARE_REPO/refs/heads/" 2>&1
# Expected: a `main` file with the current SHA
```

If the path is different from what was documented, **note the actual path** and use it consistently in subsequent tasks. Per F25, the repo is at org `nexostrat` (not personal).

- [ ] **Step 4: Capture the Gitea container's user/group ownership**

```bash
ls -la "$BARE_REPO/refs/heads/main"
# Expected: owner is something like git:git or 1000:1000
# (we need to know this so the path-watcher can read the file)
```

The user `ricardo` may or may not have read access. If not, the systemd unit will need to run with sudo or be group-readable. Document the result.

- [ ] **Step 5: Write `00_GOVERNANCE/system_map.md`**

Write `/srv/Nexostrat/00_GOVERNANCE/system_map.md`:

```markdown
# System map — Nexostrat infrastructure

> **Updated:** 2026-05-14 (Plan 01b Task 1)
> **Owner:** Founder
> **Purpose:** Single source of truth for "where things live" across hosts,
> containers, and the systemd surface. Consult before adding any new unit,
> service, or scheduled job.

## Hosts

| Hostname | Tailscale IP | OS | Role | Notes |
|---|---|---|---|---|
| `ricardo-hp-laptop` | `100.64.121.80` | Linux Mint 22.2 | hp-server | Primary host; runs Gitea, bot, shadow stack |
| `<warm-standby-tbd>` | `<TBD>` | Linux Mint 22.2 | hp-standby | Filled at standby provisioning (Plan 01b Tasks 7-9) |
| `ricardo-desktop`     | `<TBD>` | Linux Mint 22.2 | ricardo-desktop | GPU host (Ollama); wake-on-LAN target |

> **OS pinning:** Linux Mint 22.2 LTS across all hosts at Stage 1. Bump this
> column (here and in `infra/machines/*.yaml`) when any host is upgraded.

## Docker stack on hp-server

Compose file: `/srv/Nexostrat/docker-compose.yml` (Plan 02 lands the actual compose; Plan 01b uses what already exists for Gitea).

| Container | Image (pinned) | Host port | Bound to | Purpose |
|---|---|---|---|---|
| `gitea`     | `gitea/gitea:1.22` | `3001` | Tailscale `100.64.121.80` | Git origin, web UI |
| `nexostrat-bot` | (custom — Plan 04) | (none) | n/a | Telegram bot service |
| (others)    | (Plan 02-08 add) | | | |

## Gitea on-disk paths

| What | Host-side path |
|---|---|
| Gitea data root (bind-mount of `/data` in container) | `/srv/gitea/data` |
| `nexostrat/nexostrat` bare repo | `/srv/gitea/data/git/repositories/nexostrat/nexostrat.git` |
| `refs/heads/main` (the watch target) | `/srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main` |
| Gitea container user/group | `git:git` (uid/gid likely 1000:1000 inside container) |

**Path-watcher access:** The mirror systemd units (Tasks 4-5) watch the
`refs/heads/main` file. The file is owned by Gitea's container user; the
host-side `ricardo` user reads via group permissions on `/srv/gitea/data`.
If permissions don't allow, the unit will need to chmod the data directory
or run with elevated privileges — captured at install time.

## SSH config

`~/.ssh/config` aliases for git operations:

| Host alias | Real host | Port | Identity |
|---|---|---|---|
| `gitea-nexostrat` | `100.64.121.80` (Tailscale) | `2222` | `~/.ssh/nexostrat_ed25519` |
| `github.com` | (default) | `22` | `~/.ssh/nexostrat_ed25519` |
| `codeberg.org` | (default) | `22` | `~/.ssh/nexostrat_ed25519` |

## Mirrors (populated by Tasks 4-5)

| Mirror | Remote URL | Trigger | Service |
|---|---|---|---|
| GitHub | `git@github.com:nexostrat/nexostrat.git` | systemd `.path` watching Gitea bare-repo `refs/heads/main` | `nexostrat-mirror-github.service` |
| Codeberg | `git@codeberg.org:nexostrat/nexostrat.git` | same | `nexostrat-mirror-codeberg.service` |

## Warm-standby (populated by Tasks 7-12)

| Field | Value |
|---|---|
| Hostname | `<TBD-at-provisioning>` |
| Tailscale IP | `<TBD>` |
| Clone path | `/srv/Nexostrat/` (mirror of HP) |
| Rsync source | `ricardo@hp-server:/srv/Nexostrat/` |
| Rsync schedule | nightly 03:00 America/Tijuana |
| Service status at rest | All Docker services pulled but stopped |
| Failover RTO target | 15-30 min |

## Systemd units (populated by Tasks 4-5, 9, 12)

System-level units at `/etc/systemd/system/`:

| Unit | Type | Trigger | Purpose |
|---|---|---|---|
| (filled by Plan 01b execution) | | | |

## Cross-cutting notes

- All mirror PATs (`GITHUB_MIRROR_PAT`, `CODEBERG_MIRROR_PAT`) live in
  `secrets.env.age` per `infra/secrets/MANIFEST.md`. The mirror service
  reads them via `infra/scripts/run-with-secrets.sh`.
- The age key for decryption is `~/.config/age/nexostrat.key.age` for
  `ricardo`. JP's same-named file on his machine has the same purpose.
- The mirror `.service` units are NOT triggered by Gitea internals (per
  C4 fix — Gitea hooks can't decrypt). They are triggered by `.path` units
  on the host that watch the bare-repo file.

## What this map is NOT

- Not a runbook (those live in `docs/runbooks/`).
- Not a credentials store (those live in `secrets.env.age`).
- Not auto-generated — humans update this when they touch infrastructure.
  Stale entries trigger a quarterly review (`00_PARTNERSHIP/reviews/`).
```

- [ ] **Step 6: Pre-create `00_GOVERNANCE/incidents/`, stage + commit**

```bash
# Pre-create the incidents folder so Task 11's HP-down runbook has a tracked
# destination on first incident (matches Plan 01a's scaffold-with-.gitkeep
# pattern; otherwise the folder appears mid-incident, which is the wrong time
# for tooling friction).
mkdir -p 00_GOVERNANCE/incidents
touch 00_GOVERNANCE/incidents/.gitkeep

git add 00_GOVERNANCE/system_map.md 00_GOVERNANCE/incidents/.gitkeep
git commit -m "$(cat <<'EOF'
Plan 01b Task 1 · system_map.md + incidents/ scaffold + Gitea path verified (F22, F25)

Verified Gitea bare-repo lives at:
  /srv/gitea/data/git/repositories/nexostrat/nexostrat.git

This is the path the mirror .path units (Tasks 4-5) will watch. Org-level
repo per F25 (not personal namespace).

00_GOVERNANCE/system_map.md is the new "where things live" reference,
populated incrementally as each Plan 01b task lands its piece.

00_GOVERNANCE/incidents/.gitkeep pre-creates the destination for Task 11's
HP-down post-mortem entries.

Spec refs: §1 (replication topology), F22-subset, F25, ADR-002.
EOF
)"
```

---

## Task 2: GitHub mirror — remote setup + first push + PAT in secrets

**Goal:** Add `github` as a remote on the HP working clone, generate a `GITHUB_MIRROR_PAT` (Personal Access Token) at github.com, store it in `secrets.env.age`, push the current `main` to GitHub once manually so the mirror exists with content.

**Files:**
- Modify: `secrets.env.age` (adds `GITHUB_MIRROR_PAT`)
- Modify: `infra/secrets/MANIFEST.md` (Last rotated)

- [ ] **Step 1: Generate the PAT at github.com**

Manual step (Ricardo): visit github.com/settings/tokens (classic) or beta fine-grained tokens UI. Create a token:
- Name: `nexostrat-mirror-2026-05-14`
- Scope: `repo` only (write to private repos)
- Expiration: 1 year (or no expiration for set-and-forget; rotation cadence in MANIFEST.md will catch it)

Copy the token. **Do not paste it into terminal history** (use the next step's stdin pattern).

- [ ] **Step 2: Add `GITHUB_MIRROR_PAT` to `secrets.env.age`**

```bash
TMP=/dev/shm/secrets-edit-$$
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/secrets.env.age > "$TMP"

# Edit the empty value (use nano, vim, or Ricardo's editor of choice)
# Reminder: never paste the PAT into shell history or any tracked file other
# than "$TMP" (in /dev/shm, shredded below). The Plan 01a Task 3 pre-commit
# secret-scan hook catches tokens in staged blobs as a safety net — but the
# right discipline is to not stage them in the first place.
nano "$TMP"
# Change line:  GITHUB_MIRROR_PAT=
# To:           GITHUB_MIRROR_PAT=<token-pasted-here>

# Re-encrypt
age -R /srv/Nexostrat/infra/age-recipients.txt \
    -o /srv/Nexostrat/secrets.env.age \
    "$TMP"
shred -u "$TMP"
```

- [ ] **Step 3: Verify the secret is reachable via the wrapper**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
    sh -c 'echo "PAT length: ${#GITHUB_MIRROR_PAT}"'
# Expected: "PAT length: 40" (classic token) or longer (fine-grained)
```

- [ ] **Step 4: Add the GitHub remote on HP working clone**

```bash
cd /srv/Nexostrat
git remote add github git@github.com:nexostrat/nexostrat.git 2>&1 || \
  git remote set-url github git@github.com:nexostrat/nexostrat.git

git remote -v | grep github
# Expected: 2 lines (fetch + push) for github
```

- [ ] **Step 5: First manual push to GitHub**

```bash
git push github main
# Expected: pushes current HEAD; GitHub UI now shows the repo with content
```

- [ ] **Step 6: Update `infra/secrets/MANIFEST.md` Last rotated for `GITHUB_MIRROR_PAT`**

Edit `/srv/Nexostrat/infra/secrets/MANIFEST.md` — change the row:

```
| `GITHUB_MIRROR_PAT` | GitHub | `nexostrat-mirror-github.service` (Plan 01b) | every 12 mo | (not yet provisioned) | scope: `repo` only |
```

To:

```
| `GITHUB_MIRROR_PAT` | GitHub | `nexostrat-mirror-github.service` (Plan 01b) | every 12 mo | 2026-05-14 | scope: `repo` only; classic PAT, no expiration |
```

(Replace "no expiration" with the actual expiry date if Ricardo set one.)

- [ ] **Step 7: Stage + commit**

```bash
git add secrets.env.age infra/secrets/MANIFEST.md
git commit -m "$(cat <<'EOF'
Plan 01b Task 2 · GitHub mirror remote + PAT

- GITHUB_MIRROR_PAT added to secrets.env.age (re-encrypted to both recipients)
- MANIFEST.md row updated (Last rotated = 2026-05-14)
- `github` remote added to HP working clone
  → git@github.com:nexostrat/nexostrat.git
- First manual push completed; GitHub repo populated

The systemd path-watcher unit (Task 4) will use the same remote going forward,
authenticated via the same PAT (decrypted via run-with-secrets.sh).

Spec refs: §3 (Backup ladder), ADR-006.
EOF
)"
git push origin main
```

---

## Task 3: Codeberg mirror — remote setup + first push + PAT in secrets (F7)

**Goal:** Same pattern as Task 2 but for Codeberg (`codeberg.org/nexostrat/nexostrat`). F7 was missing from the original Plan 01.

**Files:**
- Modify: `secrets.env.age` (adds `CODEBERG_MIRROR_PAT`)
- Modify: `infra/secrets/MANIFEST.md` (Last rotated)

- [ ] **Step 1: Generate the PAT at codeberg.org**

Manual step (Ricardo): visit codeberg.org/user/settings/applications. Create a new "access token":
- Name: `nexostrat-mirror-2026-05-14`
- Scopes: `write:repository`
- Click Generate Token; copy the value.

- [ ] **Step 2: Add `CODEBERG_MIRROR_PAT` to `secrets.env.age`**

Same pattern as Task 2 Step 2:

```bash
TMP=/dev/shm/secrets-edit-$$
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/secrets.env.age > "$TMP"

# Reminder: never paste the PAT into shell history or any tracked file other
# than "$TMP" (in /dev/shm, shredded below). The Plan 01a Task 3 pre-commit
# secret-scan hook catches tokens in staged blobs as a safety net — but the
# right discipline is to not stage them in the first place.
nano "$TMP"
# Change line:  CODEBERG_MIRROR_PAT=
# To:           CODEBERG_MIRROR_PAT=<token>

age -R /srv/Nexostrat/infra/age-recipients.txt \
    -o /srv/Nexostrat/secrets.env.age \
    "$TMP"
shred -u "$TMP"
```

- [ ] **Step 3: Verify via wrapper**

```bash
/srv/Nexostrat/infra/scripts/run-with-secrets.sh \
    sh -c 'echo "Codeberg PAT len: ${#CODEBERG_MIRROR_PAT}"'
# Expected: a non-zero number
```

- [ ] **Step 4: Add the Codeberg remote**

```bash
cd /srv/Nexostrat
git remote add codeberg git@codeberg.org:nexostrat/nexostrat.git 2>&1 || \
  git remote set-url codeberg git@codeberg.org:nexostrat/nexostrat.git

git remote -v | grep codeberg
# Expected: 2 lines for codeberg
```

- [ ] **Step 5: First manual push to Codeberg**

```bash
git push codeberg main
# Expected: pushes HEAD; Codeberg UI shows the repo populated
```

- [ ] **Step 6: Update `infra/secrets/MANIFEST.md` for `CODEBERG_MIRROR_PAT`**

Same edit pattern as Task 2 Step 6 — change `(not yet provisioned)` to `2026-05-14`.

- [ ] **Step 7: Stage + commit**

```bash
git add secrets.env.age infra/secrets/MANIFEST.md
git commit -m "$(cat <<'EOF'
Plan 01b Task 3 · Codeberg mirror remote + PAT (F7)

- CODEBERG_MIRROR_PAT added to secrets.env.age
- MANIFEST.md row updated (Last rotated = 2026-05-14)
- `codeberg` remote added; first manual push completed

Closes F7 (Codeberg mirror missing from original Plan 01). The mirror
systemd unit (Task 5) follows the same pattern as the GitHub one.

Spec refs: §3 (Backup ladder), F7, ADR-006.
EOF
)"
git push origin main
```

---

## Task 4: `nexostrat-mirror-github` systemd path-watcher (C4)

**Goal:** Install systemd `.path` + `.service` units that watch `/srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main` and push to GitHub when it changes. Replaces the dead Gitea-internal post-receive hook (C4 fix).

**Files:**
- Create: `infra/systemd/nexostrat-mirror-github.path`
- Create: `infra/systemd/nexostrat-mirror-github.service`
- Create: `infra/scripts/mirror-push.sh`
- Create: `infra/scripts/install-systemd-units.sh`

- [ ] **Step 1: Write the unified `mirror-push.sh` script**

Both mirror services call this script with the remote name as `$1`. Single script, two callers — DRY.

Create `/srv/Nexostrat/infra/scripts/mirror-push.sh`:

```bash
#!/usr/bin/env bash
# mirror-push.sh — Nexostrat
#
# Push the canonical local clone of /srv/Nexostrat/ to a named git remote.
# Called by nexostrat-mirror-<remote>.service (systemd).
#
# Usage: mirror-push.sh <remote>
#
# Exit codes:
#   0  push succeeded (or nothing to push)
#   1  push failed
#   2  remote not found / invalid argument

set -uo pipefail

REPO="/srv/Nexostrat"
REMOTE="${1:?usage: mirror-push.sh <remote>}"

cd "$REPO"

# Sanity: remote exists
if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "ERROR: remote '$REMOTE' not configured for $REPO" >&2
  exit 2
fi

# Use a deterministic timestamped log line so journalctl is greppable
TS=$(date -Iseconds)
echo "[$TS] mirror-push: pushing main → $REMOTE"

# The push uses the SSH key in ~/.ssh/config — no PAT needed for SSH-based
# remotes. The PATs in secrets.env.age are reserved for HTTPS fallback (TBD).
if git push "$REMOTE" main 2>&1; then
  echo "[$TS] mirror-push: $REMOTE OK"
  exit 0
else
  echo "[$TS] mirror-push: $REMOTE FAILED" >&2
  exit 1
fi
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/mirror-push.sh
```

**Note on PAT vs SSH:** The script uses SSH-based remotes (cleaner, no token expiration mid-mirror). The PAT in `secrets.env.age` is the fallback for when SSH-based push fails (e.g., GitHub SSH outage, key revocation). Stage 1 ships SSH-only; Plan 02 may add the HTTPS-PAT fallback path.

- [ ] **Step 2: Write the `nexostrat-mirror-github.service` unit**

Create `/srv/Nexostrat/infra/systemd/nexostrat-mirror-github.service`:

```ini
[Unit]
Description=Nexostrat — push HP origin to GitHub mirror
Documentation=file:///srv/Nexostrat/00_GOVERNANCE/system_map.md
After=network-online.target gitea.service
Wants=network-online.target

[Service]
Type=oneshot
User=ricardo
Group=ricardo
WorkingDirectory=/srv/Nexostrat
Environment=HOME=/home/ricardo
Environment=SSH_AUTH_SOCK=
ExecStart=/srv/Nexostrat/infra/scripts/mirror-push.sh github

# Hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/srv/Nexostrat
ProtectHome=read-only
# ricardo's HOME needs read for ~/.ssh/config + ~/.ssh/nexostrat_ed25519
BindReadOnlyPaths=/home/ricardo/.ssh

# Modest log retention
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nexostrat-mirror-github

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 3: Write the `nexostrat-mirror-github.path` unit**

Create `/srv/Nexostrat/infra/systemd/nexostrat-mirror-github.path`:

```ini
[Unit]
Description=Nexostrat — watch Gitea bare-repo refs/heads/main and trigger GitHub mirror
Documentation=file:///srv/Nexostrat/00_GOVERNANCE/system_map.md

[Path]
PathChanged=/srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main
Unit=nexostrat-mirror-github.service

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 4: Write the host-side installer script**

Create `/srv/Nexostrat/infra/scripts/install-systemd-units.sh`:

```bash
#!/usr/bin/env bash
# install-systemd-units.sh — Nexostrat
#
# Symlinks every unit file in infra/systemd/ to /etc/systemd/system/, runs
# `systemctl daemon-reload`, and enables (does not start) each one.
#
# Idempotent: re-running is safe; existing symlinks update; daemon-reload
# is always run.
#
# Requires sudo.

set -euo pipefail

REPO="/srv/Nexostrat"
SRC="$REPO/infra/systemd"
DST="/etc/systemd/system"

if [[ "$EUID" -ne 0 ]]; then
  echo "Re-running with sudo..."
  exec sudo "$0" "$@"
fi

echo "Installing units from $SRC"

shopt -s nullglob
units=("$SRC"/*.{service,path,timer})
[[ ${#units[@]} -gt 0 ]] || { echo "No units found in $SRC"; exit 0; }

for unit in "${units[@]}"; do
  base="$(basename "$unit")"
  ln -sf "$unit" "$DST/$base"
  echo "  symlinked $base"
done

systemctl daemon-reload
echo "daemon-reload OK"

for unit in "${units[@]}"; do
  base="$(basename "$unit")"
  systemctl enable "$base" >/dev/null 2>&1 || \
    { echo "WARN: enable $base — skipping (probably already enabled)"; continue; }
  echo "  enabled $base"
done

echo
echo "Installed and enabled. Use 'systemctl status <unit>' to inspect."
echo "Path units start watching as soon as they're started; .timer units"
echo "fire on their schedule. To start a .path unit now:"
echo "  sudo systemctl start nexostrat-mirror-github.path"
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/install-systemd-units.sh
```

- [ ] **Step 5: Install + start the GitHub mirror units**

```bash
bash /srv/Nexostrat/infra/scripts/install-systemd-units.sh
# Expected: symlink confirmations + daemon-reload OK + enabled lines

sudo systemctl start nexostrat-mirror-github.path
sudo systemctl status nexostrat-mirror-github.path --no-pager | head -10
# Expected: Active: active (waiting)
```

- [ ] **Step 6: Trigger a test push to validate the wire-up**

```bash
# Make a trivial change on HP, push to Gitea origin, watch the mirror fire
cd /srv/Nexostrat
date -Iseconds > infra/systemd/.last-mirror-test
git add infra/systemd/.last-mirror-test
git commit -m "Plan 01b Task 4 · mirror wire-up test"
git push origin main

# Watch journal for the mirror service to fire (typically <5s after push)
sudo journalctl -u nexostrat-mirror-github.service -f --since '1 minute ago'
# Expected: log lines from mirror-push.sh ending with "github OK"
# Ctrl-C after seeing the success line
```

- [ ] **Step 7: Verify the commit landed on GitHub**

```bash
# After the mirror fires:
sleep 10
git fetch github
git log --oneline github/main..HEAD
# Expected: empty (GitHub HEAD now matches local HEAD)

git rev-parse HEAD
git rev-parse github/main
# Expected: same SHA on both lines
```

If GitHub HEAD doesn't match within 60s, debug:
- `sudo journalctl -u nexostrat-mirror-github.service --since '5 minutes ago'`
- Verify SSH key agent / key permissions
- Check `git push github main` works manually

- [ ] **Step 8: Update `00_GOVERNANCE/system_map.md` mirror table**

Edit `/srv/Nexostrat/00_GOVERNANCE/system_map.md` — change the GitHub row from `(populated by Tasks 4-5)` to `OK 2026-05-14, validated end-to-end via test commit`. Add to the Systemd units table:

| Unit | Type | Trigger | Purpose |
|---|---|---|---|
| `nexostrat-mirror-github.path` | path-watcher | gitea bare-repo `refs/heads/main` change | Triggers `nexostrat-mirror-github.service` |
| `nexostrat-mirror-github.service` | oneshot | invoked by .path | Pushes HP origin → GitHub via SSH |

- [ ] **Step 9: Stage + commit**

```bash
git add infra/systemd/nexostrat-mirror-github.{path,service} \
        infra/scripts/{mirror-push.sh,install-systemd-units.sh} \
        00_GOVERNANCE/system_map.md \
        infra/systemd/.last-mirror-test
git commit -m "$(cat <<'EOF'
Plan 01b Task 4 · GitHub mirror systemd path-watcher (C4)

Replaces the original Plan-01 Gitea post-receive hook design with a
host-side systemd path-watcher (per C4 fix — Gitea-internal hooks can't
decrypt secrets and would silently die):

- nexostrat-mirror-github.path watches:
  /srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main
- nexostrat-mirror-github.service runs as ricardo, calls mirror-push.sh
  with `github` as remote arg
- SSH-based push (no PAT needed in normal path; PAT is HTTPS fallback)

infra/scripts/install-systemd-units.sh idempotently symlinks every unit
in infra/systemd/ to /etc/systemd/system/ and enables them.

Validated end-to-end: test commit on HP origin landed on GitHub within
~5 seconds.

Spec refs: §1 (replication), C4, ADRs 006, 029.
EOF
)"
git push origin main
```

The push above ALSO fires the mirror — the journal should show the new commit being pushed too. Watch:

```bash
sudo journalctl -u nexostrat-mirror-github.service --since '2 minutes ago' | tail -10
```

---

## Task 5: `nexostrat-mirror-codeberg` systemd path-watcher (F7)

**Goal:** Same pattern as Task 4, for Codeberg.

**Files:**
- Create: `infra/systemd/nexostrat-mirror-codeberg.path`
- Create: `infra/systemd/nexostrat-mirror-codeberg.service`

- [ ] **Step 1: Write the `nexostrat-mirror-codeberg.service` unit**

Create `/srv/Nexostrat/infra/systemd/nexostrat-mirror-codeberg.service`:

```ini
[Unit]
Description=Nexostrat — push HP origin to Codeberg mirror
Documentation=file:///srv/Nexostrat/00_GOVERNANCE/system_map.md
After=network-online.target gitea.service
Wants=network-online.target

[Service]
Type=oneshot
User=ricardo
Group=ricardo
WorkingDirectory=/srv/Nexostrat
Environment=HOME=/home/ricardo
Environment=SSH_AUTH_SOCK=
ExecStart=/srv/Nexostrat/infra/scripts/mirror-push.sh codeberg

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/srv/Nexostrat
ProtectHome=read-only
BindReadOnlyPaths=/home/ricardo/.ssh

StandardOutput=journal
StandardError=journal
SyslogIdentifier=nexostrat-mirror-codeberg

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 2: Write the `nexostrat-mirror-codeberg.path` unit**

Create `/srv/Nexostrat/infra/systemd/nexostrat-mirror-codeberg.path`:

```ini
[Unit]
Description=Nexostrat — watch Gitea bare-repo refs/heads/main and trigger Codeberg mirror
Documentation=file:///srv/Nexostrat/00_GOVERNANCE/system_map.md

[Path]
PathChanged=/srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main
Unit=nexostrat-mirror-codeberg.service

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 3: Re-run installer, start the Codeberg `.path`**

```bash
bash /srv/Nexostrat/infra/scripts/install-systemd-units.sh
sudo systemctl start nexostrat-mirror-codeberg.path
sudo systemctl status nexostrat-mirror-codeberg.path --no-pager | head -10
# Expected: Active: active (waiting)
```

- [ ] **Step 4: Trigger another test commit, watch BOTH mirrors fire**

```bash
cd /srv/Nexostrat
date -Iseconds > infra/systemd/.last-mirror-test
git add infra/systemd/.last-mirror-test
git commit -m "Plan 01b Task 5 · dual-mirror wire-up test"
git push origin main

sleep 30
sudo journalctl -u nexostrat-mirror-github.service -u nexostrat-mirror-codeberg.service \
  --since '1 minute ago' | tail -20
# Expected: BOTH services show "OK" lines
```

- [ ] **Step 5: Verify the commit landed on both remotes**

```bash
git fetch github
git fetch codeberg
git rev-parse HEAD github/main codeberg/main
# Expected: three identical SHAs
```

- [ ] **Step 6: Update `00_GOVERNANCE/system_map.md`**

Add the Codeberg unit rows to the Systemd units table; mark the Codeberg mirror row in the Mirrors table as `OK 2026-05-14`.

- [ ] **Step 7: Stage + commit**

```bash
git add infra/systemd/nexostrat-mirror-codeberg.{path,service} \
        00_GOVERNANCE/system_map.md \
        infra/systemd/.last-mirror-test

git commit -m "$(cat <<'EOF'
Plan 01b Task 5 · Codeberg mirror systemd path-watcher (F7)

Same pattern as Task 4 (GitHub) — different remote, same wiring.
End-to-end validated: test commit landed on github/main + codeberg/main
within seconds.

Closes F7.

Spec refs: §3 (Backup ladder), F7, ADRs 006, 029.
EOF
)"
git push origin main
```

---

## Task 6: 60-second mirror window verification

**Goal:** Tighten the success criterion: a single `git push origin main` results in BOTH GitHub HEAD and Codeberg HEAD matching within 60 seconds. Document the actual measured latency.

**Files:**
- Modify: `00_GOVERNANCE/system_map.md` (record measured latency)

- [ ] **Step 1: Set up a stopwatch test**

```bash
cd /srv/Nexostrat
date -Iseconds > infra/systemd/.last-mirror-test
git add infra/systemd/.last-mirror-test
git commit -m "Plan 01b Task 6 · 60s window timing test"

T0=$(date +%s)
git push origin main
echo "T0 = push completed at: $(date -Iseconds)"

# Poll GitHub
GITHUB_OK=
for i in {1..60}; do
  sleep 1
  GH_SHA=$(git ls-remote github main 2>/dev/null | awk '{print $1}')
  LOCAL_SHA=$(git rev-parse HEAD)
  if [[ "$GH_SHA" == "$LOCAL_SHA" ]]; then
    T_GH=$(date +%s)
    GITHUB_OK=$((T_GH - T0))
    echo "GitHub matched after ${GITHUB_OK}s"
    break
  fi
done

# Poll Codeberg
CODEBERG_OK=
for i in {1..60}; do
  sleep 1
  CB_SHA=$(git ls-remote codeberg main 2>/dev/null | awk '{print $1}')
  LOCAL_SHA=$(git rev-parse HEAD)
  if [[ "$CB_SHA" == "$LOCAL_SHA" ]]; then
    T_CB=$(date +%s)
    CODEBERG_OK=$((T_CB - T0))
    echo "Codeberg matched after ${CODEBERG_OK}s"
    break
  fi
done

[[ -n "$GITHUB_OK" && "$GITHUB_OK" -le 60 ]] && echo "GITHUB GREEN (${GITHUB_OK}s)" || echo "GITHUB RED"
[[ -n "$CODEBERG_OK" && "$CODEBERG_OK" -le 60 ]] && echo "CODEBERG GREEN (${CODEBERG_OK}s)" || echo "CODEBERG RED"
```

If either side exceeds 60s, debug:
- `sudo journalctl -u nexostrat-mirror-<remote>.service --since '5 minutes ago'`
- Network slowness
- SSH connection-timeout settings

- [ ] **Step 2: Record the measured latencies in `00_GOVERNANCE/system_map.md`**

Add a row to the Mirrors table or extend it:

```markdown
| Mirror | Remote URL | Trigger | Service | Last validated 60s window |
|---|---|---|---|---|
| GitHub | `git@github.com:nexostrat/nexostrat.git` | systemd `.path` | `nexostrat-mirror-github.service` | 2026-05-14 — XX seconds |
| Codeberg | `git@codeberg.org:nexostrat/nexostrat.git` | systemd `.path` | `nexostrat-mirror-codeberg.service` | 2026-05-14 — YY seconds |
```

(Replace XX, YY with the actual measurements.)

- [ ] **Step 3: Stage + commit**

```bash
git add 00_GOVERNANCE/system_map.md infra/systemd/.last-mirror-test
git commit -m "$(cat <<'EOF'
Plan 01b Task 6 · 60s mirror window measured + recorded

End-to-end stopwatch test: a single `git push origin main` results in
github/main and codeberg/main matching local HEAD within (measured) 60s.

Numbers recorded in 00_GOVERNANCE/system_map.md Mirrors table for future
regression checks.

Spec refs: §3 (Backup ladder success criterion).
EOF
)"
git push origin main
```

---

## ⏸ WARM-STANDBY GATE — Tasks 7-12 require physical second host

The next 6 tasks need a **second physical machine** (Linux Mint 22.2 minimum, ≥ 256 GB disk, on the Tailscale tailnet). If not available, pause execution here.

**Action when pausing:**
1. Update `CHECKPOINT.md` with "blocked on warm-standby host provisioning."
2. Push commits so far.
3. Tasks 1-6 alone don't qualify for `v0.1b-mirrors` tag — that tag requires the warm-standby cluster as well. Consider a `v0.1b-mirrors-only` interim tag if the standby is weeks out.

**Action when resuming:**
1. Confirm the standby host is up, Tailscale-joined, SSH-accessible from HP.
2. Update `infra/machines/hp-standby.yaml` with the actual hostname + IP.
3. Proceed to Task 7.

---

## Task 7: Warm-standby — host inventory + bootstrap prep

**Goal:** Fill in the placeholders in `infra/machines/hp-standby.yaml` and confirm the standby host meets minimum requirements.

**Files:**
- Modify: `infra/machines/hp-standby.yaml`

- [ ] **Step 1: Confirm the standby host details**

Ricardo gathers from the standby host:
- Hostname (`hostname` command).
- Tailscale IP (`tailscale ip -4`).
- Disk free (`df -h /` — needs ≥ 256 GB, ≥ 100 GB for the repo + Docker volumes).
- Linux Mint version (`lsb_release -a`).

- [ ] **Step 2: Edit `infra/machines/hp-standby.yaml`**

Use Edit to replace each `<TBD-at-provisioning>` placeholder with the real values. Confirm the resulting file parses:

```bash
python3 -c "import yaml; print(yaml.safe_load(open('/srv/Nexostrat/infra/machines/hp-standby.yaml')))"
# Expected: dict printed with no None placeholders
```

- [ ] **Step 3: Confirm SSH from HP to standby works (ricardo user)**

```bash
ssh ricardo@<standby-hostname-or-IP> "hostname && uptime"
# Expected: standby's hostname + uptime line
```

If SSH key-based auth isn't set up, copy the SSH key:

```bash
ssh-copy-id ricardo@<standby-hostname-or-IP>
```

- [ ] **Step 4: Stage + commit**

```bash
git add infra/machines/hp-standby.yaml
git commit -m "$(cat <<'EOF'
Plan 01b Task 7 · hp-standby.yaml — placeholders filled at provisioning

Standby host inventory captured. SSH ricardo@<standby> works
(key-based, no password prompt).

Hardware verified: Linux Mint 22.2, ≥256 GB disk, Tailscale-joined.

Spec refs: §5 (per-machine profiles), §3 (warm-standby).
EOF
)"
git push origin main
```

---

## Task 8: Warm-standby — initial clone + age key recovery roundtrip

**Goal:** Bootstrap the standby with an initial clone of `/srv/Nexostrat/`, install Ricardo's age key (passphrase-decrypted by Ricardo on the standby manually), verify the standby can decrypt vault content.

- [ ] **Step 1: SSH to standby, install required tools**

```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
sudo apt update
sudo apt install -y git age rsync python3 python3-pip pandoc docker.io docker-compose
sudo systemctl enable docker
sudo usermod -aG docker ricardo
EOF
)"
# Note: usermod requires logout/login to take effect — Step 2 reconnects
```

- [ ] **Step 2: Copy SSH key + config to the standby, then clone the repo**

First, copy HP's SSH key and `~/.ssh/config` to the standby so it can resolve
the `git@gitea-nexostrat` Tailscale alias (the alias lives only in HP's
config; standby's `~/.ssh/config` is empty on a fresh Mint install). This MUST
happen before the clone — otherwise the clone fails with a confusing "unknown
host" error and the operator debugs what looks like a network problem.

```bash
scp ~/.ssh/nexostrat_ed25519 ~/.ssh/nexostrat_ed25519.pub ricardo@<standby>:~/.ssh/
ssh ricardo@<standby> "chmod 600 ~/.ssh/nexostrat_ed25519"
scp ~/.ssh/config ricardo@<standby>:~/.ssh/config
```

Then SSH back in (so docker group takes effect from Step 1's `usermod`) and
clone:

```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
sudo mkdir -p /srv/Nexostrat && sudo chown ricardo:ricardo /srv/Nexostrat
cd /srv
# Tailscale alias gitea-nexostrat now resolves (key + config copied above)
git clone git@gitea-nexostrat:nexostrat/nexostrat.git Nexostrat
cd Nexostrat
git status
EOF
)"
# Expected: clean clone with current main checked out
```

- [ ] **Step 3: Install Ricardo's age key on the standby**

This is a manual step (Ricardo at the standby's keyboard or via SSH with passphrase prompts):

```bash
# On standby:
mkdir -p ~/.config/age
chmod 700 ~/.config/age

# Copy the encrypted private key from HP
# (use scp from HP to standby; the file remains encrypted in transit)
scp ricardo@<hp-server>:~/.config/age/nexostrat.key.age ~/.config/age/

ls -la ~/.config/age/nexostrat.key.age
# Expected: mode 600 file
```

- [ ] **Step 4: Verify standby can decrypt firm secrets (crypto round-trip test)**

Proves the standby's age key matches both recipients and can read the encrypted
firm-secrets pipeline. Decrypts `secrets.env.age` (the canonical artifact every
service touches via `run-with-secrets.sh`) and asserts a known variable name is
present.

```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
TMP=/dev/shm/secrets-roundtrip-$$
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/secrets.env.age > "$TMP"
# Sentinel: secrets.env.age contains the mirror PATs added by Tasks 2 + 3
grep -q "^GITHUB_MIRROR_PAT=" "$TMP" && echo "OK: standby decrypted secrets.env.age"
shred -u "$TMP"
EOF
)"
# Expected: "OK: standby decrypted secrets.env.age" — proves the standby has working
# decryption against the actual production secrets artifact.
# Note: the original draft of this step decrypted a partnership PDF
# (vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age) but that artifact
# was intentionally never created — see commit acdcc4a (2026-05-16) which reframed
# Plan 01a Task 17 to "markdown is the agreement" per the brothers-as-partners
# ceremony reduction. secrets.env.age is the durable round-trip target.
```

- [ ] **Step 5: Pre-pull all Docker images referenced in `docker-compose.yml`**

```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
cd /srv/Nexostrat
docker-compose pull 2>&1 | tail -20
# Expected: pulls all referenced images; services NOT started
EOF
)"
```

If `docker-compose.yml` doesn't exist yet on `main` (Plan 02 lands the full version), skip this step with a note. The interim Gitea-only compose does exist on the HP side; the standby should pull whatever's currently on `main`.

- [ ] **Step 6: Verify standby has no commits diverging from HP**

```bash
ssh ricardo@<standby> "cd /srv/Nexostrat && git rev-parse HEAD"
# Compare to HP:
git rev-parse HEAD
# Expected: same SHA on both lines
```

- [ ] **Step 7: NO commit yet** — this task installs material on the standby host but doesn't change the repo. Note in `STATUS.md` Recent activity that the standby is bootstrapped.

---

## Task 9: `nexostrat-warm-rsync.timer` + `.service` (HP-side, nightly 03:00)

**Goal:** Install systemd timer + service that does nightly rsync from `/srv/Nexostrat/` on HP to `/srv/Nexostrat/` on standby. Excludes ephemeral content (.git/objects pack files churn nightly otherwise; `.superpowers/`; logs).

**Files:**
- Create: `infra/systemd/nexostrat-warm-rsync.timer`
- Create: `infra/systemd/nexostrat-warm-rsync.service`
- Create: `infra/scripts/warm-rsync.sh`

- [ ] **Step 1: Write `warm-rsync.sh`**

Create `/srv/Nexostrat/infra/scripts/warm-rsync.sh`:

```bash
#!/usr/bin/env bash
# warm-rsync.sh — Nexostrat
#
# Rsync /srv/Nexostrat/ from HP to warm-standby.
# Called by nexostrat-warm-rsync.service (systemd timer).
#
# Excludes ephemeral content. Uses --delete so removed files on HP also get
# removed on standby (mirror semantics).
#
# Reads STANDBY_HOST from a file at $REPO/infra/systemd/standby-host.conf —
# avoids hardcoding the standby hostname in the script (so the script
# works for either Ricardo's or JP's eventual standby).

set -uo pipefail

REPO="/srv/Nexostrat"
HOST_CONF="$REPO/infra/systemd/standby-host.conf"

if [[ ! -f "$HOST_CONF" ]]; then
  echo "ERROR: $HOST_CONF not found — set STANDBY_HOST=ricardo@<host>" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$HOST_CONF"
: "${STANDBY_HOST:?STANDBY_HOST not set in $HOST_CONF}"

TS=$(date -Iseconds)
echo "[$TS] warm-rsync: starting → $STANDBY_HOST"

rsync -aAX --delete \
  --info=stats2 \
  --exclude='.superpowers/' \
  --exclude='.git/objects/incoming/' \
  --exclude='*.log' \
  --exclude='excalidraw.log' \
  --exclude='/dev/shm/' \
  "$REPO/" \
  "$STANDBY_HOST:$REPO/"
RC=$?

echo "[$TS] warm-rsync: exit code $RC"
exit $RC
```

```bash
chmod +x /srv/Nexostrat/infra/scripts/warm-rsync.sh
```

- [ ] **Step 2: Write the standby-host.conf (NOT committed; per-machine local)**

Add to `.gitignore` first (so the conf doesn't accidentally land in git):

```bash
echo "" >> /srv/Nexostrat/.gitignore
echo "# warm-rsync per-host config (machine-local)" >> /srv/Nexostrat/.gitignore
echo "infra/systemd/standby-host.conf" >> /srv/Nexostrat/.gitignore
```

Then write the file (NOT staged):

```bash
cat > /srv/Nexostrat/infra/systemd/standby-host.conf <<EOF
# Per-machine warm-rsync config — NOT in git
STANDBY_HOST=ricardo@<standby-hostname-or-IP>
EOF
```

- [ ] **Step 3: Write `nexostrat-warm-rsync.service`**

Create `/srv/Nexostrat/infra/systemd/nexostrat-warm-rsync.service`:

```ini
[Unit]
Description=Nexostrat — nightly warm-standby rsync
Documentation=file:///srv/Nexostrat/00_GOVERNANCE/system_map.md
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=ricardo
Group=ricardo
WorkingDirectory=/srv/Nexostrat
Environment=HOME=/home/ricardo
ExecStart=/srv/Nexostrat/infra/scripts/warm-rsync.sh

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/srv/Nexostrat
ProtectHome=read-only
BindReadOnlyPaths=/home/ricardo/.ssh

StandardOutput=journal
StandardError=journal
SyslogIdentifier=nexostrat-warm-rsync

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 4: Write `nexostrat-warm-rsync.timer` (nightly 03:00 America/Tijuana)**

Create `/srv/Nexostrat/infra/systemd/nexostrat-warm-rsync.timer`:

```ini
[Unit]
Description=Nexostrat — nightly warm-standby rsync timer
Documentation=file:///srv/Nexostrat/00_GOVERNANCE/system_map.md

[Timer]
# 03:00 America/Tijuana every night
OnCalendar=*-*-* 03:00:00 America/Tijuana
Persistent=true
RandomizedDelaySec=300

Unit=nexostrat-warm-rsync.service

[Install]
WantedBy=timers.target
```

`Persistent=true` ensures the rsync runs after a missed window (e.g., HP was off at 03:00). `RandomizedDelaySec=300` smears load across a 5-minute window in case other timers also fire at 03:00.

- [ ] **Step 5: Install + enable the timer**

```bash
bash /srv/Nexostrat/infra/scripts/install-systemd-units.sh
sudo systemctl start nexostrat-warm-rsync.timer
sudo systemctl status nexostrat-warm-rsync.timer --no-pager | head -10
# Expected: Active: active (waiting)

systemctl list-timers nexostrat-warm-rsync.timer --no-pager
# Expected: shows next-fire time at 03:00 America/Tijuana
```

- [ ] **Step 6: Stage + commit**

```bash
git add infra/systemd/nexostrat-warm-rsync.{timer,service} \
        infra/scripts/warm-rsync.sh \
        .gitignore
# NOTE: standby-host.conf is .gitignored — should NOT appear in `git status`
git status --short | grep standby-host && \
  { echo "ERROR: standby-host.conf staged — fix .gitignore"; exit 1; }

git commit -m "$(cat <<'EOF'
Plan 01b Task 9 · warm-rsync timer + service (nightly 03:00 America/Tijuana)

- nexostrat-warm-rsync.timer: OnCalendar=*-*-* 03:00:00 America/Tijuana,
  Persistent=true, RandomizedDelaySec=300
- nexostrat-warm-rsync.service: Type=oneshot, User=ricardo, hardened
  (NoNewPrivileges, PrivateTmp, ProtectSystem=strict)
- warm-rsync.sh reads STANDBY_HOST from infra/systemd/standby-host.conf
  (machine-local, .gitignored — so the same script works for any
  eventual standby host without hardcoding hostnames)

Excludes from rsync: .superpowers/, *.log, .git/objects/incoming/

Real start-and-verify test follows in Task 10 (F24 fix).

Spec refs: §3 (Backup ladder), F24, ADRs 006, 023, 029.
EOF
)"
git push origin main
```

---

## Task 10: Real warm-rsync smoke test (F24)

**Goal:** Per F24 fix, the smoke test must be a real `systemctl start` + verify `status=0/SUCCESS` with file-transferred count > 0. Replaces the original Plan-01 false-positive `--dry-run` smoke.

- [ ] **Step 1: Manually trigger the rsync**

```bash
sudo systemctl start nexostrat-warm-rsync.service
# Wait for completion — service is Type=oneshot, finishes when rsync exits
sleep 5

sudo systemctl status nexostrat-warm-rsync.service --no-pager | head -20
```

Look for:
- `Active: inactive (dead)` (oneshot finishes by exiting)
- `Process: ... ExecStart=... (code=exited, status=0/SUCCESS)`
- Log lines from `warm-rsync.sh` showing the file-transferred count (rsync `--info=stats2` output).

- [ ] **Step 2: Verify the explicit success criterion**

```bash
sudo systemctl show nexostrat-warm-rsync.service \
  --property=Result,ExecMainStatus
# Expected: Result=success, ExecMainStatus=0
```

- [ ] **Step 3: Confirm rsync transferred non-trivial content**

```bash
sudo journalctl -u nexostrat-warm-rsync.service --since '5 minutes ago' \
  | grep -E 'Number of files|Total file size'
# Expected: lines like
#   Number of files: 4321 (reg: 3210, dir: 1111)
#   Total file size: 12345678 bytes
```

- [ ] **Step 4: Verify content actually landed on standby**

```bash
ssh ricardo@<standby> "cd /srv/Nexostrat && ls 00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md && git log --oneline -1"
# Expected: file exists; HEAD SHA matches HP HEAD
```

If the standby is missing the partnership file or the SHAs differ, debug:
- `sudo journalctl -u nexostrat-warm-rsync.service --since '10 minutes ago'`
- Check `STANDBY_HOST` in `infra/systemd/standby-host.conf` is correct
- Verify rsync excludes aren't dropping required content

- [ ] **Step 5: Commit a single-line note in `00_GOVERNANCE/system_map.md`**

Update the warm-standby block to record the validated state:

```markdown
| Field | Value |
|---|---|
| Last validated rsync | 2026-05-14 — Result=success, ExecMainStatus=0, Number of files: NNNN |
```

```bash
git add 00_GOVERNANCE/system_map.md
git commit -m "$(cat <<'EOF'
Plan 01b Task 10 · warm-rsync real-trigger smoke test PASS (F24)

`sudo systemctl start nexostrat-warm-rsync.service` completes with
Result=success, ExecMainStatus=0, file count > 0. Standby's HEAD now
matches HP's HEAD; Standby has the partnership file (decryptable per
Task 8).

Closes F24 (the original Plan-01 --dry-run smoke would silently pass even
when the rsync had nothing to transfer; this real-trigger version proves
the timer-driven path works end-to-end).

Spec refs: §3, F24.
EOF
)"
git push origin main
```

---

## Task 11: HP-down failover runbook + dry-run

**Goal:** Write the `docs/runbooks/hp_down.md` runbook. Dry-run it on the standby so the procedure is verified, not just documented.

**Files:**
- Create: `docs/runbooks/hp_down.md`

- [ ] **Step 1: Write the runbook**

Write `/srv/Nexostrat/docs/runbooks/hp_down.md`:

```markdown
# Runbook — HP server down (failover to warm-standby)

**Trigger:** HP server unreachable; can't `git push`, can't reach Gitea web,
Tailscale shows HP as offline for ≥ 5 minutes during business hours.

**RTO target:** 15-30 minutes from trigger to standby serving.

**Required:** Ricardo's (or JP's) age key, SSH access to standby, Tailscale
working.

---

## Step 1 — Confirm HP is actually down

Before failing over, confirm it's not a network glitch on your end:

```bash
tailscale status | grep ricardo-hp-laptop
# Expected: shows the host. If "offline" for ≥5 min, proceed.

ping -c 3 100.64.121.80
# Expected: timeouts. If responses, this is a service issue, not a host issue —
# see docs/runbooks/service_restart.md instead (TBD).
```

---

## Step 2 — SSH to the standby

```bash
ssh ricardo@<standby-host>
```

If SSH fails, you have a bigger problem (standby also down or Tailscale
issue). Pause and triage Tailscale status; if both hosts are offline, this
is a network-side issue not a server-down issue.

---

## Step 3 — Bring the standby's repo up to date

```bash
cd /srv/Nexostrat
git pull origin main 2>&1 || git fetch origin && git reset --hard origin/main
```

(`git pull` fails if the standby's clone has *diverged* from origin — e.g.,
local commits during a prior partial failover. A clone that's merely *behind*
will succeed on pull. The fallback hard-reset is safe because the standby is
read-only between failovers.)

---

## Step 4 — Start the Docker stack

```bash
cd /srv/Nexostrat
docker-compose up -d
sleep 10
docker-compose ps
# Expected: all containers showing "Up" status
```

If any container fails to start:
- Check `docker-compose logs <service>` for the specific error.
- Most common: missing secrets — run `infra/scripts/run-with-secrets.sh docker-compose up -d`.

---

## Step 5 — Update Tailscale DNS (manual; takes ~60 seconds)

The firm's internal references use `gitea-nexostrat` resolved via
`~/.ssh/config` Host alias to `100.64.121.80` (HP's Tailscale IP). To swap:

```bash
# On EACH device using the Gitea alias:
# Case-insensitive match — OpenSSH canonical form is HostName (camelcase per
# ssh_config(5)), but some users hand-edit with lowercase Hostname.
sed -i.bak -E \
  -e 's/^([[:space:]]*)([Hh]ost[Nn]ame)[[:space:]]+100\.64\.121\.80/\1\2 <STANDBY_TAILSCALE_IP>/' \
  ~/.ssh/config

# Post-check — sed -i reports zero exit even on zero substitutions, so verify
# the swap actually landed. Errors loudly if not (load-bearing for failover).
if ! grep -qE "^[[:space:]]*[Hh]ost[Nn]ame[[:space:]]+<STANDBY_TAILSCALE_IP>" ~/.ssh/config; then
  echo "ERROR: sed produced no substitution — DNS swap did NOT happen" >&2
  echo "       Manually edit ~/.ssh/config so the gitea-nexostrat Host block" >&2
  echo "       points HostName at <STANDBY_TAILSCALE_IP>" >&2
  exit 1
fi
echo "OK: gitea-nexostrat HostName now points at <STANDBY_TAILSCALE_IP>"
```

Or, if you've set up Tailscale MagicDNS aliases (Stage 2 plan), update the
alias mapping in the Tailscale admin console.

For Stage 1 (manual), the impact is: each device needs a one-line `~/.ssh/config`
edit. Document that in this runbook so the procedure isn't surprising.

---

## Step 6 — Notify

```bash
# Telegram (Plan 04 must be running on standby):
echo "/note hp-down failover complete; standby active at <STANDBY_IP>" | \
  bot-cli   # script lands in Plan 04
```

Until Plan 04's Telegram bot is live, notify JP via the agreed out-of-band
personal channel (the channel itself is not specified in this runbook — keep
it private). Message template:
"Failover complete. Standby active at <IP>. Use git push as normal; gitea-nexostrat
SSH alias points to standby until further notice."

---

## Step 7 — Once HP is restored

1. Power up HP. Tailscale will reconnect automatically.
2. SSH to HP, do not start any services yet.
3. On HP: `cd /srv/Nexostrat && git pull origin main` (will pull any commits
   landed via the standby during the outage).
4. On standby: stop Docker (`cd /srv/Nexostrat && docker-compose down`).
5. On HP: `docker-compose up -d`.
6. Revert `~/.ssh/config` Hostname back to HP's IP on every device.
7. Manually trigger a warm-rsync to ensure standby is back in sync:
   `sudo systemctl start nexostrat-warm-rsync.service`.

---

## Step 8 — Post-mortem entry

Write a brief incident note in `00_GOVERNANCE/incidents/` (folder
auto-created if missing). Format:

```markdown
# YYYY-MM-DD HP-down incident

**Detected:** <time>
**Failover started:** <time>
**Failover complete:** <time>
**Restored:** <time>
**Cause:** <root cause if known>
**Lessons:** <what to fix in the runbook>
```

---

## Negative cases this runbook does NOT cover

- **HP + standby both down simultaneously.** See `docs/runbooks/total_outage.md`
  (Plan 10 writes it). Short version: pull from GitHub mirror to a fresh host,
  restore secrets from age-encrypted Bitwarden backup, follow normal bootstrap.
- **HP filesystem corrupted (data integrity issue, not host down).** Do NOT
  fail over until you've confirmed the corruption did NOT propagate via
  warm-rsync. Inspect last few rsync logs before deciding.
- **Active client work in progress on HP at moment of failure.** The standby
  has the most recent rsync content (max 24h old). Manually re-derive any
  in-progress work from CHECKPOINT.md + journal entries.
```

- [ ] **Step 2: Dry-run the failover**

Don't actually swap DNS — but verify Steps 1-4 of the runbook execute cleanly:

```bash
# Step 1 — confirm we can detect HP down (via tailscale status)
tailscale status | grep -i hp

# Step 2 — SSH to standby works
ssh ricardo@<standby> "echo standby-reachable"

# Step 3 — standby's git is up to date
ssh ricardo@<standby> "cd /srv/Nexostrat && git fetch origin && git status"

# Step 4 — docker-compose can be triggered (don't actually start; just validate)
ssh ricardo@<standby> "cd /srv/Nexostrat && docker-compose config | head -3"
```

Document the dry-run result. Time it: from "decide to fail over" to "standby
has Docker config validated" should be under 10 minutes for a practiced operator.

- [ ] **Step 3: Stage + commit**

```bash
git add docs/runbooks/hp_down.md
git commit -m "$(cat <<'EOF'
Plan 01b Task 11 · HP-down failover runbook + dry-run

docs/runbooks/hp_down.md walks the operator through:
1. Confirm HP is actually down (not a network glitch)
2. SSH to standby
3. git pull on standby
4. docker-compose up -d
5. Update Tailscale/SSH-config DNS pointing
6. Notify (manual, out-of-band; Plan 04 will Telegram-automate)
7. HP restoration sequence (stop standby, restart HP, re-rsync)
8. Post-mortem entry in 00_GOVERNANCE/incidents/

Dry-run completed: SSH to standby works; git fetch on standby works;
docker-compose config validates. Time-to-decision-to-validation ~10 min.

RTO target 15-30 min looks achievable.

Spec refs: §3 (Recovery procedures), ADR-006.
EOF
)"
git push origin main
```

---

## Task 12: Final verification + tag `v0.1b-mirrors`

**Goal:** Re-run every Plan-01b success criterion as a single end-to-end check, fix anything that doesn't pass, then tag `v0.1b-mirrors` and push.

- [ ] **Step 1: Mirror verification (60s window)**

Run the same stopwatch test from Task 6, recording the latest measurements:

```bash
cd /srv/Nexostrat
date -Iseconds > infra/systemd/.last-mirror-test
git add infra/systemd/.last-mirror-test
git commit -m "Plan 01b Task 12 · final verification commit"

T0=$(date +%s); git push origin main

for i in {1..60}; do
  sleep 1
  GH_SHA=$(git ls-remote github main | awk '{print $1}')
  CB_SHA=$(git ls-remote codeberg main | awk '{print $1}')
  LOCAL_SHA=$(git rev-parse HEAD)
  if [[ "$GH_SHA" == "$LOCAL_SHA" && "$CB_SHA" == "$LOCAL_SHA" ]]; then
    DT=$(($(date +%s) - T0))
    echo "BOTH MIRRORS GREEN after ${DT}s"
    break
  fi
done
```

- [ ] **Step 2: Warm-rsync verification (real trigger)**

```bash
sudo systemctl start nexostrat-warm-rsync.service
sleep 10
sudo systemctl show nexostrat-warm-rsync.service --property=Result,ExecMainStatus
# Expected: Result=success, ExecMainStatus=0
```

- [ ] **Step 3: Confirm working tree clean and commits pushed**

```bash
git status --short
git push origin main
# Expected: clean tree; everything pushed
```

- [ ] **Step 4: Update STATUS.md + tasks.json**

- Mark Plan 01b complete in STATUS Recent activity.
- Mark `t-plan-01b-execute` done in tasks.json.
- Mark `t-gitea-path-verify` done.
- Update Next sequence Step 1 → Plan 01c.

- [ ] **Step 5: Tag and push**

```bash
git tag -a v0.1b-mirrors -m "$(cat <<'EOF'
Nexostrat foundation milestone 01b · mirrors + warm-standby

Closes Plan 01b:
- GitHub mirror via systemd .path watching Gitea bare-repo (C4)
- Codeberg mirror, same pattern (F7)
- 60s mirror window verified end-to-end
- Warm-standby host bootstrapped (clone + age key + Docker images pulled)
- Nightly warm-rsync timer at 03:00 America/Tijuana (Persistent=true)
- Real warm-rsync smoke test PASS (F24 — replaces --dry-run false-positive)
- HP-down failover runbook + dry-run

00_GOVERNANCE/system_map.md updated with all unit + path + host info.

Next: Plan 01c (personas + hooks + integration test).
EOF
)"

git push origin main
git push origin v0.1b-mirrors
```

- [ ] **Step 6: Commit final STATUS/tasks updates**

```bash
git add STATUS.md tasks.json
git commit -m "Plan 01b Task 12 · STATUS + tasks update — Plan 01b DONE, tagged v0.1b-mirrors"
git push origin main
```

---

## Self-Review

**Spec coverage** — Every Plan 01b deliverable from the master-index header maps to a task:

- GitHub mirror systemd path-watcher (C4) → Task 4
- Codeberg mirror, same pattern (F7) → Task 5
- Gitea bare-repo path verified + 00_GOVERNANCE/system_map.md (F22 sub-task) → Task 1
- Warm-standby provisioning → Tasks 7-8
- Warm-rsync timer + service → Task 9
- Real warm-rsync smoke test (F24) → Task 10
- HP-down failover runbook → Task 11
- 00_GOVERNANCE/system_map.md (running document) → Tasks 1, 4, 5, 6, 10
- Repo tag `v0.1b-mirrors` → Task 12

**Placeholder scan** — `<standby>`, `<standby-hostname-or-IP>`, `<STANDBY_TAILSCALE_IP>` are intentional — they get filled by Ricardo at provisioning. No "TBD" or "implement later" in any executable instruction.

**Type consistency** — `STANDBY_HOST` variable name matches between `warm-rsync.sh` (Task 9) and `infra/systemd/standby-host.conf` (Task 9 Step 2). Mirror service unit names consistent across Tasks 4-6, 12. The `mirror-push.sh` arg name (`<remote>`) matches between Task 4 (definition) and Task 5 (reuse).

**Missing items found in self-review** — none.

---

## Execution handoff

Plan complete and saved to `00_META/plans/2026-05-14_plan-01b-mirrors.md`.

**Recommended execution path: subagent-driven** (`superpowers:subagent-driven-development`).

- Tasks 1-6 (mirror cluster) run in one session; gates only on Plan 01a tag + GitHub/Codeberg accounts existing.
- Tasks 7-12 (warm-standby cluster) run in a second session, gating on physical second host being available.
- Pre-flight checks at the top of this plan run once.

**Inline execution** — also viable; `superpowers:executing-plans` with checkpoints at Tasks 6, 8, 12.

---

*This plan inherits audit findings C4, F7, F22-subset, F24, F25. Plan 01c (personas + hooks + integration test) follows.*
