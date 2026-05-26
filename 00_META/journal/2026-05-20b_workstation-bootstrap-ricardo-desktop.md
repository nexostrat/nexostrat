# Workstation bootstrap — ricardo-desktop

Date: 2026-05-20T17:57:13-07:00
Operator: ricardo
Profile: ricardo-desktop

Round-trip smoke test from the new-workstation.md runbook. This commit
proves the machine can push to origin and mirrors fire.

## Mirror fan-out — fix verified

Discovered during this bring-up: mirror-push.sh pushed from HP's stale
local clone, so off-HP pushes silently no-op'd. Patched in 03d15f8 to
fetch origin first then push origin/main. This commit is the test artifact.
Concurrency fix (commit 643e4ec): each service uses refs/mirror-stage/<remote>.
URL-based fetch (commit follow-up): bypasses configured refspec to remove the last race.

---

# 2026-05-20 — Desktop workstation bring-up (session summary)

**Session type:** maintenance
**Duration:** ~4 hours (interrupted by a power outage mid-session, resumed)
**Agent:** Claude

## What was done

- Bootstrapped `ricardo-desktop` (Linux Mint 22.3, RTX 3060 Ti, 31 GB RAM, Tailscale 100.104.83.2) as a full Nexostrat workstation per `~/Desktop/new-workstation.md`.
- Generated `~/.ssh/nexostrat_ed25519`, added to GitHub + Codeberg + Gitea; wrote three `*-nexostrat` Host blocks to `~/.ssh/config`.
- Recovered `~/.config/age/nexostrat.key.age` via scp from HP (Bitwarden held only the public key — see Decisions).
- Cloned `git@gitea-nexostrat:nexostrat/nexostrat.git` → `/srv/Nexostrat`, set per-repo identity `Nexostrat <contacto@nexostrat.com>`, installed `infra/hooks/pre-commit` symlink.
- Validated Step 9 vault decrypt (`github_pat_len=40`) and Step 10 round-trip commit.
- Pulled Ollama models the profile prescribed: `llama3.1:8b` + `mistral:7b` (qwen2.5:14b already present).
- Installed Python skill deps via apt (`python3-pip python3-docx python3-pytest python3-pandas python3-openpyxl`) — chose apt over `pip --break-system-packages` because of PEP 668 on Ubuntu 24-based Mint. Harness: **32 PASS · 0 SKIP · 0 FAIL** (`infra/scripts/test_skills.sh`).
- Updated `infra/machines/ricardo-desktop.yaml` with hostname, tailscale_ip, MAC `04:d9:f5:7f:12:a2` (enp4s0), OS 22.3, GPU model (commit `a8c3da1`).

## Bugs found and fixed in `infra/scripts/mirror-push.sh` (3 commits)

- **`03d15f8`** — script pushed HP's stale local `main` instead of fetching first; off-HP pushes silently no-op'd ("Everything up-to-date" because HP's local clone was behind). Fix: fetch origin, push `origin/main:refs/heads/main`.
- **`643e4ec`** — discovered race: both mirror services fire on the same `.path` event and ran concurrent fetches into `refs/remotes/origin/main`, contending on the ref lock ("cannot lock ref ... is at X but expected Y"). Fix: per-remote staging ref `refs/mirror-stage/<remote>`.
- **`7147111`** — staging ref alone wasn't enough; `git fetch origin <refspec>` ALSO honors the configured `fetch = +refs/heads/*:refs/remotes/origin/*` and updates `origin/main` in parallel. Fix: URL-form fetch (`git fetch <url>` not `git fetch origin`) bypasses configured refspecs.
- End-to-end verified: pushed test commits `8c38609`, `d5f3eaf`, `97ee871`; all four (local, origin, github, codeberg) converged on `97ee871` after the last push.

## Decisions made

- **Bitwarden flagged as priority 1** — the item only held the public key, useless for decryption. We scp'd from HP as a fallback, but a future bring-up without HP available would have no path. User updated Bitwarden with the base64 of `nexostrat.key.age` later in the session.
- **Mirror fix approach** — chose URL-form fetch + per-remote staging ref over (a) retry-on-lock-conflict, (b) pushing from the bare repo with hardcoded URLs, (c) serializing into a single mirror service. The chosen approach minimizes change to systemd/wrapper structure and has no risk of clobbering uncommitted edits in HP's working tree.
- **Python deps via apt, not pip** — PEP 668 on Ubuntu 24 / Mint 22 blocks `pip install --user`. `--break-system-packages` works but pollutes system Python; apt packages cover all 7 deps (python-docx, pillow, pyyaml, requests, pytest, pandas, openpyxl).
- **SSH key has no passphrase** — picked for autonomy during bring-up; user can re-key with `ssh-keygen -p -f ~/.ssh/nexostrat_ed25519` later. Trade-off accepted.
- **Existing `id_ed25519` left in Gitea alongside new key** — `id_ed25519` is for general HP SSH access (per existing `Host ricardo-hp-laptop` block), `nexostrat_ed25519` is the dedicated firm key. Two keys, two purposes; revoking the machine requires removing both.

## Open items

- **Runbook not committed to the repo.** Lives at `~/Desktop/new-workstation.md` on desktop. HP has an untracked copy at `docs/runbooks/new-workstation.md`. User declined to commit during this session. If a future session wants it canonical, the desktop's version is the most recently updated (has the 6-item drift correction in its change log).
- **`~/Desktop/DESKTOP_PC_COMMANDS.md` has a small bug** — Cross-PC nav line `ssh -p 2222 ricardo@100.64.121.80` should be `git@`, not `ricardo@`. User left as-is; the new Nexostrat section uses the correct `gitea-nexostrat` alias so it's shadowed in practice.
- **`infra/machines/ricardo-desktop.yaml` field `hooks.pre_commit`** points to `infra/hooks/pre-commit-secret-scan.sh` but in reality `infra/hooks/pre-commit` is the orchestrator that runs all 4 checks. Minor doc accuracy item.
- **`git pull origin main` on HP failed twice with "Cannot fast-forward to multiple branches"** during mirror-fix iteration — workaround was `git fetch origin main && git merge --ff-only FETCH_HEAD`. Likely caused by stale `FETCH_HEAD` entries from the earlier failed mirror service fetches. Worth a root-cause investigation separately.

## Notes

- **Doc drift in `~/Desktop/new-workstation.md` corrected** (change log entry added): Gitea web port 3001 (not 3000); `secrets.env.age` at repo root (not `vault/`); `GIT_USER_EMAIL` no longer in secrets; test harness at `infra/scripts/test_skills.sh`; PEP 668 → apt; Bitwarden body must be base64.
- **Per-user session memory updated** at `~/.claude/projects/-home-ricardo/memory/`: added `project_nexostrat.md`, refreshed `reference_machines.md` (new `ricardo-desktop` entry replacing the old Windows 100.82.111.85), index updated in `MEMORY.md`.
- **`~/Desktop/DESKTOP_PC_COMMANDS.md`** gained a new "Nexostrat (firm workspace)" section + 3 Quick-reference one-liners.
- HP mirror flow now race-free for off-HP pushes — confirmed by clean fan-out on `97ee871`.
