# Plan 01a — Patch Verification Trail

> **Created:** 2026-05-14 (Batch 3 step 1, end of session)
> **Purpose:** Forensic-friendly companion to the Plan 01a re-audit. Per-finding, this doc shows **what was wrong**, **what's there now**, and **how a future auditor can independently verify the fix is live**. Pairs with — does not replace — the adversarial audit report.
> **Reading order:** start with the audit report ([`2026-05-14_plan-01a-audit-report.md`](2026-05-14_plan-01a-audit-report.md)); then for each HIGH finding, jump to the matching section below.
>
> **Companion artifacts:**
> - Audit report (the adversarial finding): [`2026-05-14_plan-01a-audit-report.md`](2026-05-14_plan-01a-audit-report.md)
> - Patched plan (the artifact the fixes live in): [`../plans/2026-05-14_plan-01a-foundation.md`](../plans/2026-05-14_plan-01a-foundation.md)
> - Commit landing all patches: `6ca022c` ("Plan 01a re-audit (Batch 3 step 1) + 7 HIGH inline patches")
> - Session journal: `../journal/2026-05-14_plan-01a-reaudit-and-patches.md`
>
> **Note for a future auditor:** if you are running a follow-up audit of Plan 01a, the workflow Ricardo + Claude followed was:
>   1. Audit by independent risk-auditor (this session's artifact: the audit report)
>   2. Verdict: YELLOW (large) — 0 CRITICAL, 7 HIGH, 5 MEDIUM, 3 LOW, no DESIGN-RETHINK FLAG.
>   3. Decision: surgical inline patches (auditor's own recommended path; matches the spirit of the >3-HIGH rewrite rule because each fix is task-scoped, not architectural).
>   4. Trail (this doc) records every fix so you can re-verify.
> A clean re-audit should find: zero HIGH defects matching findings 1-7; the patches themselves are correct; possible new defects introduced by the patches (unknown unknown — please look).

## Verdict + counts

| Severity | Count | Status |
|---|---:|---|
| CRITICAL | 0 | (none found) |
| HIGH | 7 | **All patched inline.** See trail per-finding below. |
| MEDIUM | 5 | Deferred per auditor recommendation. Listed in § Deferred findings. |
| LOW | 3 | Deferred per auditor recommendation. Listed in § Deferred findings. |
| **Total** | **15** | — |

DESIGN-RETHINK FLAG: **not triggered** (auditor's own assessment). Architecture is sound; defects local.

## Summary index — 7 HIGH patches

| # | Severity | Subject | Audit report ref | Patch location in plan | Verification command |
|---:|:---|:---|:---|:---|:---|
| 1 | HIGH | `*secrets*` glob blocks `secrets.env.age` + MANIFEST.md | report §"Finding 1" | plan lines 379-400 + Step 5b lines 486-504 | `cd /srv/Nexostrat && git check-ignore -q secrets.env.age \|\| echo OK`; expect `OK` |
| 2 | HIGH | C1 leak-test false PASS via passphrase hang | report §"Finding 2" | plan lines 2820-2916 | run `bash infra/scripts/test_run_with_secrets_no_leak.sh` (interactive); expect both PASS lines |
| 3 | HIGH | Secret-scan hook scans on-disk, not staged blob | report §"Finding 3" | plan lines 624-660 (hook) + 715-744 (Step 6b) | run Plan 01a Task 3 Step 6b stage-then-edit test; expect `PASS — hook blocked commit based on staged-blob content` |
| 4 | HIGH | `SIGNED_PDF="~/Downloads/..."` tilde does not expand | report §"Finding 4" | plan line 3192 | `bash -c 'V="$HOME/x"; ls "$V" 2>&1' \| head -1`; expect path-not-found error referencing `/home/...`, not literal `~` |
| 5 | HIGH | `git add 00_META/skills` after `rmdir` errors fatal | report §"Finding 5" | plan lines 1583-1589 | `grep -n 'git add 00_META/skills' …plan…`; expect match only in audit-response note (line 32), NOT in any task body |
| 6 | HIGH | C2 reverse-direction roundtrip underspecified | report §"Finding 6" | plan lines 2641-2718 | run Plan 01a Task 13 Step 3 Direction A + Direction B; both must succeed |
| 7 | HIGH | `run-with-secrets.sh` `2>/dev/null` swallows age errors | report §"Finding 7" | plan lines 2980-2992 | manually trigger wrapper with deliberately-wrong passphrase; expect captured `age stderr:` block in stderr output |

Line numbers above are **post-patch** (current `HEAD`). The audit report's line numbers are **pre-patch** (the version that was audited).

---

## Finding 1 — gitignore `*secrets*` glob blocks intentional commits

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 1" (search for "Finding 1 — `.gitignore` pattern").
**Plan location post-patch:** Task 2 Step 3 lines 379-400 (the gitignore content) + Step 5b lines 486-504 (positive `git check-ignore` assertion) + Step 1 test additions around line 329.

### What was wrong

The original `.gitignore` payload (Task 2 Step 3, pre-patch) included:

```
*secrets*
secrets.env
```

The leading no-slash `*secrets*` matches at any path depth per gitignore semantics. Verified empirically by the auditor:
```
$ git check-ignore -v infra/secrets/MANIFEST.md
.gitignore:1:*secrets*	infra/secrets/MANIFEST.md
$ git check-ignore -v secrets.env.age
.gitignore:1:*secrets*	secrets.env.age
```
Result: Tasks 14 (`git add secrets.env.age`) and 16 (`git add infra/secrets/MANIFEST.md`) would silently no-op the `git add`, then commit empty staged sets. `v0.1a-foundation` tag would point at a state missing both files.

### What's there now (post-patch, plan lines 379-400)

```
# Surgical secret patterns — DO NOT use a blanket `*secrets*` glob (per Finding 1
# of the 2026-05-14 re-audit): it would silently block the intentional commits
# of secrets.env.age (Task 14) and infra/secrets/MANIFEST.md (Task 16).
secrets.env
secrets.env.local
secrets.local.env
*.secrets.json
**/secrets.env
**/secrets.local.env
*.key
*.pem
*.pfx
*.p12
key.txt
infra/age/keys/

# Explicit allowlist — these MUST be committable despite the patterns above.
!secrets.env.age
!infra/secrets/MANIFEST.md
```

Plus a new **Step 5b** that runs `git check-ignore -q` against the two allowlisted paths and FAILs if either is ignored. Plus an update to the coverage test (`infra/scripts/test_gitignore_coverage.sh`) that asserts the surgical pattern AND the allowlist:

```bash
check "Age password files"    'secrets\.env$|\*\*/secrets\.env|\*\.secrets\.json'
check "Allowlist secrets.env.age"      '^!secrets\.env\.age'
check "Allowlist secrets MANIFEST.md"  '^!infra/secrets/MANIFEST\.md'
```

### How a future auditor verifies the fix

After Plan 01a Task 2 has executed (i.e. after the patched `.gitignore` is on disk), run:

```bash
cd /srv/Nexostrat
# 1. The blanket *secrets* glob must NOT be present
grep -c '^\*secrets\*$' .gitignore
# Expected: 0

# 2. Both allowlist lines must be present
grep -c '^!secrets\.env\.age$' .gitignore                      # expect 1
grep -c '^!infra/secrets/MANIFEST\.md$' .gitignore             # expect 1

# 3. Live positive control — the two intentional paths must NOT be ignored
for p in secrets.env.age infra/secrets/MANIFEST.md; do
  git check-ignore -q "$p" && echo "FAIL ignored: $p" || echo "OK not-ignored: $p"
done
# Expected: both lines say "OK not-ignored"
```

If any check fails, the gitignore patch regressed and Tasks 14/16 will produce empty commits.

---

## Finding 2 — C1 leak-detection test false PASS via passphrase hang

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 2" (search for "false PASS; does not actually test C1").
**Plan location post-patch:** Task 15 Step 1 lines 2820-2916 (test script body) + updated Step 4 expected output (~line 3030) + reworked Step 5 manual smoke (~line 3043).

### What was wrong

The pre-patch test backgrounded the wrapper (`"$WRAPPER" sh -c 'sleep 60' &`) then checked `/dev/shm` after 2 seconds. But the wrapper's inner `age -d` (decrypting the passphrase-encrypted private key) reads `/dev/tty` for the passphrase. The backgrounded process blocks indefinitely on that prompt before reaching the `> "$PT"` write. At T+2s, no plaintext file exists yet — so `LEAKED=0` and the test prints "PASS — no leak". The wrapper could leak catastrophically and this test would still pass.

Secondary defects: the standalone positive-sourcing block had no assertion; `pkill -P $WRAPPER_PID` targeted a dead parent's children; the pre-condition `rm -f /dev/shm/nexostrat-secrets-*` silently nuked any concurrent legitimate session.

### What's there now (post-patch, plan lines 2820-2916)

The test is now a poll-based interactive protocol:

1. **Snapshot** existing `/dev/shm/nexostrat-secrets-*` files (preserve concurrent sessions — no global `rm -f`).
2. Background the wrapper around `sleep 20`.
3. **Poll** for a NEW file (set-difference vs snapshot) with a 30-second deadline. The poll keeps `kill -0` checking the wrapper PID so it bails fast if the wrapper died (e.g. decrypt failure).
4. **Positive control:** once a new file appears, print PASS. (If poll deadline expires, FAIL with diagnostic.)
5. Kill the wrapper, wait, sleep 1s.
6. **Negative control:** check the SPECIFIC observed file path is gone. PASS if gone; FAIL if still present (C1 cleanup did not fire).

This forces real exercise of the C1 cleanup pathway: the file must be observed to exist (proving the wrapper got past the passphrase prompt and wrote the plaintext) and must be observed to disappear (proving the trap fired).

### How a future auditor verifies the fix

```bash
# 1. The buggy 2s-sleep pattern must NOT be present anywhere
grep -n 'sleep 2$' /srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh
# Expected: no match (after Plan 01a Task 15 executed)

# 2. The poll-based design markers must be present
grep -c 'POLL_DEADLINE_SECS\|positive control\|negative control' \
  /srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh
# Expected: >= 3

# 3. Run the test — must require interactive passphrase entry AND emit both PASS lines
bash /srv/Nexostrat/infra/scripts/test_run_with_secrets_no_leak.sh
# Expected stdout includes:
#   PASS — wrapper created /dev/shm/nexostrat-secrets-<pid> during execution (positive control)
#   PASS — /dev/shm/nexostrat-secrets-<pid> removed after wrapper exit (negative control — C1 cleanup verified)
```

If the test exits 0 WITHOUT the human entering a passphrase, that's the old false-PASS bug returning — investigate.

---

## Finding 3 — Pre-commit secret-scan hook scans on-disk, not staged blob

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 3" (search for "scans the on-disk file, not the staged blob").
**Plan location post-patch:** Task 3 Step 3 lines 624-660 (hook body) + Step 6b lines 715-744 (stage-then-edit integration test).

### What was wrong

Pre-patch hook iterated `git diff --cached --name-only` to get staged paths, then `grep`ed each as an on-disk path. Stage-vs-disk divergence (user stages a file with a secret, then edits the on-disk copy clean before commit) would slip the secret into history because the on-disk content was clean by the time the hook ran. The plan's own integration test couldn't catch this because it staged + committed in the same step (on-disk == staged).

### What's there now (post-patch, plan lines 624-660)

The hook now branches on mode:

```bash
MODE="git-hook"
if [[ "${1:-}" == "--files-from-stdin" ]]; then
  MODE="stdin"
  mapfile -t FILES < <(cat)
else
  mapfile -t FILES < <(git diff --cached --name-only --diff-filter=ACMR)
fi
# ...
for f in "${FILES[@]}"; do
  # ...
  if [[ "$MODE" == "git-hook" ]]; then
    # Read the staged blob. Skip silently if blob unavailable (e.g. deleted path).
    if blob=$(git show ":$f" 2>/dev/null); then
      if printf '%s' "$blob" | scan_content "$f"; then
        violations=$((violations+1))
      fi
    fi
  else
    # stdin mode — scan disk file directly
    [[ -f "$f" ]] || continue
    if grep -EHn "$PATTERNS" "$f" 2>/dev/null; then
      violations=$((violations+1))
    fi
  fi
done
```

`--files-from-stdin` mode (unit-test harness) keeps the on-disk read because the test creates files outside any git index. Real git-hook mode reads `git show :"$f"` — the staged blob — which is what actually enters the repository.

New **Step 6b** (lines 715-744) explicitly exercises the stage-then-edit-clean scenario in a real git workflow: stage a planted secret, edit on-disk clean, attempt commit, expect the commit to be blocked.

### How a future auditor verifies the fix

```bash
# 1. Hook must contain the staged-blob read path
grep -c 'git show ":\$f"' /srv/Nexostrat/infra/hooks/pre-commit-secret-scan.sh
# Expected: 1

# 2. Plan must contain Step 6b
grep -c "Step 6b: Stage-then-edit-clean" \
  /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: 1

# 3. Run the live integration test (requires Plan 01a Task 3 already executed)
cd /srv/Nexostrat
echo "sk-ant-stagedblobtest1234567890abcdef" > stage_edit_verify.txt
git add stage_edit_verify.txt
echo "harmless" > stage_edit_verify.txt
# This commit MUST be blocked by the hook (staged blob contains the secret)
git commit -m "should be blocked" 2>&1 | grep -q BLOCKED && \
  echo "OK staged-blob scan working" || echo "FAIL — Finding 3 regression"
git restore --staged stage_edit_verify.txt
rm -f stage_edit_verify.txt
```

If the commit is NOT blocked, the hook regressed to on-disk scanning.

---

## Finding 4 — `SIGNED_PDF="~/Downloads/..."` tilde does not expand inside quotes

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 4" (search for "tilde inside double quotes").
**Plan location post-patch:** Task 17 Step 1 line 3192.

### What was wrong

Bash performs tilde expansion only on **unquoted** tildes. The pre-patch line:
```bash
SIGNED_PDF="~/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf"  # adjust to actual path
ls -la "$SIGNED_PDF"
```
Sets `$SIGNED_PDF` to the literal string `~/Downloads/...`. `ls` then errors with "No such file or directory" because there's no file at literal `~/...`. Steps 2 + 3 inherit the broken value.

### What's there now (post-patch, plan line 3192)

```bash
# Use $HOME (not ~ inside quotes — tilde does NOT expand inside double quotes; per Finding 4 of the 2026-05-14 re-audit).
SIGNED_PDF="$HOME/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf"  # adjust to actual path
ls -la "$SIGNED_PDF"
```

`$HOME` expands inside double quotes per POSIX shell rules. Steps 2 + 3 reuse `"$SIGNED_PDF"` and inherit the corrected expansion automatically.

### How a future auditor verifies the fix

```bash
# 1. No tilde-in-quotes remains in Task 17 (or anywhere in the plan)
grep -n 'SIGNED_PDF="~/' /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: no match outside the audit-response note (header line 31)

# 2. $HOME pattern present
grep -c 'SIGNED_PDF="\$HOME/' /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: 1
```

---

## Finding 5 — Task 7 `git add 00_META/skills` after `rmdir` errors fatal

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 5" (search for "Task 7 Step 5 `git add 00_META/skills` fails").
**Plan location post-patch:** Task 7 Step 5 lines 1583-1589.

### What was wrong

Pre-patch sequence:
- Step 2: `git mv 00_META/skills/<each> skills/<NN>_<each>` (renames staged)
- Step 3: `rmdir /srv/Nexostrat/00_META/skills` (removes empty source dir)
- Step 5: `git add 00_META/skills skills/`

After Step 3 the source path is gone. `git add 00_META/skills` errors fatal:
```
$ git mv src/file dst/ && rmdir src && git add src dst/
fatal: pathspec 'src' did not match any files
```
The R-rename entries were already staged by `git mv`, but the executor either has to know to ignore the fatal exit (manual run) or aborts (script run with `set -e`).

### What's there now (post-patch, plan lines 1583-1589)

```bash
# `git mv` (Step 2) has already staged the renames; `rmdir` (Step 3) removed the
# now-empty source directory. Use `git add -A` to pick up any remaining
# `.gitkeep` housekeeping without erroring on the removed source path
# (per Finding 5 of the 2026-05-14 re-audit — the previous `git add 00_META/skills`
# would have errored fatal because the path no longer exists).
git add -A
git status --short
```

`git add -A` operates on all changes in the working tree and never errors on a non-existent path argument.

### How a future auditor verifies the fix

```bash
# 1. The fatal-pathspec command must be absent from any task body
# (matches in the audit-response note at the top are expected; matches in
#  Task 7 itself are the regression).
grep -n 'git add 00_META/skills' /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: only lines 32 (audit-response note) and ~1587 (the contextualizing comment)
#           and ABSOLUTELY NOT a bare `git add 00_META/skills` command line.

# 2. The fix marker is present
grep -c '^git add -A$' /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: >= 1
```

---

## Finding 6 — C2 reverse-direction roundtrip underspecified for JP Light-mode

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 6" (search for "JP is Light-mode default").
**Plan location post-patch:** Task 13 Step 3 lines 2641-2706 + Step 4 lines 2708-2728.

### What was wrong

Pre-patch Step 3 instructed Ricardo to encrypt a sentinel, commit, push; JP pulls and decrypts. Then in prose: "Then the reverse (JP encrypts a sentinel; Ricardo decrypts)." Problems:
- JP is Light-mode default per ADR-021bis (Telegram + Gitea web only, no git CLI).
- No delivery mechanism specified for JP's encrypted sentinel back to Ricardo.
- Step 4 `git rm` expected BOTH files in the repo, but only one was committed.
- Without a concrete reverse-flow, bidirectional verification is one-way — silently violates spec §3's "either holder can decrypt" promise.

### What's there now (post-patch, plan lines 2641-2728)

**Direction A — Ricardo → JP** stays git-based (Ricardo pushes; JP pulls via Gitea web "raw" link, OR optionally clones one-time in Heavy mode).

**Direction B — JP → Ricardo** uses **Signal-attachment delivery, no git required on JP's side**:

1. Ricardo sends `infra/age-recipients.txt` contents via Signal (2-line public file, safe to paste).
2. JP saves it as `/tmp/nexostrat-recipients.txt` and encrypts:
   ```bash
   echo "Sentinel from JP $(date -Iseconds)" | \
     age -R /tmp/nexostrat-recipients.txt -o /tmp/sentinel-jp-to-ricardo.age
   ```
3. JP attaches `/tmp/sentinel-jp-to-ricardo.age` to a Signal message.
4. Ricardo saves the attachment, copies into `vault/keys/`, decrypts, confirms via Signal.
5. Stage + commit `vault/keys/sentinel-jp-to-ricardo.age` so Step 4 cleanup can `git rm` both sentinels in one pass.

Step 4 cleanup now uses `git rm` (not `git rm ... 2>/dev/null`) so the command errors loudly if either sentinel is missing — which is the desired loud failure if Step 3 was skipped or partial.

### How a future auditor verifies the fix

This finding has two verification surfaces: the plan **specifies** the flow (static check), and the executor **runs** the flow (dynamic check during Plan 01a execution).

```bash
# 1. Static: plan must specify Direction A and Direction B with Signal-attachment flow
grep -c 'Direction A — Ricardo → JP\|Direction B — JP → Ricardo' \
  /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: 2

grep -c 'Signal-attachment flow' /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md
# Expected: >= 1

# 2. Static: Step 4 cleanup must not silence the `git rm` errors
grep -A2 'remove both sentinels' /srv/Nexostrat/00_META/plans/2026-05-14_plan-01a-foundation.md | \
  grep -c 'git rm vault/keys/sentinel.*2>/dev/null'
# Expected: 0  (the pre-patch version silenced errors; the patched version does not)

# 3. Dynamic (during Plan 01a Task 13 execution): both directions must be exercised.
#    Ricardo + JP confirm via Signal. Both confirmations logged in STATUS.md.
#    A spot-check after Task 13 commits:
git log --grep="C2 verification sentinels" --oneline
# Expected: one commit, named "Plan 01a Task 13 · remove C2 verification sentinels"
#           with a body referencing BOTH Direction A and Direction B.
```

If Direction B was skipped, no JP-side confirmation will appear in STATUS.md and Step 4's `git rm` will have errored (no `sentinel-jp-to-ricardo.age` to remove).

---

## Finding 7 — `run-with-secrets.sh` `2>/dev/null` swallows age error diagnostics

**Severity:** HIGH
**Audit reference:** see audit report §"Finding 7" (search for "swallows decrypt-failure diagnostics").
**Plan location post-patch:** Task 15 Step 3 lines 2978-2996.

### What was wrong

Pre-patch wrapper:
```bash
if ! age -d -i <(age -d "$PRIV_KEY_AGE") "$ENC" > "$PT" 2>/dev/null; then
  echo "ERROR: failed to decrypt $ENC (wrong passphrase or recipient mismatch)" >&2
  exit 1
fi
```
The `2>/dev/null` discards age's stderr — which is where age writes its actual diagnostic messages ("Error: no identity matched", "decryption failed", "wrong passphrase", "identity file has unexpected format"). The user sees only the generic plan-defined message and exit 1, with no way to tell whether the failure is at the inner decrypt (private key issues) or the outer (recipient/file issues).

This matters most on JP's first successful onboarding: getting the passphrase wrong is normal; understanding *which* layer failed is critical to recovering.

### What's there now (post-patch, plan lines 2978-2996)

```bash
# Decrypt secrets to /dev/shm
# (the inner age -d prompts for the private-key passphrase on /dev/tty;
#  age's diagnostic messages go to stderr — capture them rather than silence,
#  per Finding 7 of the 2026-05-14 re-audit: first-time users need to
#  distinguish wrong-passphrase vs recipient-mismatch vs identity-file-format
#  failures.)
AGE_ERR=$(mktemp)
if ! age -d -i <(age -d "$PRIV_KEY_AGE") "$ENC" > "$PT" 2>"$AGE_ERR"; then
  echo "ERROR: failed to decrypt $ENC" >&2
  echo "  hint: wrong passphrase, recipient mismatch, or identity-file format issue" >&2
  if [[ -s "$AGE_ERR" ]]; then
    echo "  age stderr:" >&2
    sed 's/^/    /' "$AGE_ERR" >&2
  fi
  rm -f "$AGE_ERR"
  exit 1
fi
rm -f "$AGE_ERR"
```

`AGE_ERR` is a temp file collecting age's stderr stream. On failure, it's surfaced (indented 4 spaces) and removed. On success, it's removed silently.

### How a future auditor verifies the fix

```bash
# 1. `2>/dev/null` must NOT appear on the decrypt line
grep -n '2>/dev/null' /srv/Nexostrat/infra/scripts/run-with-secrets.sh | grep 'age -d'
# Expected: no match  (after Plan 01a Task 15 executed)

# 2. `2>"$AGE_ERR"` redirect pattern must be present
grep -c '2>"\$AGE_ERR"' /srv/Nexostrat/infra/scripts/run-with-secrets.sh
# Expected: >= 1

# 3. Dynamic: trigger a deliberately-wrong passphrase and verify diagnostic surfaces
/srv/Nexostrat/infra/scripts/run-with-secrets.sh true 2>&1 | grep -q 'age stderr:'
# When wrong passphrase entered: expected match. (Manual interactive test.)
```

---

## Deferred findings (5 MEDIUM + 3 LOW)

Per the auditor's own "Recommended next step" — these are addressable during Plan 01a execution as known-limits, or in a follow-up cycle.

| # | Severity | Subject | Why deferred | Where to track |
|---:|:---|:---|:---|:---|
| 8 | MEDIUM | tasks.json schema validation may halt on `created`-field absence | Plan handles via "stop and surface" gate; not catastrophic | Plan 01a Task 5 Step 7 (in-plan) |
| 9 | MEDIUM | `ln -sf .git/hooks/pre-commit` silently destroys existing custom hooks | Pre-flight check would be nice; not Plan 01a-blocking | Future hardening item |
| 10 | MEDIUM | `state.json` references schema `nexostrat-client-state-v1` not yet shipped | Plan 03 ships the schema; intermediate state is documented | Plan 03 |
| 11 | MEDIUM | Test sentinels live in `vault/keys/` (production-recovery namespace) | Hygiene regression, not correctness; alternative path `infra/test-fixtures/` works too | Optional Plan 01a in-execution swap |
| 12 | MEDIUM | `cost-sharing-agreement.md` notes spec §5 drift | Track via `t-spec-cost-table-amendment` | Existing tasks.json entry |
| 13 | LOW | `git add infra` in Task 1 may include pre-existing content | Cosmetic; no actual conflict | — |
| 14 | LOW | "Verified-only" list omits `infra/scripts/` state | Cosmetic | — |
| 15 | LOW | `v0.1a-foundation` tag precedes the STATUS.md update commit | Cosmetic ordering | — |

---

## How to re-verify the entire patch trail in one pass

A future auditor (or a paranoid future Claude) can run this single block to spot-check that every HIGH patch is still live:

```bash
cd /srv/Nexostrat
PLAN=00_META/plans/2026-05-14_plan-01a-foundation.md

echo "=== Finding 1: blanket *secrets* glob absent? ==="
grep -c '^\*secrets\*$' "$PLAN"                                             # expect 0
echo "=== Finding 1: allowlist present? ==="
grep -c '^!secrets\.env\.age$' "$PLAN"                                       # expect 1
grep -c '^!infra/secrets/MANIFEST\.md$' "$PLAN"                              # expect 1
echo "=== Finding 1: Step 5b positive-control present? ==="
grep -c 'Step 5b: Positive control' "$PLAN"                                  # expect 1

echo "=== Finding 2: poll-based design markers? ==="
grep -c 'POLL_DEADLINE_SECS\|positive control\|negative control' "$PLAN"     # expect >= 3
echo "=== Finding 2: buggy '2s sleep + immediate check' pattern absent? ==="
# (best done by inspecting the test body; this pattern was the false-PASS shape)

echo "=== Finding 3: hook uses git show staged-blob? ==="
grep -c 'git show ":\$f"' "$PLAN"                                            # expect 1
echo "=== Finding 3: Step 6b stage-then-edit test? ==="
grep -c "Step 6b: Stage-then-edit-clean" "$PLAN"                             # expect 1

echo "=== Finding 4: tilde-in-quotes absent in Task 17? ==="
# audit-response note (line 31) is allowed; Task 17 body is not
grep -n 'SIGNED_PDF="~/' "$PLAN"                                             # expect only line ~31 (note)
echo "=== Finding 4: \$HOME pattern present? ==="
grep -c 'SIGNED_PDF="\$HOME/' "$PLAN"                                        # expect 1

echo "=== Finding 5: bare 'git add 00_META/skills' command absent? ==="
# In task body, NOT inside the audit-response note + contextualizing comment
grep -nE '^git add 00_META/skills$' "$PLAN"                                  # expect no match
echo "=== Finding 5: 'git add -A' fix present? ==="
grep -c '^git add -A$' "$PLAN"                                               # expect >= 1

echo "=== Finding 6: bidirectional flow specified? ==="
grep -c 'Direction A — Ricardo → JP\|Direction B — JP → Ricardo' "$PLAN"     # expect 2
echo "=== Finding 6: Signal-attachment flow present? ==="
grep -c 'Signal-attachment flow' "$PLAN"                                     # expect >= 1

echo "=== Finding 7: '2>/dev/null' absent on the age decrypt line? ==="
grep -nE 'age -d.*2>/dev/null' "$PLAN"                                       # expect no match
echo "=== Finding 7: AGE_ERR capture pattern present? ==="
grep -c 'AGE_ERR=\$(mktemp)' "$PLAN"                                         # expect 1
grep -c 'hint: wrong passphrase' "$PLAN"                                     # expect 1

echo "=== Audit-response note in plan header? ==="
grep -c 'Re-audit response (2026-05-14)' "$PLAN"                             # expect 1
```

All 17 checks should land on the expected counts. Any deviation is either a regression of one of the 7 HIGH patches OR a structural change to the plan that should be reviewed independently.

---

## What this trail does NOT cover

- **The patches' correctness.** The trail proves the patches landed in the right places with the expected shape. It does NOT prove the patched code is bug-free — a future re-audit should treat the patches as new code under scrutiny. Specifically the new C1 leak-test (Finding 2's replacement) is interactive and depends on the human running it correctly; the staged-blob hook (Finding 3's replacement) has not been live-tested against every edge case (e.g. binary files, very large blobs, files with no newline); the Signal-attachment flow (Finding 6's replacement) assumes JP can receive/send attachments reliably, which has never been exercised.
- **The MEDIUM/LOW deferred findings.** Findings 8-15 may still surface as bugs during execution. They are documented above for the executor's awareness but no fix has landed.
- **New issues introduced by the patches.** Possible unknown-unknowns: the `MODE="git-hook"` branch in the secret-scan hook could behave unexpectedly under partial-stage-with-deletion; the `git add -A` in Task 7 is broader than the original intent and could pull in unrelated tracked changes; the `AGE_ERR=$(mktemp)` in `run-with-secrets.sh` creates a temp file outside `/dev/shm` that is not shred-cleaned. The future auditor should look for these.

---

*This trail was created at the close of Batch 3 step 1 (Plan 01a re-audit + patches), 2026-05-14. The next session will execute Plan 01a Tasks 1-11 via `superpowers:subagent-driven-development`. After execution completes (and on every subsequent re-audit), this trail can be used as the verification-side companion to the original audit report.*
