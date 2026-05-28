# Runbook — Fresh Workstation Bring-Up

**Goal:** Take a clean machine to a fully-operational Nexostrat workstation: clone the repo, decrypt vault secrets, run skills, commit + push with mirror fan-out working.

**Audience:** Ricardo (Founder). Same procedure on Desktop PC, Travel laptop, or any future Linux workstation.

**Estimated time:** 60–90 min wall-clock (≈30 min of that is whisper.cpp model downloads, which only apply to the recording-stack-equipped Desktop PC).

**Outcome:** Machine can do everything HP (`ricardo-hp-laptop`) does — read all repo content, decrypt vault secrets, run all 5 skills end-to-end, push commits that propagate to Gitea origin + GitHub mirror + Codeberg mirror automatically.

---

## When to use this

- Bringing up a new workstation (Desktop PC, travel laptop, replacement machine).
- Recovering from HP loss onto a fresh box (in conjunction with `docs/runbooks/hp_down.md` once that lands — Plan 02b territory).
- Onboarding any future operator who needs the same full-clone access (note: JP Light per ADR-021bis does NOT need this runbook — his interface is Telegram + email only, no clone).

**Do NOT use for:** the warm-standby cluster (Plan 01b Tasks 7-12, separate runbook when those land — different end-state: idle until failover, nightly rsync only, no interactive editing).

---

## Pre-flight checklist

Before starting, confirm you have:

- [ ] **Hardware:** x86_64, ≥8 GB RAM, ≥40 GB free on the partition that will hold `/srv/Nexostrat/`.
- [ ] **OS:** Linux Mint 22.x (Cinnamon or XFCE). Other Debian/Ubuntu derivatives work with the same `apt` lines; macOS adaptation in the appendix.
- [ ] **Sudo access** on the target machine.
- [ ] **Bitwarden master password** (for age private key recovery — Step 8).
- [ ] **Age passphrase** for `nexostrat.key.age` (memorized — it is not in Bitwarden).
- [ ] **Tailscale account** that owns `ricardo-hp-laptop` (`ricardomejiacaicedo@gmail.com` at time of writing). Admin console at <https://login.tailscale.com/admin/machines>.
- [ ] **Gitea ssh access** to the Tailscale-resident origin (HP must be online with `gitea` service up — verify by `tailscale status` from any joined host).
- [ ] **GitHub + Codeberg accounts** (`nexostrat` user on both) with permission to add a new SSH key per machine.

Pick the machine profile that matches the target:

| If the machine is … | Use profile | Role |
|---|---|---|
| The Desktop PC (GPU host, records meetings) | `infra/machines/ricardo-desktop.yaml` | Full dev + recording + Ollama GPU host |
| The travel laptop (read-mostly + edit) | `infra/machines/ricardo-travel.yaml` | Full dev, no recording, no GPU |
| HP itself (reference) | `infra/machines/hp-server.yaml` | Already bootstrapped — server origin |

Optional sections (Steps 11-13) are gated by role. Mandatory sections (Steps 1-10, 14) run on every machine.

---

## Step 1 — Base OS packages

Single `apt` line for the universal CLI base used by every Nexostrat workstation.

```bash
sudo apt update
sudo apt install -y \
    git age jq python3 python3-pip python3-venv \
    curl wget rsync openssh-client \
    pandoc libreoffice \
    build-essential
```

**Why each:**

- `git age jq` — repository + crypto + JSON munging (canonical Nexostrat tools).
- `python3 python3-pip python3-venv` — skills + Baserow migration scripts are Python.
- `curl wget rsync openssh-client` — everyday transport tools.
- `pandoc libreoffice` — skill renderers convert `.md → .docx → .pdf`; LibreOffice is the headless PDF path used in the Trixx pilot.
- `build-essential` — required if you'll also build whisper.cpp (Step 12). Harmless on machines that won't.

**Verify:**

```bash
git --version && age --version && python3 --version && pandoc --version | head -1 && libreoffice --version
```

All five should print a version line.

---

## Step 2 — Tailscale (network identity)

If `tailscale status` already works on the target machine and shows it on the tailnet, **skip to Step 3.**

Otherwise install Tailscale, authenticate, and confirm reachability to HP.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

The `up` command prints a URL — open it, authenticate as the same Tailscale account that owns HP. Once authenticated:

```bash
tailscale status
```

You should see the machine listed alongside `ricardo-hp-laptop`, `ricardo-desktop`, `ricardo-hp-travel`, and any other joined hosts.

