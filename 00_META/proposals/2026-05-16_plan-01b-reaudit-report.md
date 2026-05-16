# Plan 01b re-audit report

> **Audit date:** 2026-05-16
> **Auditor:** dispatched general-purpose agent (Opus 4.7, 1M context) with risk-auditor persona inlined
> **Audited:** `00_META/plans/2026-05-14_plan-01b-mirrors.md` (1751 lines, 12 tasks)
> **Audited against:** `v0.1a-foundation` baseline (commit `acdcc4a` + hard-system-audit patches through HEAD `4d6b46b` on `main`)
> **Audit brief:** inline dispatch (not file-based), inheriting the format from 2026-05-13/14/16 priors
> **Verdict:** **YELLOW (small)**

---

## 1. Verdict + counts

**Verdict: YELLOW (small).** Plan 01b is architecturally sound and execute-ready **after surgical patches**. No CRITICAL findings; no DESIGN-RETHINK FLAG. The plan correctly inherits the C4 amendment (Gitea hook → host-side systemd path-watcher), correctly closes F7 (Codeberg mirror), correctly closes the F22 subset (Gitea-bare-repo verification with n8n dropped), correctly closes F24 (real `systemctl start` rather than `--dry-run`), correctly closes F25 (org `nexostrat`). The systemd unit shapes are clean, ADR-029 (Python + systemd, no n8n) and ADR-013 (`events.jsonl` as inter-persona spine) are respected, and the warm-rsync + failover model maps directly to the CLAUDE.md backup posture.

What pulls the verdict to YELLOW are **five HIGH findings**, all surgical:
1. Three process-substitution age-decrypt sites at lines 330/432/1118 — the same defect the hard audit pre-flagged. Mechanical patch.
2. Task 8 Step 4's decrypt-roundtrip targets `vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age` — a file that **does not exist** and intentionally never will (commit `acdcc4a` reframed the partnership to markdown-is-the-agreement; vault/partnership has only `.gitkeep`). Substitute target needed.
3. Two Signal references inside the Nexostrat-internal failover runbook violate the 2026-05-16 Telegram-only directive.
4. The HP-down failover runbook's `sed` DNS-swap pattern (`s/Hostname 100.64.121.80/.../`) will never match — actual SSH config uses `HostName` (capital N). Silent failure on a load-bearing recovery step.
5. Task 8 Step 2 `sudo chown ricardo:ricardo /srv` chowns the entire `/srv` directory, which on the standby will collide with any existing `/srv/gitea`, `/srv/atten-bot`, etc. directories. Should be scoped to `/srv/Nexostrat`.

The MEDIUM and LOW lanes carry execution-friction items: a task-range typo, a docker package coexistence concern, a runbook step-execution path-order subtlety, missing pre-flight checks for the standby SSH config, and a Signal reference in the systemd-trigger sentinel notification. All cheap to amend.

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| HIGH | 5 |
| MEDIUM | 7 |
| LOW | 5 |

---

## 2. Findings table

