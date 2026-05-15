# Audit Report — Plan 01a (Repository Foundation)

> **Auditor:** risk-auditor (adversarial second seat, no exposure to plan-writing session)
> **Date filed:** 2026-05-14
> **Artifacts examined:**
> - `00_META/plans/2026-05-14_plan-01a-foundation.md` (3319 lines, 18 tasks)
> - `00_META/proposals/2026-05-13_nexostrat-system-design.md` (1008 lines, ADRs 001-037, Batch-1-amended)
> - `00_META/proposals/2026-05-14_amendments.md` (287 lines)
> - `00_META/proposals/2026-05-14_audit-report.md` (653 lines — reference only; conclusions not inherited)
> - Repo state at `/srv/Nexostrat/` (HEAD `2b6db31`; 16 commits past pre-audit baseline)
>
> **Brief:** independent re-audit gate before Plan 01a execution. Verify the 12 amendment-finding closures (C1, C2, F5, F10, F12, F13, F15, F16, F19, F21, F23, F26) are delivered by executable tasks, not just gestured at. Find correctness bugs, ordering violations, stale tasks, spec drift.

## Verdict
**YELLOW (large)**

## Summary

The plan is structurally sound and the 12 amendment-finding closures are all addressed by concrete tasks — no closure is purely cosmetic. But there are **three correctness bugs that will fail on first execution** (one of which makes the comprehensive `.gitignore` ironically un-commitable, and another of which causes the C1 test to pass trivially without exercising the C1 fix), plus a cluster of HIGHs around the secret-scan hook scanning the wrong content surface, the C2 reverse-direction roundtrip being underspecified for JP Light-mode, and the run-with-secrets wrapper having a non-interactive failure mode that the plan acknowledges but doesn't resolve.