**Confirm reachability to HP:**

```bash
ping -c 3 100.64.121.80    # ricardo-hp-laptop's Tailscale IP
```

3/3 packets returned ⇒ tailnet works. If 0/3, check the Tailscale admin console — both nodes must be in the same tailnet and not key-expired.

---

## Step 3 — SSH key + register on three remotes

Generate a per-machine SSH key (do not reuse keys across machines — easier to revoke a single device).

```bash
ssh-keygen -t ed25519 -f ~/.ssh/nexostrat_ed25519 -C "nexostrat-$(hostname)-$(date +%Y%m%d)"
# Accept the default passphrase-prompt flow. A passphrase is recommended; ssh-agent caches it.
```

Print the public key so you can paste it into the three remotes:

```bash
cat ~/.ssh/nexostrat_ed25519.pub
```

Add the public key to **all three** remotes:

1. **GitHub** — <https://github.com/settings/keys> → New SSH key → paste. Title: `nexostrat-<hostname>`. Type: Authentication.
2. **Codeberg** — <https://codeberg.org/user/settings/keys> → Add Key → paste.
3. **Gitea** — open <http://100.64.121.80:3000> from your browser (HP must be online + Tailscale up on this machine). Log in as `ricardo` → Settings → SSH/GPG Keys → Add Key → paste.

**Verify each remote responds to the new key:**

```bash
ssh -T -i ~/.ssh/nexostrat_ed25519 git@github.com
# expected: "Hi nexostrat! You've successfully authenticated, but GitHub does not provide shell access."

ssh -T -i ~/.ssh/nexostrat_ed25519 git@codeberg.org
# expected: "Hi there, nexostrat!" or similar greeting.

ssh -T -i ~/.ssh/nexostrat_ed25519 -p 2222 git@100.64.121.80
# expected: "Hi there, ricardo! You've successfully authenticated, but Gitea does not provide shell access."
```

All three must succeed before continuing.

---

## Step 4 — SSH config aliases

Add the canonical Nexostrat aliases so commands in `COMMANDS.md` and the repo's git remotes work unchanged on this machine.