| ID | Title | Plan line(s) | Source-of-truth ref | Reality | Severity | Recommendation |
|---|---|---|---|---|---|---|
| H1 | Three process-substitution age-decrypt sites violate the Plan-01a-established direct-`-i` pattern; will fail in TTY-less subshells | `2026-05-14_plan-01b-mirrors.md:330, 432, 1118` | `infra/scripts/run-with-secrets.sh:53-57` (direct `-i $PRIV_KEY_AGE`); commit `7e950ee` patched 11 sites of the same defect across Plan 01a | All 3 plan sites still use `age -d -i <(age -d ~/.config/age/nexostrat.key.age) <ciphertext>` | HIGH | Mechanical patch to `age -d -i ~/.config/age/nexostrat.key.age <ciphertext>` at all 3 sites. |
| H2 | Task 8 Step 4 decrypts a partnership PDF artifact that does not exist | `2026-05-14_plan-01b-mirrors.md:1116-1126` | `git show acdcc4a` ("Plan 01a Task 17 reframed · PARTNERSHIP_AGREEMENT.md (markdown is the agreement)"); `00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md:96` ("Form of agreement: plain markdown (no notarized PDF; brothers-as-partners)") | `find /srv/Nexostrat/vault/partnership -type f` returns only `.gitkeep`. The only `.age` file in vault is `vault/keys/sentinel-ricardo-to-jp.age` (the Direction-A roundtrip sentinel) | HIGH | Replace the decrypt target with one that actually exists. Two options: (a) decrypt `secrets.env.age` (already present, exercised by `run-with-secrets.sh`); (b) decrypt `vault/keys/sentinel-ricardo-to-jp.age` and assert `file`-type is text (and shred). Option (a) is cleaner — it tests the same crypto path AND the secrets pipeline. |
| H3 | Failover runbook hardcodes Signal as the JP-notify channel; violates the 2026-05-16 Telegram-only directive for Nexostrat artifacts | `2026-05-14_plan-01b-mirrors.md:1525, 1610` | Project memory `project_no_notion.md` + Ricardo 2026-05-16 directive: "Nexostrat uses Telegram; Signal is his personal-only channel and must not appear in Nexostrat artifacts"; CLAUDE.md "External coordination: Ricardo ↔ JP: Signal messages (async). Telegram bot (Plan 04+) for in-system events" — note Signal is permitted for personal coord but should NOT be the documented runbook channel inside Nexostrat artifacts | Line 1525: `Until Plan 04 is live, send a Signal message to JP manually:`. Line 1610: `6. Notify (Signal manual; Plan 04 will Telegram-automate)` | HIGH | Reword both to "Until Plan 04's Telegram bot is live, notify JP via the agreed personal channel (out of band; not specified in this runbook)." Removes Signal from Nexostrat-internal artifacts while keeping the operational reality. |
| H4 | HP-down runbook DNS-swap `sed` pattern will never match — case mismatch with actual SSH config syntax | `2026-05-14_plan-01b-mirrors.md:1502-1507` | `~/.ssh/config:20` uses `HostName 100.64.121.80` (camelcase, per OpenSSH `ssh_config(5)` canonical form) | Plan 01b pattern `s/Hostname 100.64.121.80/Hostname <STANDBY_TAILSCALE_IP>/` (lowercase `n`). Will silently produce zero substitutions; `.bak` file will be byte-identical to the original; failover continues to point at HP. | HIGH | Change both `Hostname` → `HostName` in the sed pattern. Better still: use `-e` with a case-insensitive matcher `sed -i.bak -E 's/^([Hh]ost[Nn]ame)[[:space:]]+100\.64\.121\.80/\1 <STANDBY_TAILSCALE_IP>/'`. Add a `grep -c HostName ~/.ssh/config.bak` post-check to confirm the substitution actually happened. |
| H5 | Task 8 Step 2 chowns all of `/srv` to `ricardo:ricardo`; collides with any existing service directories on the standby | `2026-05-14_plan-01b-mirrors.md:1076` | OS convention: `/srv` is the canonical site-data root and typically contains multiple service dirs (matching HP's layout: `/srv/gitea`, `/srv/atten-bot`, `/srv/Nexostrat`, etc., observed via `ls /srv/`); chowning the parent recursively breaks them | `sudo mkdir -p /srv && sudo chown ricardo:ricardo /srv` — the chown is NOT recursive (no `-R`), so only `/srv` itself becomes ricardo-owned; this is mostly harmless for *future* dirs but still wrong (a fresh `/srv` should be root-owned 0755 per FHS). Larger problem if `-R` is later added or if the standby happens to have existing `/srv/*` content from prior bootstraps. | HIGH | Replace with: `sudo mkdir -p /srv/Nexostrat && sudo chown ricardo:ricardo /srv/Nexostrat`. Same effect for the immediate need, no scope leakage. |
| M1 | Task-range inconsistency: pre-flight says "Tasks 7-11", warm-standby gate + system_map + execution-handoff all say "Tasks 7-12" | `2026-05-14_plan-01b-mirrors.md:24` ("Tasks 7-11") vs `247, 982, 1744` ("Tasks 7-12") | Plan ends at Task 12; the warm-standby cluster is canonically Tasks 7-12 | Single typo at line 24 | MEDIUM | One-word edit: `7-11` → `7-12`. |
| M2 | Task 8 Step 1 apt install combines `docker.io` (Ubuntu/Mint repo) with `docker-compose-plugin` (docker.com-repo-only); not co-installable on stock Mint without first adding docker.com repo | `2026-05-14_plan-01b-mirrors.md:1064` | Linux Mint 22.2 ships `docker.io` (Moby fork from Ubuntu); `docker-compose-plugin` is only available from docker.com's official apt repo, and that repo expects `docker-ce` (not `docker.io`) as the runtime. Mixing causes `apt` to either refuse the install or to uninstall `docker.io` mid-install | Step 1 will fail or surprise the operator on a fresh Mint install. CLAUDE.md backup posture says standby is "Linux Mint 22.2" so the assumption stack is uniform | MEDIUM | Either (a) use `docker.io` + `docker-compose` (both Ubuntu-repo, older but works for Stage 1); or (b) add the docker.com repo as a pre-step and install `docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`. Option (a) is one line shorter and matches "self-host on Mint with no third-party repos" discipline. |
| M3 | Task 11 runbook Step 3 fallback `git pull \|\| git fetch && git reset --hard` has correct precedence but misleading comment | `2026-05-14_plan-01b-mirrors.md:1473-1477` | Bash operator precedence: `A \|\| B && C` parses as `(A \|\| B) && C` — if A succeeds, B and C are both skipped (✓); if A fails and B succeeds, C runs (✓); if A fails and B fails, C is skipped (✓). The comment says "git pull may fail if the standby's clone is behind" — but a *behind* clone is exactly the case `git pull` succeeds on. Pull fails on divergence/conflict, not on being-behind | Behavior is right; explanation is wrong | MEDIUM | Reword comment to: "git pull may fail if the standby's clone has diverged from origin (e.g., local commits during a prior partial failover); hard-reset is safe because the standby is read-only between failovers." Also add explicit `set -e`-style guard or `git fetch origin main` before the reset so the reset target is known to be current. |
| M4 | Task 8 first SSH clone uses `git@gitea-nexostrat:` Tailscale alias but standby has no such alias until the conditional fallback step | `2026-05-14_plan-01b-mirrors.md:1079, 1090-1093` | Standby starts with empty `~/.ssh/config` (fresh Mint install); the Tailscale alias `gitea-nexostrat` lives only in HP's `~/.ssh/config`. Plan attempts clone first (will fail), then provides fallback `scp ~/.ssh/config` ONLY in the "if the clone fails because" branch | Operator hits a confusing SSH error on first clone attempt; the fallback is reactive not proactive | MEDIUM | Hoist the SSH key + config copy BEFORE the clone attempt. Make it Step 2a (or new Step 1.5): "Copy HP's SSH key + config to the standby so the Tailscale alias resolves." Then Step 2's clone works on first try. |
| M5 | Plan 01b makes no acknowledgement of the pre-commit secret-scan hook installed by Plan 01a Task 3; commits in Task 4/5/9 stage `.last-mirror-test` files and unit files that the hook will scan | `2026-05-14_plan-01b-mirrors.md` (no mention); `infra/hooks/pre-commit-secret-scan.sh` exists post-Plan 01a | The hook scans staged blobs, not the disk, so Plan 01b commits should be clean. But Plan 01a's `7e950ee` lesson — "any code embedded literally in plan documentation needs the same secret-safety discipline as the live code" — applies. Plan 01b text uses `<token>` placeholders (line 336, 437) so the plan-text itself won't false-positive. However, operators could accidentally paste a real PAT into the editor opened in Task 2 Step 2 / Task 3 Step 2 and *then* commit the wrong file | MEDIUM. Risk is the operator-mistake path, not the plan-text path | MEDIUM | Add a one-line reminder in Task 2 Step 2 + Task 3 Step 2: "the pre-commit secret-scan hook will catch a PAT pasted into a non-`*.age` file, but do not rely on it — never paste the PAT into shell history or any tracked file other than `secrets.env.age` (which is encrypted before commit)." |
| M6 | Task 1 system_map.md table for `<warm-standby-tbd>` lists `os: Linux Mint 22.2`, conflicting with the broader spec's note that the standby could be any Linux host; minor ambiguity | `2026-05-14_plan-01b-mirrors.md:202` | `infra/machines/hp-standby.yaml:6-7` already pins `os: linux-mint` + `os_version: "22.2"` | Plan and inventory file agree; no real conflict, but the table column is hardcoded which means a future Mint-23 standby would need a plan edit | MEDIUM | Either (a) leave as-is and note "Mint 22.2 LTS — bump when standby is upgraded"; or (b) parameterize in the system_map. (a) is cheaper and Plan 01b is one-shot. |
| M7 | `00_GOVERNANCE/incidents/` is referenced as auto-creating on first incident, but is not pre-created in the scaffold | `2026-05-14_plan-01b-mirrors.md:1547` | `ls /srv/Nexostrat/00_GOVERNANCE/` shows only `adr/` exists post-Plan 01a; no `incidents/` | The runbook says "folder auto-created if missing" — fine, but worth nothing that creating an empty `.gitkeep` ahead of time matches Plan 01a's scaffold pattern for other expected-empty dirs | MEDIUM | Either pre-create `00_GOVERNANCE/incidents/.gitkeep` in Task 1 (cheap, one line), or document the intentional non-creation in a comment. Pre-create is cleaner. |
| L1 | "PathChanged=" used; PathModified vs PathChanged distinction not explained, but PathChanged is the right choice for this use case | `2026-05-14_plan-01b-mirrors.md:609, 824` | systemd.path(5): `PathChanged=` fires when the watched file is closed after being open for writing; `PathModified=` fires on every write. For a git ref update (atomic rename or single write), both work; `PathChanged` is safer (one fire per atomic update) | Correct choice; comment would help future readers | LOW | Add a one-line comment in the path unit explaining the choice. Polish-pass material. |
| L2 | Runbook Step 5 `sed -i.bak` produces a `.bak` file each failover; over time, accumulates `.bak.bak.bak…` if multiple failovers happen | `2026-05-14_plan-01b-mirrors.md:1504` | `sed -i.bak` always creates a `.bak`; running twice with the same input would create `~/.ssh/config.bak.bak` on the second invocation only if you also re-edit `~/.ssh/config.bak`, which doesn't happen here. Mostly cosmetic but worth a note | LOW | Add note: "the `.bak` is the pre-failover config; remove it after the post-restoration step (`docs/runbooks/hp_down.md` Step 7)." |
| L3 | `OnCalendar=*-*-* 03:00:00 America/Tijuana` is correct syntax for systemd 248+, but no test verifies systemd is actually 248+ on the standby pre-install (pre-flight only checks HP) | `2026-05-14_plan-01b-mirrors.md:109-115` (pre-flight) | systemd 248 ships with Ubuntu 22.04+ / Mint 21+; Mint 22.2 has systemd 255 so this is fine — but the warm-rsync timer runs on HP per Task 9's "HP-side", so the standby's systemd version is irrelevant. The pre-flight check is correctly scoped to HP | LOW | None; auditor confirms scoping is right. Worth a single line of clarification: "systemd version check is HP-only because the timer runs on HP." |
| L4 | `--exclude='/dev/shm/'` in warm-rsync.sh is paranoia-only (rsync source path is `/srv/Nexostrat/` so `/dev/shm/` isn't even reachable) | `2026-05-14_plan-01b-mirrors.md:1203` | rsync `--exclude` patterns are relative to the source path unless they start with `/`; the leading `/` here means "literal path /dev/shm/" which is outside the source tree | LOW. Harmless | LOW | Either remove (no-op), or note "defensive — should never match because source is `/srv/Nexostrat/`." |
| L5 | Self-Review section's "Missing items found in self-review — none" is wrong; the partnership-PDF defect (H2) and the SSH-config-case defect (H4) survived self-review | `2026-05-14_plan-01b-mirrors.md:1733` | Findings H2 and H4 demonstrate the self-review missed them. Plan 01a re-audit Finding 8 ("Plan-level success criterion #3 is checked against tasks.json before Task 5 modifies it") was a similar self-review miss class. Pattern: self-review without external eyes catches typos, not architectural drift | LOW. Self-review is a checklist not a guarantee; this is an auditor-vs-self-review observation | LOW | After re-audit patches land, the Self-Review section should append: "(amended post-re-audit 2026-05-16 — H2/H4 corrected)" so the lesson sticks. |

---

## 3. Detailed findings — HIGH

### Finding H1 — Three process-substitution age-decrypt sites violate the Plan-01a direct-`-i` pattern; will fail in TTY-less execution

**Severity:** HIGH
**Lines:** 330, 432, 1118
**Source of truth:** `infra/scripts/run-with-secrets.sh:53-67` (canonical pattern) + commit `7e950ee` (Plan 01a patched 11 sites of this defect 2026-05-16)

**What's wrong:**

All three sites use:
```bash
age -d -i <(age -d ~/.config/age/nexostrat.key.age) <ciphertext>
```

The inner `age -d ~/.config/age/nexostrat.key.age` runs in a subshell whose stdin is the FIFO from process substitution, not the controlling TTY. age 1.1.0+ needs `/dev/tty` to prompt for the passphrase to unwrap a passphrase-encrypted identity file. Inside the subshell, age sees no TTY and fails silently (or with a confusing "decryption failed" error). The outer `age -d -i <FIFO> <ciphertext>` then reads a zero-byte identity and fails.

This is identical to the defect Plan 01a Task 11 surfaced during execution. The fix (commit `7e950ee`) was to use age 1.1.0's documented capability: `age -d -i <passphrase-encrypted-identity-file> <ciphertext>` directly handles the passphrase prompt on its own controlling TTY, no subshell needed. See `infra/scripts/run-with-secrets.sh:57` and the explanatory comment at `:46-55` ("age 1.1.0+ accepts passphrase-encrypted identity files via `-i` directly … One prompt on /dev/tty, no inner subshell. Earlier drafts wrapped the identity through process-substitution `<(age -d "$PRIV_KEY_AGE")`, which breaks under TTY-less execution …").

The hard system audit (2026-05-16) flagged this in "What this audit did NOT cover" item 4, naming exact line numbers.

**Evidence:**
```
$ grep -n "age -d -i <" /srv/Nexostrat/00_META/plans/2026-05-14_plan-01b-mirrors.md
330:age -d -i <(age -d ~/.config/age/nexostrat.key.age) \
432:age -d -i <(age -d ~/.config/age/nexostrat.key.age) \
1118:age -d -i <(age -d ~/.config/age/nexostrat.key.age) \
```

Sites in context:
- Line 330 — Task 2 Step 2 (add `GITHUB_MIRROR_PAT` to `secrets.env.age`)
- Line 432 — Task 3 Step 2 (add `CODEBERG_MIRROR_PAT` to `secrets.env.age`)
- Line 1118 — Task 8 Step 4 (standby decrypt-roundtrip test — but see Finding H2: the target file also doesn't exist)

**Why it matters:** Tasks 2 and 3 are gating steps for the entire mirror cluster. If the operator runs Plan 01b under any non-interactive harness (subagent-driven-development with stdin redirected, scripted execution, agentic tools), Steps 2/3 fail before any commit can happen. Even in interactive use, the failure mode is confusing (the inner age fails silently, the outer age reports a generic decryption error).

**Recommendation:** Mechanical patch at all 3 sites:
```bash
# Before:
age -d -i <(age -d ~/.config/age/nexostrat.key.age) \
    /srv/Nexostrat/secrets.env.age > "$TMP"

# After (mirroring run-with-secrets.sh:57):
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/secrets.env.age > "$TMP"
```

Apply identically at lines 330, 432, 1118. (Note: line 1118's target file is also broken — see H2 — so this patch and H2's patch land together.)

**Effort:** 5 minutes total (3 mechanical substitutions; same pattern as `7e950ee`).

---

### Finding H2 — Task 8 Step 4 decrypt-roundtrip targets a partnership PDF that does not and never will exist

**Severity:** HIGH
**Lines:** 1116-1126

**What's wrong:**

```bash
# Plan 01b Task 8 Step 4 (line 1116-1126):
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
TMP=/dev/shm/agreement-test-$$.pdf
age -d -i <(age -d ~/.config/age/nexostrat.key.age) \
    /srv/Nexostrat/vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age \
    > "$TMP"
file "$TMP"
shred -u "$TMP"
EOF
)"
```

The decrypt target `vault/partnership/PARTNERSHIP_AGREEMENT_2026-05-12.pdf.age` does not exist in the repo and was intentionally never created. Commit `acdcc4a` ("Plan 01a Task 17 reframed · PARTNERSHIP_AGREEMENT.md (markdown is the agreement)") removed the PDF-encrypt step entirely. The commit message reads: *"Brothers-as-partners do not need a notarized PDF at Stage 1. Skip the vault/partnership PDF encrypt + the sensitive_index row that the original Task 17 plan prescribed. The markdown summary IS the canonical agreement."*

**Evidence:**
```
$ find /srv/Nexostrat/vault -type f
/srv/Nexostrat/vault/README.md
/srv/Nexostrat/vault/sensitive_index.md
/srv/Nexostrat/vault/accounting/.gitkeep
/srv/Nexostrat/vault/clients/.gitkeep
/srv/Nexostrat/vault/partnership/.gitkeep    # ← only this; no PDF
/srv/Nexostrat/vault/keys/.gitkeep
/srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age
/srv/Nexostrat/vault/legal/.gitkeep

$ cat /srv/Nexostrat/00_PARTNERSHIP/PARTNERSHIP_AGREEMENT.md | grep -i "form of agreement\|PDF"
> artifact exists. Formality (signed PDF, notarization, registered entity) returns at the
**Form of agreement:** plain markdown (no notarized PDF; brothers-as-partners — see top blockquote)
```

**Why it matters:** Task 8 Step 4 is the **only crypto round-trip validation** in Plan 01b — its purpose is to confirm the standby has a working age key that can read encrypted vault content. If the target file doesn't exist, the test fails for the wrong reason ("file not found") and the operator must debug a phantom defect before realizing the plan's premise is wrong. Plan 01b would block partway through Task 8 with no clean diagnosis.

This is also a meta-finding: the plan was written 2026-05-14, the partnership-PDF was reframed 2026-05-16 in commit `acdcc4a`. Plan 01b never got the memo. Suggests a need for a plan-review step after any architectural decision lands ("does this break any deferred-plan assumption?").

**Recommendation:** Replace the decrypt target with one that actually exists. Two options, ranked:

**Option A (preferred):** Decrypt `secrets.env.age` and check sentinel content:
```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
TMP=/dev/shm/secrets-roundtrip-$$
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/secrets.env.age > "$TMP"
# Sanity check — secrets.env.age should contain known variable names
grep -q "^GITHUB_MIRROR_PAT=" "$TMP" && echo "OK: standby decrypted secrets.env.age"
shred -u "$TMP"
EOF
)"
```
Rationale: (a) tests the actual crypto pipeline used by every service, (b) proves the standby's age key matches both recipients, (c) no fake artifact needed.

**Option B (acceptable):** Decrypt `vault/keys/sentinel-ricardo-to-jp.age`:
```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
TMP=/dev/shm/sentinel-roundtrip-$$
age -d -i ~/.config/age/nexostrat.key.age \
    /srv/Nexostrat/vault/keys/sentinel-ricardo-to-jp.age > "$TMP"
file "$TMP"   # expect ASCII text
shred -u "$TMP"
EOF
)"
```
Rationale: this is the file's intended purpose (recipient-roundtrip verification per Plan 01a Task 13). Caveat: the sentinel itself is scheduled for cleanup once `t-plan-01a-jp-and-tty-deferred` closes; long-term, Option A is more durable.

Bundle the H1 fix into the same patch.

**Effort:** 10 minutes (rewrite Task 8 Step 4; pick Option A or B; verify the chosen target exists in the v0.1a tree).

---

### Finding H3 — Signal references inside Nexostrat-internal runbook violate the 2026-05-16 Telegram-only directive

**Severity:** HIGH
**Lines:** 1525, 1610

**What's wrong:**

Two locations in `docs/runbooks/hp_down.md` (written by Task 11) mention Signal as the failover notification channel:

```
Line 1525:  Until Plan 04 is live, send a Signal message to JP manually:
            "Failover complete. Standby active at <IP>. ..."

Line 1610:  6. Notify (Signal manual; Plan 04 will Telegram-automate)
```

Per the 2026-05-16 directive (CLAUDE.md context for this audit + project memory at `/home/ricardo/.claude/projects/-srv-Nexostrat/memory/`): "Nexostrat's coordination channel is Telegram only; Signal is Ricardo's personal-only channel and must not appear in Nexostrat artifacts."

Note the subtlety: Signal is fine for Ricardo↔JP coordination per CLAUDE.md ("External coordination: Ricardo ↔ JP: Signal messages (async)"). The constraint is that Nexostrat documented procedures should not specify Signal as the canonical channel — that's Telegram (Plan 04+).

**Evidence:**
```
$ grep -n -i "signal" /srv/Nexostrat/00_META/plans/2026-05-14_plan-01b-mirrors.md
1525:Until Plan 04 is live, send a Signal message to JP manually:
1610:6. Notify (Signal manual; Plan 04 will Telegram-automate)
```

**Why it matters:** The hard system audit (2026-05-16) flagged Telegram-vs-Signal as one of the "load-bearing operator-facing surfaces" that should be cleaned in the pre-Plan-01b sweep. The runbook is exactly that kind of surface — it will be read at a stressful moment (HP is down) and inconsistency between artifact and directive will cost time + confidence.

**Recommendation:** Reword both sites to remove "Signal" as the named channel:

Line 1525 — change:
```
Until Plan 04 is live, send a Signal message to JP manually:
"Failover complete. Standby active at <IP>. ..."
```
to:
```
Until Plan 04's Telegram bot is live, notify JP via the agreed personal
channel (out of band — not specified in this runbook). Message template:
"Failover complete. Standby active at <IP>. ..."
```

Line 1610 — change:
```
6. Notify (Signal manual; Plan 04 will Telegram-automate)
```
to:
```
6. Notify (manual, out-of-band; Plan 04 will Telegram-automate)
```

**Effort:** 3 minutes (two text edits).

---

### Finding H4 — HP-down runbook DNS-swap `sed` pattern will never match — case mismatch with actual SSH config syntax

**Severity:** HIGH
**Lines:** 1502-1507

**What's wrong:**

The runbook Step 5 prescribes:
```bash
sed -i.bak \
  -e 's/Hostname 100.64.121.80/Hostname <STANDBY_TAILSCALE_IP>/' \
  ~/.ssh/config
```

But OpenSSH config files use `HostName` (camelcase) per `ssh_config(5)`. Verified on the current HP:
```
$ grep -nE "HostName|Hostname" ~/.ssh/config
20:  HostName 100.64.121.80
```
No occurrences of lowercase `Hostname`. The sed expression will produce zero substitutions, `.bak` will be byte-identical to the original, and SSH continues to resolve `gitea-nexostrat` to HP's IP. Failover is silently broken at this step.

**Why it matters:** This step is on the recovery critical path. RTO target is 15-30 min; a silently failed DNS swap means the operator notices "but I can't push to gitea-nexostrat" several minutes later, then debugs the sed pattern under stress. Worse, if the runbook reader doesn't realize sed failed (no error code; `sed -i` reports nothing on zero substitutions), they may move on to Step 6 and "complete" the runbook with the failover only half-working.

This is the same class of defect as the Plan 01a Finding 4 ("Task 17 Step 1 uses tilde inside double quotes; path will not expand") — a syntax-level slip in a step that's load-bearing under stress.

**Recommendation:** Two-part fix:

1. **Correct the pattern** — case-insensitive matcher that handles both forms:
   ```bash
   sed -i.bak -E \
     -e 's/^([Hh]ost[Nn]ame)[[:space:]]+100\.64\.121\.80/\1 <STANDBY_TAILSCALE_IP>/' \
     ~/.ssh/config
   ```

2. **Add a post-check** to make the failure loud:
   ```bash
   if ! grep -q "HostName <STANDBY_TAILSCALE_IP>" ~/.ssh/config 2>/dev/null && \
      ! grep -q "Hostname <STANDBY_TAILSCALE_IP>" ~/.ssh/config 2>/dev/null; then
     echo "ERROR: sed produced no substitution — DNS swap did NOT happen" >&2
     echo "       Manually edit ~/.ssh/config to point gitea-nexostrat at <STANDBY_TAILSCALE_IP>" >&2
     exit 1
   fi
   ```

Better still: include the exact pre-substitution + post-substitution snippet in the runbook so the operator can eyeball-verify.

**Effort:** 10 minutes (rewrite the runbook block + smoke-test the sed against a copy of `~/.ssh/config`).

---

### Finding H5 — Task 8 Step 2 `sudo chown ricardo:ricardo /srv` is FHS-incorrect; risk of cross-service ownership collision

**Severity:** HIGH (borderline MEDIUM — see "why it matters")
**Lines:** 1076

**What's wrong:**

```bash
ssh ricardo@<standby> bash -c "$(cat <<'EOF'
sudo mkdir -p /srv && sudo chown ricardo:ricardo /srv
cd /srv
git clone git@gitea-nexostrat:nexostrat/nexostrat.git Nexostrat
EOF
)"
```

The chown changes `/srv` itself (non-recursive — there's no `-R`, so it only affects the directory inode, not its contents). Two concerns:

1. **FHS posture:** `/srv` should be `root:root 0755` per the Filesystem Hierarchy Standard. Service-specific subdirs (e.g., `/srv/Nexostrat`) can be owned by the service operator. Owning `/srv` itself by `ricardo:ricardo` is non-standard and could trip up other init/installer scripts that expect root ownership.

2. **Cross-service collision risk:** On HP, `/srv` contains `atten-bot`, `brain`, `brain-sensitive-mount`, `gitea`, `Nexostrat`. If the standby ever takes on a similar multi-service role (e.g., as a failover target for AttenBot too), the ricardo-owned `/srv` parent could cause permission surprises when those services try to write their own subdirs.

The fix is trivially scoped: `chown ricardo:ricardo /srv/Nexostrat`, not `/srv`.

**Why it matters:** Today the standby is a single-purpose Nexostrat failover host so the immediate impact is zero. The finding is HIGH because: (a) it's a one-character fix with zero downside, (b) leaving it as-is normalizes a non-FHS pattern that will compound if more services land on the standby later, (c) the hard audit's "do it right, do it once" memory rule points away from cutting corners on infrastructure ownership.

**Evidence:**
```
$ ls /srv/ | head -5
atten-bot
brain
brain-sensitive-mount
gitea
Nexostrat
```
(HP layout; standby will end up similarly diverse over time.)

**Recommendation:** Change line 1076 from:
```bash
sudo mkdir -p /srv && sudo chown ricardo:ricardo /srv
```
to:
```bash
sudo mkdir -p /srv/Nexostrat && sudo chown ricardo:ricardo /srv/Nexostrat
```

If `/srv` doesn't exist yet on a brand-new Mint install, the `mkdir -p /srv/Nexostrat` creates `/srv` with default ownership (`root:root`) and then creates `/srv/Nexostrat` owned by root too — the explicit `chown` only flips `/srv/Nexostrat`. Clean.

**Effort:** 2 minutes.

---

## 4. Deferred findings appendix — MEDIUM and LOW

**M1 (task-range typo, line 24):** Plan line 24 says "Tasks 7-11"; should be "Tasks 7-12". Single-word edit. Bundle with other patches.

**M2 (docker.io + docker-compose-plugin coexistence, line 1064):** Stock Linux Mint 22.2 ships `docker.io` from the Ubuntu repo; `docker-compose-plugin` is only available from docker.com's official apt repo and expects `docker-ce`, not `docker.io`. Either use `docker.io` + `docker-compose` (both Ubuntu-repo) for Stage 1 simplicity, or add the docker.com repo as an explicit pre-step. Recommend the former for consistency with "self-hosted on stock Mint" minimalism.

**M3 (runbook Step 3 pull/reset comment, lines 1473-1477):** The bash precedence `A || B && C` parses as `(A || B) && C` — correct behavior, but the comment ("git pull may fail if the standby's clone is behind") describes the wrong failure mode. A *behind* clone causes pull to succeed; pull fails on *divergence*. Reword the comment to match reality.

**M4 (Task 8 SSH config bootstrap ordering, lines 1079/1090-1093):** The clone command uses `git@gitea-nexostrat:` (a Tailscale SSH alias defined only in HP's `~/.ssh/config`), but the fallback `scp ~/.ssh/config` step is in a conditional "if the clone fails" branch. Operator hits a confusing error on first attempt. Hoist the SSH key + config copy to BEFORE the clone attempt.

**M5 (no secret-scan-hook acknowledgement):** Plan 01b makes no mention of the pre-commit secret-scan hook installed by Plan 01a Task 3. The plan-text itself uses `<token>` placeholders so it won't false-positive, but Task 2 Step 2 / Task 3 Step 2 open `nano` on a `/dev/shm` plaintext — if the operator typoed and pasted the PAT into a tracked file by mistake, the hook would catch it, but the plan should remind: "do not paste the PAT into shell history or any tracked file other than the temporary plaintext."

**M6 (system_map.md hardcoded Mint 22.2):** Task 1's system_map.md table pins the standby's `OS` column to `Linux Mint 22.2`. Matches `infra/machines/hp-standby.yaml` (which also pins 22.2). Future-Mint upgrade would require both files to be touched. Stage 1 is fine; just flag the coupling.

**M7 (`00_GOVERNANCE/incidents/` not pre-created):** Runbook Step 8 (line 1547) says the folder is auto-created on first use, but Plan 01a's pattern is to pre-create empty dirs with `.gitkeep`. Inconsistency. Cheap fix: pre-create in Task 1 (with `incidents/.gitkeep` + a one-line README explaining the format).

**L1 (PathChanged choice unexplained, lines 609 + 824):** The correct choice for git ref updates, but a one-line `# PathChanged fires once per atomic ref-update, vs PathModified which fires per-write` comment would help future readers. Polish material.

**L2 (sed -i.bak accumulation, line 1504):** After several failovers, multiple `.bak` files could pile up in `~/.ssh/config*`. Add a cleanup note in runbook Step 7 (post-restoration): `rm ~/.ssh/config.bak`.

**L3 (systemd 248+ scoped only to HP):** Pre-flight checks systemd version on HP but not on standby. The warm-rsync timer runs on HP, so this is correctly scoped. One line of clarification in the pre-flight section would prevent future audit confusion.

**L4 (`--exclude='/dev/shm/'` in warm-rsync, line 1203):** Rsync `--exclude` patterns are relative to source unless leading-`/`. The `/dev/shm/` exclude is outside the source tree and can never match. Harmless defensive code; note as such or remove.

**L5 (Self-Review section claims "missing items: none"):** H2 and H4 both demonstrate self-review missed real defects. Suggest appending "(amended post-re-audit YYYY-MM-DD)" to the Self-Review block after patches land so future readers see the lesson.

---

## 5. Production-readiness assessment

If Plan 01b is patched per Findings H1-H5 and executed cleanly, does the `v0.1b-mirrors` tag tree deliver the backup posture promised in CLAUDE.md § Backup Posture?

**What WILL be delivered:**

- Gitea origin → GitHub mirror via systemd `.path` + `.service` (event-driven; 60s window verified end-to-end).
- Gitea origin → Codeberg mirror, same pattern.
- Standby host with: full clone, age key installed, working decrypt round-trip (post-H2 patch), Docker images pre-pulled, SSH from HP works key-based.
- Nightly warm-rsync at 03:00 America/Tijuana (Persistent=true, RandomizedDelaySec=300).
- Real `systemctl start && verify status=0/SUCCESS` smoke test (F24 closure, not the false-positive `--dry-run`).
- HP-down failover runbook with dry-run validation, RTO 15-30 min achievable (post-H4 patch).
- `00_GOVERNANCE/system_map.md` as the running "where things live" reference.

**Hidden gaps relative to CLAUDE.md § Backup Posture:**

1. **Drive 2TB heavy-asset flow** — CLAUDE.md backup ladder mentions "Drive 2TB (heavy assets, age-encrypted before upload)" and "NAS rclone mirror (when NAS comes online)." Plan 01b does not touch these. Per CLAUDE.md "Known gaps (current state)" — this is explicitly Plan 01a-or-later territory. No new defect here; just confirming Plan 01b's scope ends before the Drive layer.

2. **No periodic mirror-health monitor** — Plan 01b validates mirror latency at install time, then trusts the systemd path-watcher to keep working. A silently-failing mirror (e.g., GitHub revokes the SSH key, Codeberg account locked) would not be caught until the next manual `git fetch github` or until someone reads `journalctl -u nexostrat-mirror-*.service`. CLAUDE.md says "Verification cadence: integration smoke test (Plan 01c) does real decrypt round-trip + real `git push` + verify GitHub HEAD changed. After that, periodic verification per a yet-undefined schedule (Plan 10 territory)." So this gap is explicitly Plan 10. Not a Plan 01b defect; flag only.

3. **No mirror-retention monitoring** — GitHub free org has no inactive-account expiry; Codeberg free has a no-activity expiry policy (community-style soft warning then suspension after ~12mo of total inactivity). The mirror pushes themselves keep the account active, so this is not a near-term concern. Worth a single Plan 10 note.

4. **Standby's age key has the same passphrase as HP's** — Plan 01b Task 8 Step 3 copies the encrypted private key to the standby. If HP's age key is ever rotated (Plan 10 territory), the standby key must be re-copied. No automation. Flag for Plan 10.

5. **Warm-rsync is push-only from HP** — if HP's network is up but HP itself is broken (e.g., kernel panic on filesystem), the standby can't pull. A pull-style rsync from standby would be more resilient. CLAUDE.md backup ladder doesn't specify push vs pull; current plan is push. Worth a note for Plan 02 or 10 to revisit.

**Overall:** Post-patch Plan 01b delivers the Stage 1 backup posture as advertised. None of the hidden gaps block Stage 1 launch (2026-07-15 to 2026-07-30); they're Plan 10 (observability + go-live) territory.

---

## 6. Recommended actions

### (a) Patch inline before Plan 01b execution starts (HIGH; total ~30 min)

Apply all 5 HIGH findings as direct in-place edits to `00_META/plans/2026-05-14_plan-01b-mirrors.md`:

- **H1** — 3 mechanical substitutions: `age -d -i <(age -d $KEY) $CT` → `age -d -i $KEY $CT` at lines 330, 432, 1118.
- **H2** — Task 8 Step 4 (lines 1116-1126): replace the partnership-PDF decrypt with the Option A pattern (decrypt `secrets.env.age`, grep for known variable name, shred). Bundles with H1's patch at line 1118.
- **H3** — Two text edits at lines 1525, 1610: remove "Signal" as the named channel; replace with "out-of-band personal channel" or equivalent.
- **H4** — Runbook Step 5 (lines 1502-1507): correct `Hostname` → `HostName` in the sed pattern; add a post-substitution `grep` check that errors if zero substitutions happened.
- **H5** — Line 1076: change `chown ricardo:ricardo /srv` to `mkdir -p /srv/Nexostrat && chown ricardo:ricardo /srv/Nexostrat`.

After all 5 edits land in a single commit, Plan 01b is execute-ready. Suggested commit message:
```
Plan 01b re-audit patches · H1-H5 closed in single pass

H1: 3 process-sub age-decrypt sites → direct -i (lines 330, 432, 1118)
H2: Task 8 Step 4 decrypt target → secrets.env.age (PDF artifact reframed away)
H3: Runbook Signal references → out-of-band personal channel
H4: Runbook sed pattern Hostname → HostName (case fix) + post-check
H5: chown /srv → chown /srv/Nexostrat (FHS-correct scope)

Re-audit report: 00_META/proposals/2026-05-16_plan-01b-reaudit-report.md
```

### (b) Bundle into a single follow-up amendment commit (MEDIUM; ~1 hour, optional)

Either patch in the same commit as (a) above, or write a small `t-plan-01b-text-amendments` task closed before execution:

- **M1** — Line 24 task range `7-11` → `7-12`.
- **M2** — Line 1064 apt-install simplified to `docker.io docker-compose` (Ubuntu-repo-only, no docker.com repo dependency).
- **M3** — Runbook Step 3 comment reworded (divergence, not behind).
- **M4** — Task 8 Step 2: hoist `scp ~/.ssh/config + nexostrat_ed25519` before the clone attempt.
- **M5** — Task 2 Step 2 + Task 3 Step 2: one-line reminder about the secret-scan hook scope.
- **M6** — Note the Mint 22.2 hardcode in system_map.md or the standby YAML.
- **M7** — Pre-create `00_GOVERNANCE/incidents/.gitkeep` in Task 1.

These are cheap and the operator-experience improvement is real, but none of them block execution. Recommend bundling them with (a) if Ricardo wants a single clean patch commit.

### (c) Track as new tasks (none required)

No new tasks needed — H1-H5 + M1-M7 are all patchable inline. The production-readiness gaps in §5 (Drive flow, mirror-health monitor, account-expiry monitor, key-rotation propagation, push-vs-pull rsync) are already tracked-or-implicit in Plan 10's scope.

### (d) Polish-pass material (post-Plan-01c)

L1-L5: code-comment polish, sed-i.bak cleanup note, self-review-honesty edit. Bundle into the canonical-shared-stanzas pass that Plan 01c will need for `00_META/shared/*.md` polish.

---

## 7. What this audit did NOT cover

Honest scope gaps the auditor cannot verify from a read-only seat:

1. **Live systemd `.path` unit behavior** — auditor cannot confirm that `PathChanged=/srv/gitea/data/git/repositories/nexostrat/nexostrat.git/refs/heads/main` actually fires reliably on every Gitea push without `sudo` privileges to install the unit and trigger a test push. systemd documentation supports the design; real behavior depends on filesystem-event timing (rename-vs-write semantics under Gitea's specific commit handling). **Recommendation:** during Plan 01b Task 4 execution, the very first wire-up test (Step 6) IS the validation — if it fires, the design holds.

2. **GitHub/Codeberg side behavior** — auditor cannot test `git push` to either remote without provider credentials. Assumes Ricardo's terrain-prep work (SSH keys registered, accounts exist) holds. Plan 01b's pre-flight checks (lines 83-103) cover this.

3. **rsync `--info=stats2` output format on standby OS** — auditor confirmed `rsync` is available on HP (per CLAUDE.md baseline); standby is Linux Mint 22.2 per `infra/machines/hp-standby.yaml`, so format should match. Validation happens in Task 10 Step 3.

4. **Tailscale connectivity from HP to a not-yet-provisioned standby** — Task 7 first-step is exactly this validation. Audit confirms the plan checks the right thing at the right time.

5. **Gitea version-specific behavior** — Gitea version not pinned in `infra/machines/hp-server.yaml`; auditor confirmed Gitea container is running (`docker ps` shows it) but did not verify the bare-repo HEAD-write pattern matches what the systemd `.path` unit expects. Task 4 Step 6 (the wire-up test) covers this empirically.

6. **The post-Plan-01b state of `vault/keys/sentinel-ricardo-to-jp.age`** — hard audit's H5 deferral notes this file may still be at HEAD when Plan 01b executes, in which case warm-rsync will replicate it to the standby. Plan 01b's Task 8 Step 4 (H2-patched per this audit) will pass either way; the sentinel cleanup is a separate flow tracked in `t-plan-01a-jp-and-tty-deferred`.

7. **`docker compose` plugin command-vs-binary** — Plan 01b uses `docker compose` (space) throughout, which requires the Compose v2 plugin. On stock Linux Mint without docker.com's repo, `docker-compose` (hyphen) v1 is what comes with `docker.io`. This intersects with Finding M2. Auditor flagged but did not run the actual install.

---

*End of Plan 01b re-audit report. Sibling priors: `2026-05-14_audit-report.md` (founding spec), `2026-05-14_plan-01a-audit-report.md` (Plan 01a re-audit, 7H all patched), `2026-05-16_hard-system-audit-report.md` (5H/9M/6L hard audit at v0.1a-foundation, all HIGH+MEDIUM patched same-session). This audit's 5 HIGH should follow the same patch-in-session pattern.*