No CRITICAL severity findings (the gitignore bug, although blocking, has a trivial inline fix; the broken C1 test is HIGH because the C1 wrapper itself is correctly implemented — the test is what's wrong). 7 HIGH findings means this falls into YELLOW (large) per the verdict scale: the affected tasks need to be re-written before execution. **No DESIGN-RETHINK FLAG** — the plan's architecture is correct; the defects are local fixes inside individual tasks.

## Findings

### Finding 1 — `.gitignore` pattern `*secrets*` blocks `infra/secrets/MANIFEST.md` (Task 16) AND `secrets.env.age` (Task 14)

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 2 Step 3, line 366 (gitignore content); collides with Task 14 (`secrets.env.age` commit) and Task 16 (`infra/secrets/MANIFEST.md` commit).

**Description:**
The proposed comprehensive `.gitignore` includes the pattern `*secrets*` (line 366). Per gitignore semantics, a no-slash pattern matches at any path depth. Verified empirically:
```
$ git check-ignore -v infra/secrets/MANIFEST.md
.gitignore:1:*secrets*	infra/secrets/MANIFEST.md
$ git check-ignore -v secrets.env.age
.gitignore:1:*secrets*	secrets.env.age
```

**Why it's wrong:**
Task 14 (`git add secrets.env.age`) and Task 16 (`git add infra/secrets/MANIFEST.md`) will both fail silently (`git add` on an ignored path is a no-op without `-f`), or the subsequent `git status` will show the staged set as empty. The plan's "Step 4: Stage + commit" sequence does not check that the file was actually staged — it commits whatever is staged, which for Task 14 / Task 16 is **nothing**. The commit succeeds with the wrong content; the encrypted secrets file and the manifest never enter the repo. v0.1a-foundation tag would point at a state missing both files.

**Proposed amendment:**
Replace the `*secrets*` blanket with surgical patterns. Three lines instead of one:
```
secrets.env
secrets.env.local
*.secrets.json
```
Or scope the pattern to specific paths:
```
**/secrets.env
**/secrets.local.env
```
Add an explicit allowlist for the two intentional commits:
```
!secrets.env.age
!infra/secrets/MANIFEST.md
```
Update the `test_gitignore_coverage.sh` test: the current "Age password files" check (`\*secrets\*|secrets\.env\$|\*\.env\b`) passes against the buggy pattern, so the test does not catch this regression. Add a positive test:
```bash
check "Allow MANIFEST.md" '!infra/secrets/MANIFEST\.md|^infra/secrets/MANIFEST'
check "Allow secrets.env.age" '!secrets\.env\.age'
```
Or better: add a live `git check-ignore` step that asserts the two intentional paths are NOT ignored.

---

### Finding 2 — `test_run_with_secrets_no_leak.sh` produces a false PASS; does not actually test C1

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 15 Step 1 (lines 2673-2722); the C1 closure test.

**Description:**
The leak-detection test backgrounds the wrapper (`"$WRAPPER" sh -c 'sleep 60' &`) then checks `/dev/shm` after 2 seconds. But `run-with-secrets.sh` calls `age -d -i <(age -d "$PRIV_KEY_AGE") ...` — the inner `age -d` decrypts the passphrase-encrypted private key, which **requires interactive passphrase entry on /dev/tty**. The backgrounded process has no controlling TTY (or shares the test harness's TTY without focus), so it blocks indefinitely on the passphrase prompt before ever reaching the `> "$PT"` write. At T+2s, `/dev/shm/nexostrat-secrets-*` does not exist yet because the wrapper hasn't gotten past the passphrase prompt — so `LEAKED=0` and the test prints "PASS — no leak". The wrapper could leak catastrophically and this test would still pass.

Secondary defects in the same script:
- Step 2 (positive test, lines 2702-2704) prints `ANTHROPIC_API_KEY=…` but has no assertion. If the sourcing failed entirely the test still exits 0.
- Step 4 cleanup (`pkill -P $WRAPPER_PID` after `kill $WRAPPER_PID`) targets a dead parent's children. Once the wrapper exits, its child shell + sleep get reparented to init; `pkill -P` finds no children. Leftover `sleep` processes accumulate across test runs.
- Step 1's pre-condition (`rm -f /dev/shm/nexostrat-secrets-*`) silently deletes any concurrent legitimate session's plaintext if the developer happens to be using `run-with-secrets.sh` in another terminal — a footgun.

**Why it's wrong:**
C1 is one of the two load-bearing CRITICAL findings the plan claims to close. The test that proves the closure is the gate. A test that passes by accident on the broken case (passphrase-hang masks the leak detection) means **C1 is not actually verified by Plan 01a's own DoD**. The plan-level success criterion (line 15: "no files — C1 verified") is checked by Task 18 Step 1 by re-running this same broken test. Task 15 Step 5 includes a manual smoke test (kill the wrapper, recount) which is correct — but only if the executor reaches that step interactively after the passphrase prompt resolves.

**Proposed amendment:**
Either (a) make the test non-interactive by caching the unlocked private key (write `~/.config/age/nexostrat.key` plaintext-on-tmpfs for the test duration, shred after), or (b) accept that the test is interactive and rewrite it as a **two-step protocol** the human runs:
1. Foreground: `bash $WRAPPER sleep 30 &` — type passphrase, hit enter, immediately disown.
2. After 5s (wrapper now running, file is at `/dev/shm`), check it exists (positive control — file SHOULD be there during execution).
3. Kill wrapper PID. Sleep 1s. Check file is gone (negative control — file MUST be removed).
4. Assert exit code based on both checks.

Additionally:
- Remove the silent `rm -f /dev/shm/nexostrat-secrets-*` pre-condition (or scope it to test-PID-only files).
- Add a `set -e`-style assertion in Step 2 that captures the wrapper's stdout and `grep`s for `ANTHROPIC_API_KEY=`, exiting non-zero if absent.
- Replace `pkill -P` cleanup with `kill 0` from inside a subshell wrapper, or use `setsid` to make the wrapper a process-group leader and kill the whole group.

---

### Finding 3 — Pre-commit secret-scan hook scans the on-disk file, not the staged blob

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 3 Step 3 (lines 544-603); `infra/hooks/pre-commit-secret-scan.sh`.

**Description:**
The hook iterates `git diff --cached --name-only --diff-filter=ACMR` to get staged paths, then `grep`s each as a path on disk (`grep -EHn "$PATTERNS" "$f"`). For 95% of workflows this is equivalent to scanning the staged content — but it diverges in the dangerous case:

1. User edits a file with a secret, runs `git add`, then edits the file to remove the secret, then `git commit`. The on-disk file is clean; the **staged blob still contains the secret**. The hook scans the clean on-disk content, lets the commit through, the secret enters history.
2. Inverse: user `git add` of a clean file, then edits to add a secret, then `git commit`. Hook scans on-disk (now dirty), blocks the commit. But the actual staged content is clean — false positive.

**Why it's wrong:**
The hook's purpose is to prevent secrets from entering the repository. The repository contents = staged blobs, not working-tree files. The plan's live integration test in Step 6 (lines 627-636) plants the secret, `git add`s, immediately commits — so on-disk == staged. The test passes despite the hook scanning the wrong surface.

Stage-vs-disk divergence is a real recurring scenario in interactive development (especially with editors that auto-format on save). The probability of false-negative in a 12-month window is non-trivial.

**Proposed amendment:**
Replace the on-disk read with `git show :<path>` (the staged-blob read):
```bash
for f in "${FILES[@]}"; do
  # Stop iterating if file deleted (D filter excluded already)
  if blob=$(git show ":$f" 2>/dev/null); then
    if printf '%s' "$blob" | grep -EHn "$PATTERNS" --label="$f" 2>/dev/null; then
      violations=$((violations+1))
    fi
  fi
done
```
Update `test_secret_scan_hook.sh` to test both the `--files-from-stdin` mode (current) and a real git-staged scenario where on-disk and staged differ.

---

### Finding 4 — Task 17 Step 1 uses tilde inside double quotes; path will not expand

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 17 Step 1, line 2988; reused at Step 2 (line 3000) and Step 3 (line 3015).

**Description:**
```bash
SIGNED_PDF="~/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf"  # adjust to actual path
ls -la "$SIGNED_PDF"
```
Bash performs tilde expansion only on **unquoted** tildes (and certain assignment contexts). Inside double quotes, `~` is literal. Verified:
```
$ SIGNED_PDF="~/Downloads/test.pdf"; ls "$SIGNED_PDF"
ls: cannot access '~/Downloads/test.pdf': No such file or directory
```

**Why it's wrong:**
Step 1 fails with "No such file or directory" even if the PDF exists at `$HOME/Downloads/...`. Step 2 (encrypt) inherits the broken value and writes the input from a non-existent path. Step 3 (sha256 comparison) compares the same broken path to the decrypted output. The plan acknowledges "adjust to actual path" but doesn't fix the quoting — an executor that pastes literally and only edits the filename portion still hits the bug.

**Proposed amendment:**
Two correct forms — either:
```bash
SIGNED_PDF=~/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf  # no quotes
```
or:
```bash
SIGNED_PDF="$HOME/Downloads/PARTNERSHIP_AGREEMENT_2026-05-12_signed.pdf"
```
Apply consistently in Steps 1, 2, 3.

---

### Finding 5 — Task 7 Step 5 `git add 00_META/skills` fails after Step 3 removes the directory

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 7 Step 3 (line 1465: `rmdir /srv/Nexostrat/00_META/skills`) then Step 5 (line 1483: `git add 00_META/skills skills/`).

**Description:**
After `git mv 00_META/skills/<each> skills/<NN>_<each>`, the source folder is empty. Step 3 `rmdir`s it. Step 5 then runs `git add 00_META/skills skills/`, but `00_META/skills` no longer exists. Verified:
```
$ git mv src/file.txt dst/ && rmdir src && git add src dst/
fatal: pathspec 'src' did not match any files
```
Exit code 128.

**Why it's wrong:**
The `git mv` already staged the rename; `git add` on the removed source path errors out. The commit step then fails because the commit message heredoc is the next command in the sequence — `set -e` style runners abort, manual runners get a confusing error. The R-rename entries are already staged so the commit could succeed, but only if the executor knows to skip the failed `git add`.

**Proposed amendment:**
Replace Step 5's `git add` line with one of:
```bash
git add -A                                 # all changes including renames
# OR
git add skills/                            # only the destination side
```
Or drop the `git add` entirely — `git mv` has already done the staging.

---

### Finding 6 — C2 reverse-direction (JP → Ricardo) roundtrip is underspecified

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 13 Step 3 (lines 2531-2570); load-bearing C2 success criterion ("Reverse roundtrip holds" — plan header line 14).

**Description:**
Step 3 commands Ricardo to encrypt a sentinel, commit, push. JP decrypts. Then in prose: "Then the reverse (JP encrypts a sentinel; Ricardo decrypts)." But:
- JP is Light-mode default (per ADR-021bis): Telegram + Gitea web only, no git CLI, no commit-and-push capability.
- No mechanism is specified for JP to deliver his encrypted sentinel back to Ricardo (Signal attachment? Gitea web upload? Plan doesn't say).
- Step 4 cleanup (`git rm vault/keys/sentinel-ricardo-to-jp.age vault/keys/sentinel-jp-to-ricardo.age`) expects BOTH files in the repo, but only the first was committed.

**Why it's wrong:**
Bidirectional roundtrip is the load-bearing C2 success criterion ("either holder can decrypt" — spec §3 Identities; "Reverse roundtrip holds" — plan line 14). One-directional verification (Ricardo encrypts, JP decrypts) only proves JP's pubkey was added correctly to the recipients file. It does NOT prove JP's private key actually decrypts properly with passphrase under his real working setup. If JP's passphrase is wrong, or his Bitwarden backup is corrupt, the spec's "either holder can decrypt" promise is silently broken — only discovered later when Ricardo is unavailable.

**Proposed amendment:**
Specify the reverse-direction flow concretely:
1. JP encrypts on his machine: `age -R infra/age-recipients.txt -o /tmp/sentinel-jp.age <<<"sentinel from JP $(date -Iseconds)"`. (Requires JP has a clone OR the recipients file content — give him the recipients-file contents via Signal so he doesn't need git.)
2. JP attaches `/tmp/sentinel-jp.age` to Signal → Ricardo.
3. Ricardo `git add`s into `vault/keys/sentinel-jp-to-ricardo.age`, commits, decrypts with his key, confirms.
4. Step 4 cleanup commits both removals in one pass.

Alternatively: include a "JP Heavy-mode" lite version of this gate — JP installs git + clones one-time just for this test, encrypts in-tree, pushes. Or document the verification as "JP performs decrypt-only; the encrypt-side is verified later when JP next has Heavy access" — but this weakens C2 closure.

---

### Finding 7 — `run-with-secrets.sh` `2>/dev/null` swallows decrypt-failure diagnostics

**Severity:** HIGH
**Artifact:** plan-01a
**Location:** Task 15 Step 3 line 2787; `age -d -i <(age -d "$PRIV_KEY_AGE") "$ENC" > "$PT" 2>/dev/null`.

**Description:**
The wrapper redirects all of age's stderr to `/dev/null`. Two consequences:
1. The passphrase prompt for the inner `age -d` (decrypting `$PRIV_KEY_AGE`) goes to `/dev/tty` (age uses TTY directly for passphrases), so the user does see and can answer it. But age's error messages — "Error: no identity matched" / "decryption failed" / "wrong passphrase" — go to stderr and are silenced.
2. When the decrypt legitimately fails, the user gets the generic plan-defined message "ERROR: failed to decrypt $ENC (wrong passphrase or recipient mismatch)" and exit 1. The actual age error (e.g., "passphrase entered too quickly" or "identity file has unexpected format") is lost.

**Why it's wrong:**
The first time JP runs the wrapper and the passphrase is wrong (very likely on first attempt — Bitwarden retrieval, typing in passphrase, etc.), he gets no signal whether the failure is at the inner decrypt (his private key) or the outer (the secrets file). Diagnostic feedback is critical at this trust-establishment moment.

**Proposed amendment:**
Drop the `2>/dev/null` or redirect to a captured log:
```bash
AGE_LOG=$(mktemp)
if ! age -d -i <(age -d "$PRIV_KEY_AGE") "$ENC" > "$PT" 2>"$AGE_LOG"; then
  echo "ERROR: failed to decrypt $ENC" >&2
  echo "age stderr:" >&2
  sed 's/^/  /' "$AGE_LOG" >&2
  rm -f "$AGE_LOG"
  exit 1
fi
rm -f "$AGE_LOG"
```

---

### Finding 8 — Plan-level success criterion #3 is checked against tasks.json before Task 5 modifies it

**Severity:** MEDIUM
**Artifact:** plan-01a
**Location:** Plan header line 16 (success criterion); Task 5 (validates tasks.json + calendar.json against schemas).

**Description:**
The plan's success criterion #3 says `python3 -c "import jsonschema, json; jsonschema.validate(json.load(open('tasks.json')), json.load(open('infra/schemas/tasks.schema.json')))" exits 0`. The schema (Task 5 creates it) defines tasks-array items with `additionalProperties: false`, allowing only: id, subject, status, priority, due, created, completed, blocked_by, notes. But the current `tasks.json` includes some tasks with extra fields not in this list (re-checked: current tasks have only the allowed fields + occasionally `completed`/`notes` — likely OK).

More concretely: the schema requires `created` on every task. Current `tasks.json` was hand-written; if any task lacks `created`, validation fails. Task 5 Step 7 surfaces this with "**stop and surface the discrepancy to Ricardo** — do not patch existing data without his sign-off." OK as a guard — but it means Plan 01a Task 5 has a non-zero probability of halting mid-plan on a state validation issue that wasn't introduced by Plan 01a.

**Why it's wrong:**
Not catastrophic — the plan handles it via a "stop and surface" gate. But "stop and surface" introduces a Plan 01a interrupt that could happen during JP-gate-1 (Tasks 1-11), forcing a session split. The validation against existing data should have been done in Batch 1 before this plan was even written.

**Proposed amendment:**
Pre-flight check (top of Plan 01a, before Task 1): run the validator against `tasks.json` once and either confirm it passes (with a then-unwritten schema — chicken-and-egg) or have the executor preview the schema and fix `tasks.json` data drift first. Alternatively: relax the schema's `required` array to only `[id, subject, status, priority]` and document `created` as a best-practice not a hard constraint. Or schema-validate during execution and only require new task entries to have full fields.

---

### Finding 9 — Pre-flight checks run before Task 1 but don't verify hook directory or check for stale `.git/hooks/pre-commit`

**Severity:** MEDIUM
**Artifact:** plan-01a
**Location:** Pre-flight checks (lines 163-209); Task 3 Step 4 (symlinks into `.git/hooks/pre-commit`).

**Description:**
Task 3 Step 4: `ln -sf ../../infra/hooks/pre-commit-secret-scan.sh .git/hooks/pre-commit`. The `-f` (force) silently overwrites whatever was there. But: pre-flight doesn't check whether `.git/hooks/pre-commit` already exists as a real file (e.g., a user's local custom hook, or one installed by a tool like `pre-commit` Python framework, or a brain hook installed externally). The plan silently destroys it.

**Why it's wrong:**
Plan 01a's environment includes Ricardo's existing HP-laptop setup where `/srv/brain/` previously co-existed in this directory (per `brain references stripped` directive). Any leftover hook from that era gets clobbered. More generally: `ln -sf` is destructive without confirmation. Symptom: a user reports `pre-commit` framework hooks stopped firing; root cause is silently buried.

**Proposed amendment:**
Pre-flight: `ls -la .git/hooks/pre-commit` — if exists and is NOT already a symlink to the plan's target, surface to Ricardo before proceeding. Or use a managed `.git/hooks/pre-commit` wrapper that chains multiple hooks. For Plan 01a scope, a simple stat-check pre-flight + explicit `rm` before `ln -sf` is enough.

---

### Finding 10 — Task 4 `state.json` schema is "nexostrat-client-state-v1" but no schema file exists

**Severity:** MEDIUM
**Artifact:** plan-01a
**Location:** Task 4 Step 1, line 686 (`"$schema": "nexostrat-client-state-v1"`); README line 779 says "Schema: `nexostrat-client-state-v1` (full schema landed in Plan 03 alongside the event-spine validators)".

**Description:**
The `state.json` template references a schema name (`nexostrat-client-state-v1`) for which no schema file exists in Plan 01a's deliverables (`infra/schemas/` gets only `tasks.schema.json` and `calendar.schema.json` per Task 5). The schema is deferred to Plan 03. Until then, the `$schema` field is a free-floating identifier with no validator.

**Why it's wrong:**
Minor by itself, but Task 5 Step 7 includes a "validate everything against its $schema" check pattern. If anyone (mis)reads Task 5's validator pattern and applies it to state.json, the validator can't find the schema and either errors loudly (best case) or silently passes (worst case — depends on `jsonschema` library's missing-$id behavior). Plan should call out the schema-pending state explicitly in `state.json` or use a placeholder identifier (e.g., `"$schema": "nexostrat-client-state-v1 (pending — Plan 03)"`).

**Proposed amendment:**
Either:
- Add a stub `infra/schemas/client-state.schema.json` to Plan 01a that validates only the top-level fields present in the template (minimal schema, full version lands in Plan 03), OR
- Drop the `$schema` field from `state.json` entirely until Plan 03 ships the validator, with a comment in the README that explains why.

---

### Finding 11 — Task 13 sentinel files live at `vault/keys/` but plan claims Founder owns `vault/keys/` while sentinel-encrypt-roundtrip is a cross-persona test

**Severity:** MEDIUM
**Artifact:** plan-01a
**Location:** Task 13 Step 3, line 2539: `vault/keys/sentinel-ricardo-to-jp.age`.

**Description:**
Per spec §4.1 (F10 reallocation) and Task 10's README: Founder owns `vault/keys/` (recovery codes, key-rotation log). Using `vault/keys/` for ephemeral roundtrip-test artifacts is mixing test fixtures into a folder semantically reserved for production recovery material. The sentinel files commit→decrypt→remove cycle commits content that has no business in the long-term forensic record of `vault/keys/`.

**Why it's wrong:**
Not a correctness defect, but a discipline regression. A reader 6 months from now examining `git log vault/keys/` will see "sentinel-ricardo-to-jp.age" as a removed file — opaque without the plan as context. Better isolation = better hygiene.

**Proposed amendment:**
Use a test-fixture path that doesn't pollute vault namespace. E.g., `infra/test-fixtures/sentinel-*.age` or even `/dev/shm/` only with the sha256 of the ciphertext committed as the proof. Or: skip the commit entirely; share the .age via Signal attachment (matches Finding 6's proposed JP-side flow).

---

### Finding 12 — `cost-sharing-agreement.md` self-acknowledges spec drift; Plan 01a doesn't close the loop

**Severity:** MEDIUM
**Artifact:** plan-01a
**Location:** Task 9 Step 5, lines 1993-1996 (final note in cost-sharing-agreement.md: "Spec §5 cost table will be amended in a future cycle to match this document — see `t-spec-cost-table-amendment`.")

**Description:**
The cost-sharing agreement document explicitly notes that the spec's §5 cost table is inconsistent with this document (Notion now $0 to firm via JP's personal subscription; spec still has F14-style cost line per Batch 1 amendments). The plan lands a document that openly contradicts the spec and points at a TODO task.

**Why it's wrong:**
Plan 01a is supposed to leave the repo in a coherent state. Shipping a "this contradicts the spec; please fix the spec later" comment passes the buck. If the cost table is genuinely wrong post-Batch-1, fix the spec in Batch 1 closure (it claims F14 is done per the Batch-1 changelog) — verify and reconcile in Plan 01a, not later.

The MEMORY entry `feedback_no_brain_references.md` plus `project_notion_via_jp.md` confirm the F14 revision was "Notion stays $0 to firm via JP's personal subscription." Verify the spec actually reflects this state; if it doesn't, that's a Batch 1 oversight, not a Plan 01a concern. If it does, this comment in cost-sharing-agreement.md is wrong and should be removed.

**Proposed amendment:**
Either: (a) drop the trailing note in cost-sharing-agreement.md (the spec already says $0 per F14 revised); or (b) add a Task 0.5 / pre-flight check that re-reads spec §5 cost table against this document and surfaces drift before Plan 01a proceeds; or (c) add an explicit task to fix the spec in Plan 01a (small `Edit` to one spec section).

---

### Finding 13 — Task 1 commit covers `infra/` but Plan-01a-created `infra/age-recipients.txt` already exists; verify what gets committed

**Severity:** LOW
**Artifact:** plan-01a
**Location:** Task 1 Step 4, line 262: `git add 00_PARTNERSHIP docs vault knowledge skills pipeline operations infra`.

**Description:**
`git add infra` from a clean working tree where `infra/age-recipients.txt` is already committed will add only the new contents (the `.gitkeep` files in the new subfolders). But `infra/scripts/` already exists (created earlier in the session for `build_brand_template.py` parking — actually no, that's `00_META/scripts/`). Let me re-check: `ls infra/` before Task 1 has only `age-recipients.txt`. Task 1 creates `infra/{agents,telegram,events,shadow,systemd,recovery,observability,machines,schemas,secrets,scripts,hooks}/`. None of these conflict.

**Why it's wrong:**
Not actively wrong, just a fragility. The pattern `git add <dir>` is robust enough; this is a note rather than a finding.

**Proposed amendment:**
None required. Note kept for completeness.

---

### Finding 14 — Plan's "Verified-only" list omits `infra/scripts/` (does not exist before Task 1)

**Severity:** LOW
**Artifact:** plan-01a
**Location:** File Structure block, lines 153-159; comparison vs current repo state.

**Description:**
The "Verified-only" list says `infra/age-recipients.txt` exists. But it doesn't mention that `infra/` has only that single file pre-Plan-01a (no subfolders). Cosmetic — the verifier just needs to know the state.

**Proposed amendment:**
None required.

---

### Finding 15 — Task 18 tag commit comes BEFORE the STATUS.md/tasks.json update commit

**Severity:** LOW
**Artifact:** plan-01a
**Location:** Task 18 Step 7 (tag) precedes Step 8 (STATUS commit).

**Description:**
The `v0.1a-foundation` tag points at the pre-STATUS-update commit. The STATUS.md update is a follow-up commit AFTER the tag. Means `git checkout v0.1a-foundation` lands in a state where STATUS.md does not yet reflect the milestone completion. Not wrong — tag points at the substantive milestone — but slightly counterintuitive.

**Proposed amendment:**
Either reverse the order (STATUS update first, then tag), or note explicitly that the tag is at the "substantive" milestone before the prose update. Cosmetic.

---

## Stale tasks

None of Plan 01a's CREATE tasks are stale. All terrain-prep work is already represented as VERIFY tasks where appropriate:
- `infra/age-recipients.txt` — Task 11 VERIFIES (correctly framed as verification, not creation)
- `tasks.json` `$schema` — Task 5 Step 5 VERIFIES (with conditional sed if drift)
- `calendar.json` `$schema` — Task 5 Step 6 VERIFIES
- `.gitignore` — Task 2 REPLACES the interim version (intentional, not stale)
- Gitea origin remote — pre-flight check only (not a task)
- `00_META/handoff/` templates — already exist; Plan 01a doesn't try to recreate
- `00_META/journal/` — already exists with entries; Plan 01a doesn't touch
- `CLAUDE.md`, `GEMINI.md`, `README.md`, `STATUS.md`, `CHECKPOINT.md`, `00_META/CHANGELOG.md` — all listed under "Verified-only" header

One observation: Task 7 moves `00_META/skills/{company-analyst, industry-analyst, competitor-analyst, discovery-meeting}/` to canonical `skills/<NN>_<name>/`. Confirmed these four parking folders exist in the current repo state. The move is real work, not stale.

## What works well

- **Test-first discipline applied consistently.** Tasks 2, 3, 5, 15 each write a failing test, run it (expect FAIL), implement, run again (expect PASS). The pattern is correct even where individual tests have defects (Findings 2, 3 above) — the structure is sound; the test contents need fixing.
- **JP-coordination gate is cleanly placed.** Tasks 1-11 genuinely require no JP input (verified by trace: Task 11 is Ricardo-only roundtrip; Task 12 is the first task that touches JP's pubkey). The boundary is real and the pause-resume CHECKPOINT pattern is well-documented (lines 2399-2415).
- **Every claimed amendment-finding closure has a concrete task assignment.** C1 → Task 15; C2 → Tasks 12+13; F5 → Task 17; F10 → Tasks 1+10; F12 → terrain prep + Task 5 verify; F13 → Task 6 jp-heavy.yaml; F15 → Task 8; F16 → Task 4; F19 → Task 4; F21 → Task 5; F23 → Task 2; F26 → Task 6 phones.yaml. No closure is purely cosmetic.

---

## Recommended next step

Apply inline patches for Findings 1, 4, 5 (single-line fixes), and Findings 2, 3, 6, 7 (small rewrites of the affected test scripts and the wrapper's stderr handling). Re-spot-check the gitignore against Tasks 14 + 16 deliverables with `git check-ignore -v` as a positive control. After patches, plan should reach GREEN. Findings 8-15 can be addressed during execution as known-limits or deferred to a follow-up.

If the executor proceeds without these fixes, Tasks 14 and 16 will silently produce empty-staged commits (Finding 1), Task 17 will halt on a path error (Finding 4), Task 7 will hit a confusing git-add fatal (Finding 5), the C1 closure proof will be unsound (Finding 2), and the secret-scan hook can be bypassed by trivial workflow accident (Finding 3) — defects that are easy to fix now and painful to debug post-execution.

---

*This audit was conducted without seeing the plan-writing session. The plan itself is internally consistent and the architecture is correct. Defects are localized to specific tasks and inline-fixable.*