Append to `~/.ssh/config` (create the file if it doesn't exist):

```sshconfig
Host gitea-nexostrat
  HostName 100.64.121.80
  Port 2222
  User git
  IdentityFile ~/.ssh/nexostrat_ed25519
  IdentitiesOnly yes

Host github-nexostrat
  HostName github.com
  User git
  IdentityFile ~/.ssh/nexostrat_ed25519
  IdentitiesOnly yes

Host codeberg-nexostrat
  HostName codeberg.org
  User git
  IdentityFile ~/.ssh/nexostrat_ed25519
  IdentitiesOnly yes
```

Set strict permissions if the file is fresh:

```bash
chmod 600 ~/.ssh/config
```

**Verify the aliases:**

```bash
ssh -T gitea-nexostrat && ssh -T github-nexostrat && ssh -T codeberg-nexostrat
```

All three should print their authenticated greetings without prompting for a key path.

---

## Step 5 — Git identity (Nexostrat)

The repo uses the firm identity (`Nexostrat <contacto@nexostrat.com>`), not your personal one. Set it **locally** so this only applies to the Nexostrat clone, not your other repos.

(Skip the global step and apply per-repo after cloning in Step 6 — cleaner.)

---

## Step 6 — Clone the repository

The canonical install path is `/srv/Nexostrat/` on every machine. Standardizing the path means scripts and the pre-commit hook (which hardcodes `/srv/Nexostrat/infra/hooks/`) work unchanged.

```bash
sudo mkdir -p /srv
sudo chown "$USER:$USER" /srv
git clone git@gitea-nexostrat:nexostrat/nexostrat.git /srv/Nexostrat
cd /srv/Nexostrat
```

If Gitea is unreachable for any reason (HP down, tailnet broken), clone from a mirror — the mirror cluster always has the latest pushed state:

```bash
git clone git@github-nexostrat:nexostrat/nexostrat.git /srv/Nexostrat
# or
git clone git@codeberg-nexostrat:nexostrat/nexostrat.git /srv/Nexostrat
```

If you clone from a mirror, fix the remote names so `origin` still points at Gitea (the canonical write target):

```bash
cd /srv/Nexostrat
git remote rename origin github          # if cloned from github
# or:  git remote rename origin codeberg  # if cloned from codeberg
git remote add origin git@gitea-nexostrat:nexostrat/nexostrat.git
git remote add codeberg git@codeberg-nexostrat:nexostrat/nexostrat.git 2>/dev/null || true
git remote add github   git@github-nexostrat:nexostrat/nexostrat.git   2>/dev/null || true
git fetch --all
```

Set the firm identity (per-repo, scoped to this clone):

```bash
cd /srv/Nexostrat
git config user.name  "Nexostrat"
git config user.email "contacto@nexostrat.com"
```

**Verify:**

```bash
git remote -v        # should list origin / github / codeberg, all pointing at nexostrat/nexostrat.git
git log --oneline -1 # should show the latest commit (matches HP)
```

---

## Step 7 — Install the pre-commit hook

Git does not track `.git/hooks/` content, so a fresh clone has no hooks active. Install the symlink to the in-repo orchestrator:

```bash
cd /srv/Nexostrat
ln -sf ../../infra/hooks/pre-commit .git/hooks/pre-commit
```

**Verify:**

```bash
ls -la .git/hooks/pre-commit
# expected: pre-commit -> ../../infra/hooks/pre-commit
```

The orchestrator (`infra/hooks/pre-commit`) runs four checks in order:

1. `pre-commit-secret-scan.sh` — blocks staged blobs containing known secret-prefix patterns (`AKIA…`, `sk-ant-…`, `ghp_…`, etc.).
2. `pre-commit-vault-age-only.sh` — refuses to commit anything under `vault/` that is not `*.age`.
3. `pre-commit-docs-pair.sh` — enforces the `.md` / `-explicado.md` doc-pair invariant (Plan 02b territory; currently a no-op if neither exists).
4. `pre-commit-checkpoint.sh` — warns if CHECKPOINT.md was touched by another session in the last 10 minutes (R4 concurrent-session guard).

Smoke-test the hook with a no-op commit attempt:

```bash
echo "# test" >> /tmp/test-precommit.md     # outside the repo
git add /tmp/test-precommit.md 2>&1 || true  # will fail because outside repo — that's fine
# The real test is in Step 10 below — round-trip commit.
```

---

## Step 8 — Recover the age private key

The age private key is the master credential for all vault content. It lives at `~/.config/age/nexostrat.key.age` (passphrase-protected) on every operator's machine. Recover from Bitwarden:

```bash
mkdir -p ~/.config/age
chmod 700 ~/.config/age
```

1. Open Bitwarden (web vault or desktop app, signed in as the account that owns the firm credentials).
2. Find the item: **"Nexostrat age private key (ricardo)"** or similar — it contains the contents of `nexostrat.key.age` as an attached file or as a `Secure Note` with the file body in the Notes field.
3. Save the file body to `~/.config/age/nexostrat.key.age` exactly.
4. Lock the file:

```bash
chmod 600 ~/.config/age/nexostrat.key.age
```

**Verify the recovered file is a valid age-encrypted private key:**

```bash
head -c 100 ~/.config/age/nexostrat.key.age
# expected: starts with "age-encryption.org/v1" header line
```

**Verify the passphrase decrypts it** (does not persist anything to disk):

```bash
age -d ~/.config/age/nexostrat.key.age > /dev/shm/.peek-privkey
head -c 30 /dev/shm/.peek-privkey
# expected: "AGE-SECRET-KEY-1..."
shred -u /dev/shm/.peek-privkey
```

If the passphrase fails: stop here. Either the file was corrupted in transit (re-download from Bitwarden), or you're using the wrong passphrase (no recovery — the passphrase is not stored anywhere).

---

## Step 9 — Decrypt-side smoke test (read secrets.env.age)

Confirm this machine can decrypt the real vault content that's in the repo. This is the operational proof that Steps 1-8 worked.

```bash
cd /srv/Nexostrat
infra/scripts/run-with-secrets.sh sh -c 'echo "OK · git_email=${GIT_USER_EMAIL:-unset} · github_pat_len=${#GITHUB_MIRROR_PAT}"'
```

The script:

1. Asks for your age passphrase (TTY prompt).
2. Decrypts `vault/secrets.env.age` into RAM (`/dev/shm/`).
3. Sources the env into a subshell.
4. Runs the trailing `sh -c` with those vars set.
5. Shreds the decrypted plaintext after the command exits.

**Expected output:**

```
OK · git_email=contacto@nexostrat.com · github_pat_len=40
```

The lengths and identity must match. If `github_pat_len=0`, the env var didn't decode — re-check that you pulled the same `secrets.env.age` content that HP has (run `sha256sum vault/secrets.env.age` on both machines and compare).

If the passphrase prompt loops forever: the wrapper is not running under a TTY (e.g., running inside a non-interactive shell). Run from a terminal directly.

---

## Step 10 — Round-trip commit + verify mirror fan-out

Final test: make a no-op commit, push it, watch all three remotes converge.

```bash
cd /srv/Nexostrat
# Create a tiny sentinel inside the journal (an acceptable, traceable artifact)
DATE=$(date +%Y-%m-%d)
HOST=$(hostname)
mkdir -p 00_META/journal
cat > 00_META/journal/${DATE}_workstation-bootstrap-${HOST}.md <<EOF
# Workstation bootstrap — ${HOST}

Date: $(date -Iseconds)
Operator: $(whoami)
Profile: ricardo-desktop OR ricardo-travel (delete one)

Round-trip smoke test from the new-workstation.md runbook. This commit
proves the machine can push to origin and mirrors fire.
EOF

git add 00_META/journal/${DATE}_workstation-bootstrap-${HOST}.md
git commit -m "workstation bootstrap · ${HOST} · runbook round-trip"
git push origin main
```

The push to `origin` (Gitea on HP) triggers the systemd `.path` watcher on HP, which mirrors to GitHub + Codeberg automatically within ~10 s.

**Verify all three remotes converged:**

```bash
sleep 15
git ls-remote origin    main | awk '{print "origin:    " $1}'
git ls-remote github    main | awk '{print "github:    " $1}'
git ls-remote codeberg  main | awk '{print "codeberg:  " $1}'
git rev-parse HEAD       | awk '{print "local:     " $1}'
```

All four hashes must match. If `github` or `codeberg` lags, give it another 30–60 s (the mirror service has a startup window). If they still don't converge after 2 min, check on HP: `systemctl status nexostrat-mirror-github.service nexostrat-mirror-codeberg.service`.

✅ Mandatory bring-up complete. The optional sections below depend on the machine's role.

---

## Step 11 — (Optional) Python skill dependencies

Only required if this machine will **run** skills locally (Skill 01–05). Read-and-edit-only doesn't need this (you can read all generated outputs without Python).

```bash
pip install --user python-docx pillow pyyaml requests pytest
```

**Verify with the harness:**

```bash
cd /srv/Nexostrat
bash skills/_test_harness/test_skills.sh
# expected: NN PASS · 0 SKIP · 0 FAIL  (NN currently 32 — adjust as harness evolves)
```

If a test fails specifically on PDF render, it's the LibreOffice headless path — ensure `libreoffice --headless --convert-to pdf` works from CLI.

**If this host will refresh `calendar_cache.json` (Phase 5 path):** the canonical filter import path is `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py` (per spec + `00_META/calendar_filter.md` + COMMANDS.md § Calendar cache refresh).

- **On `ricardo-hp-laptop` (server role):** `/srv/brain-hub` is the real install directory. Nothing to do here; the canonical path resolves directly.
- **On `ricardo-desktop` and any new desktop-role host:** the hub install lives at `/home/ricardo/brain-hub/`. Expose the canonical path with a symlink so future Claude sessions can `import` from `/srv/brain-hub` as the docs prescribe:

```bash
# /srv/ is ricardo:ricardo-owned on these hosts; no sudo
ln -s /home/ricardo/brain-hub /srv/brain-hub
# verify
python3 -c "import sys; sys.path.insert(0, '/srv/brain-hub'); from hub.google.calendar_filter_nexostrat import FILTER_VERSION; print(FILTER_VERSION)"
# expected: nexostrat-v1
```

Without this symlink on a desktop-role host the import resolves to the literal `/home/ricardo/` path — works but drifts from the spec, and breaks the moment Ricardo's home dir changes or another user runs the refresh.

---

## Step 12 — (Optional) Recording stack — Desktop PC only

The recording stack (OBS + whisper.cpp) is **only** required on the Desktop PC role. The travel laptop does not need this.

The canonical procedure already lives in `COMMANDS.md` § "Desktop PC → One-time install (fresh Linux Mint machine)". Run those subsections top to bottom:

1. § 1. OS packages (OBS, pavucontrol, ffmpeg, build-essential, cmake, pulseaudio-utils)
2. § 2. Build whisper.cpp at `/opt/whisper.cpp`
3. § 3. Download Spanish models (`small` fallback + `large-v3` preferred — ~3.5 GB total)
4. § 4. Install `~/bin/transcribe.sh`
5. § 5. OBS one-time configuration (Profile `audio-meeting` + Software x264 encoder + Global Audio Devices = Default)
6. § 6. Verify with the smoke-test recording

Allow ~30 min wall-clock for this (most of which is the large-v3 model download at ~50 MB/s).

---

## Step 13 — (Optional) Ollama — Desktop PC GPU host only

If this machine has an NVIDIA GPU and will serve as the Ollama host (per `ricardo-desktop.yaml` schedule: office hours 09:00-18:00 America/Tijuana):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the three models declared in the profile:

```bash
ollama pull llama3.1:8b
ollama pull qwen2.5:14b
ollama pull mistral:7b
```

**Verify:**

```bash
ollama list                    # all three models listed
ollama run llama3.1:8b "say OK in one word" --verbose 2>&1 | tail -5
```

GPU details (NVIDIA driver, CUDA): the Ollama installer handles driver detection; if it warns about missing driver, install via Linux Mint's Driver Manager and reboot before retrying.

---

## Step 14 — Update the machine profile

Now that the machine is bootstrapped, update its YAML profile with the now-known values.

Edit `infra/machines/<profile>.yaml`:

```yaml
hostname: <real-hostname>           # was <TBD-at-bootstrap>
tailscale_ip: 100.x.x.x             # from `tailscale status`
# Desktop-only:
wake_on_lan:
  mac_address: <aa:bb:cc:dd:ee:ff>  # from `ip link show | grep ether`
```

Commit the update:

```bash
git add infra/machines/<profile>.yaml
git commit -m "<profile>: lock in bootstrapped values"
git push origin main
```

---

## Validation checklist

Run this on the new machine to confirm bring-up is complete:

```bash
cd /srv/Nexostrat

echo "=== Network ==="
tailscale status | grep -E "ricardo-hp-laptop|$(hostname)"

echo "=== Repo ==="
git remote -v | grep -c nexostrat.git    # expect: 6 (3 remotes × fetch+push)
git rev-parse HEAD                       # should match HP

echo "=== Hooks ==="
test -L .git/hooks/pre-commit && echo "pre-commit symlink OK" || echo "FAIL: missing hook"

echo "=== Crypto ==="
test -f ~/.config/age/nexostrat.key.age && echo "privkey present" || echo "FAIL: missing privkey"
age -d ~/.config/age/nexostrat.key.age >/dev/shm/.peek 2>/dev/null \
  && { echo "passphrase OK"; shred -u /dev/shm/.peek; } \
  || echo "FAIL: passphrase or privkey corrupt"

echo "=== Vault read ==="
infra/scripts/run-with-secrets.sh sh -c 'test -n "$GITHUB_MIRROR_PAT" && echo "secrets.env decode OK"'

echo "=== Mirror remotes reachable ==="
git ls-remote github   HEAD 2>&1 | head -1
git ls-remote codeberg HEAD 2>&1 | head -1
```

All five sections should print success lines. If anything fails, jump to Troubleshooting below.

---

## Troubleshooting

### `ssh -T gitea-nexostrat` hangs or times out

HP is either offline, the Tailscale tunnel to HP is broken, or HP's Gitea is down. Diagnose:

```bash
tailscale ping ricardo-hp-laptop   # ICMP over tailnet
ssh -v -T gitea-nexostrat 2>&1 | head -20
```

If `tailscale ping` fails: HP is offline or both nodes are key-expired. Wake HP (Wake-on-LAN if configured, otherwise physical). Re-`tailscale up` if either side shows expired keys in the admin console.

### `age -d` says "no identity matched any of the recipients"

The private key you recovered does NOT match any recipient stanza in the file you're trying to decrypt. Two causes:

1. You restored the wrong account's private key (e.g., a personal age key, not the firm one).
2. The file was encrypted before your pubkey was added to `infra/age-recipients.txt`.

Check which recipients the file encrypts to:

```bash
head -c 500 <file>.age
```

You should see two `-> X25519 …` recipient stanzas (Ricardo + JP). If you only see one, the file pre-dates ADR-003 — re-encrypt it from a machine that can decrypt.

### `secrets.env.age` decodes but env vars are empty / wrong length

The wrapper sources the file correctly but the values are stale. Compare against HP:

```bash
sha256sum vault/secrets.env.age   # run on both machines
```

If they differ, `git pull` on both and try again. If they still differ, someone has an unpushed re-encryption — investigate before continuing.

### Pre-commit hook fires on a clean commit and blocks it

The secret-scan or vault-age-only check found something. Read the hook's error message carefully:

- Secret-scan hit: the staged blob matches a known secret prefix. If it's a real secret, do NOT bypass — sanitize the file and retry. If it's a false positive (e.g., a fixture string), the scanner has a runtime-assembly trick documented in `infra/hooks/pre-commit-secret-scan.sh` itself.
- Vault-age-only hit: you're trying to commit a plaintext file under `vault/`. Either age-encrypt it first or move it elsewhere.

Never bypass with `git commit --no-verify` unless Ricardo has explicitly authorized it for a specific, understood reason.

### Mirror push lags >2 min behind origin

On HP:

```bash
sudo systemctl status nexostrat-mirror-github.service nexostrat-mirror-codeberg.service
sudo journalctl -u nexostrat-mirror-github.service -n 30
```

The `.path` watcher fires on writes to `refs/heads/main` inside the Gitea bare repo. If the service is in a failed state, restart it:

```bash
sudo systemctl restart nexostrat-mirror-github.service
```

If the failure repeats: check the PAT in `secrets.env.age` is still valid (GitHub PATs rotate; classic PATs default 90-day expiry).

---

## macOS adaptation (future-state, JP-Heavy flip)

The current stage (2026-05) does not run this runbook on macOS — JP Light per ADR-021bis needs no clone. If JP later flips to Heavy mode, the following deltas apply to the procedure above. Treat this as a sketch; validate every line in a focused session before relying on it.

| Step | Linux Mint | macOS adaptation |
|---|---|---|
| 1 (apt) | `apt install …` | `brew install git age jq python pandoc libreoffice` + GNU coreutils for `shred` → `brew install coreutils` (provides `gshred`); replace `shred` with `gshred` in scripts or PATH-alias it. |
| 2 (Tailscale) | install.sh | App Store or `brew install --cask tailscale`. |
| 7 (hooks) | symlink works fine | symlink works fine on APFS. |
| 8 (vault location for plaintext) | `/dev/shm` (tmpfs) | macOS has no `/dev/shm`. Use a RAM disk: `diskutil erasevolume HFS+ ramdisk $(hdiutil attach -nomount ram://1048576)` (≈512 MB), then `/Volumes/ramdisk` in place of `/dev/shm`. Tear down at logout. |
| 12 (recording) | OBS via apt | OBS via brew cask. Whisper.cpp builds the same. |
| 13 (Ollama) | Linux installer | macOS app from ollama.com — uses Metal GPU automatically. |

ADR-021bis change: flipping JP from Light to Heavy is a deliberate event requiring its own ADR; do not bring up `jp-mac` as a Heavy host without that ADR landing first.

---

## Quick reference — full bring-up in ~25 commands

For a future ad-hoc rerun on a known-good base. Each line is one mandatory step from above; copy-paste sequential:

```bash
sudo apt update && sudo apt install -y git age jq python3 python3-pip python3-venv curl wget rsync openssh-client pandoc libreoffice build-essential

# Tailscale — skip if already joined
curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up

# SSH key (replace HOST with your hostname)
ssh-keygen -t ed25519 -f ~/.ssh/nexostrat_ed25519 -C "nexostrat-$(hostname)-$(date +%Y%m%d)"
cat ~/.ssh/nexostrat_ed25519.pub    # paste into github + codeberg + gitea web UIs

# SSH config — append the three Host blocks per Step 4

# Clone + identity
sudo mkdir -p /srv && sudo chown "$USER:$USER" /srv
git clone git@gitea-nexostrat:nexostrat/nexostrat.git /srv/Nexostrat
cd /srv/Nexostrat
git config user.name "Nexostrat" && git config user.email "contacto@nexostrat.com"
ln -sf ../../infra/hooks/pre-commit .git/hooks/pre-commit

# Age key — restore from Bitwarden to ~/.config/age/nexostrat.key.age (chmod 600)

# Smoke
infra/scripts/run-with-secrets.sh sh -c 'echo "decode OK; pat_len=${#GITHUB_MIRROR_PAT}"'

# Round-trip commit (Step 10 block above)

# Profile update — edit infra/machines/<profile>.yaml with real hostname + tailscale_ip
```

---

## Change log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-20 | Founder (Ricardo + Claude) | Initial runbook. Drafted from option (a) of session-10 deploy-readiness assessment. Validates on first walkthrough — update line-by-line if any step needs adjustment. |
