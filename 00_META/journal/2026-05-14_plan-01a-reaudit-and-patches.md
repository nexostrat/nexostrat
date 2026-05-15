# 2026-05-14 — Plan 01a re-audit + 7 HIGH inline patches (Batch 3 step 1)

**Session type:** work · audit-response · plan-patching
**Duration:** ~2.5 hours focused
**Agent:** Claude (Opus 4.7, 1M context) at root in driver session with Ricardo
**Commits this session:** `6ca022c`
**Repo state at session end:** 17 commits ahead of pre-audit baseline; working tree clean.

## Session shape

Single-purpose session: execute **Batch 3 step 1** of the foundation-construction sequence — independent re-audit of Plan 01a, then apply every HIGH-severity finding. The CHECKPOINT.md baton from the prior session locked the dispatch pattern (general-purpose agent with `risk-auditor` persona inlined, same as the 2026-05-14 founding-spec audit). Ricardo's session opener was a single line ("PRocede with the next step"); I read it as authorization for the canonical sequence.

Two sub-arcs ran end-to-end inside the session:

1. **Re-audit dispatch.** Dispatched the agent with full inputs (the plan, the founding spec, the amendment plan, the prior audit report for format reference, the current repo state for stale-task detection). Asked for a structured report with the same shape as the 2026-05-14 founding-spec audit. The agent returned a 416-line report in ~60 minutes wall-clock.

2. **Inline patches.** Ricardo picked the surgical-patches path (auditor's own recommended next step) over the canonical-rule full-rewrite. I patched Plan 01a in 7 edits, verified each by grep, committed everything in one logical unit, and pushed.

## What we built

**Commit `6ca022c` — Plan 01a re-audit (Batch 3 step 1) + 7 HIGH inline patches.** 3 files / 700 insertions / 79 deletions:

- **NEW:** `00_META/proposals/2026-05-14_plan-01a-audit-report.md` (416 lines) — the adversarial audit's full output. Verdict YELLOW (large): 0 CRITICAL, 7 HIGH, 5 MEDIUM, 3 LOW, no DESIGN-RETHINK FLAG. Each finding includes severity, artifact, location (pre-patch line numbers), description, why-it's-wrong, proposed amendment. Sections: § Findings (15), § Stale tasks (none), § What works well (3 callouts), § Recommended next step.

- **MODIFIED:** `00_META/plans/2026-05-14_plan-01a-foundation.md` (3319 → 3523 lines) — patched in 7 surgical inline edits, plus a new "Re-audit response (2026-05-14)" block in the plan header citing the audit report and naming each fix.

- **MODIFIED:** `tasks.json` — `t-plan-01a-reaudit` moved `open → done` with detailed completion notes; `t-plan-01a-execute` notes updated to reflect re-audit closure.

## What the audit found (the 7 HIGH findings)

Lifting from the audit report — concise version:

1. **Gitignore `*secrets*` glob blocks intentional commits.** The blanket pattern at Task 2 Step 3 would silently ignore `secrets.env.age` (Task 14) and `infra/secrets/MANIFEST.md` (Task 16) — both Plan 01a deliverables. `git add` on an ignored path is a silent no-op without `-f`; the subsequent `git commit` would land an empty staged set. `v0.1a-foundation` tag would point at a state missing both files.

2. **C1 leak-detection test passes by accident.** The pre-patch test backgrounded the wrapper around `sleep 60` and checked `/dev/shm` 2 seconds later. But the wrapper's inner `age -d` blocks on the passphrase prompt before reaching the write. At T+2s, no plaintext file exists yet, so the test sees "no leak" and prints PASS — even if the C1 cleanup logic were completely broken. The test that proves the closure was unsound. (This is the load-bearing one.)

3. **Pre-commit secret-scan hook scans on-disk, not staged blob.** The hook iterated staged paths but `grep`ed each as an on-disk file. Stage-then-edit-clean (stage a file with a secret, edit it clean on disk, commit) would slip the secret into history because the on-disk content is clean by commit time. The repository contents = staged blobs, not working-tree files. The plan's own integration test couldn't catch this because it staged+committed in the same step (on-disk == staged).

4. **`SIGNED_PDF="~/Downloads/..."` tilde does not expand inside double quotes.** Bash performs tilde expansion only on unquoted tildes. Task 17 Step 1 would fail with "No such file or directory" even when the PDF exists at the right path.

5. **Task 7 `git add 00_META/skills` after `rmdir` errors fatal.** Step 3 removes the now-empty source directory; Step 5 tries to `git add` it. `fatal: pathspec '00_META/skills' did not match any files`.

6. **C2 reverse-direction roundtrip underspecified.** JP is Light-mode default (Telegram + Gitea web only, no git CLI). The pre-patch Task 13 Step 3 said "Then the reverse (JP encrypts a sentinel; Ricardo decrypts)" with no delivery mechanism. One-directional verification only proves JP's pubkey was added correctly; it does NOT prove JP's private key + passphrase actually work on his real machine. Spec §3's "either holder can decrypt" promise silently weakened.

7. **`run-with-secrets.sh` `2>/dev/null` swallows age error diagnostics.** When decrypt legitimately fails, the user sees a generic plan-defined message and exit 1 — but age's actual error ("wrong passphrase" / "no identity matched" / "identity file has unexpected format") is silenced. First-time onboarding for JP is opaque on failure.

## What we fixed (the patches)

Each finding got one targeted edit. None changed architecture; each is a code-block-scoped fix inside an existing task. The full forensic record is at `00_META/proposals/2026-05-14_plan-01a-patch-verification-trail.md` — that doc shows the pre-patch and post-patch snippet for every finding, plus exact `grep` commands a future auditor can run to verify each fix is still live.

Headline shapes:
- **Finding 1:** Replaced `*secrets*` with 6 surgical patterns + 2-line explicit allowlist (`!secrets.env.age`, `!infra/secrets/MANIFEST.md`). Added Plan 01a Task 2 Step 5b: a positive `git check-ignore -q` assertion that FAILs if either allowlisted path is ignored. Updated the coverage test to assert the allowlist lines are in the file.
- **Finding 2:** Rewrote the leak test as a poll-based positive+negative protocol. Snapshot `/dev/shm` files pre-run (no global blast); background wrapper around `sleep 20`; poll up to 30s for a NEW file to appear (positive control — proves wrapper got past passphrase prompt and wrote plaintext); kill wrapper; verify the SPECIFIC observed file path is gone (negative control — proves C1 cleanup fired).
- **Finding 3:** Branched the hook on mode. `--files-from-stdin` mode keeps on-disk grep (for unit tests). Default git-hook mode reads `git show :"$f"` — the actual staged blob. Added Task 3 Step 6b: stage-then-edit-clean integration test that proves the staged-blob path catches the bypass.
- **Finding 4:** `SIGNED_PDF="$HOME/Downloads/..."` instead of `"~/..."`. One-line.
- **Finding 5:** `git add -A` instead of `git add 00_META/skills skills/`. One-line.
- **Finding 6:** Specified Direction B (JP → Ricardo) as Signal-attachment delivery. Ricardo sends `infra/age-recipients.txt` contents via Signal paste; JP runs `age -R /tmp/nexostrat-recipients.txt -o /tmp/sentinel-jp-to-ricardo.age <<<"..."`; JP attaches the .age to Signal; Ricardo saves, copies into `vault/keys/`, decrypts. Step 4 cleanup `git rm`s both sentinels in one pass (errors loudly if either is missing).
- **Finding 7:** Captured `2>"$AGE_ERR"` (mktemp), surfaced on failure with "hint:" line + indented age stderr block. Removed `2>/dev/null` from the decrypt invocation.

## Decisions made

- **Surgical patches over full rewrite.** The amendment plan's locked rule was "YELLOW with ≤3 amendments → inline; more → re-write affected tasks." 7 HIGH would, strict-letter, trigger rewrite. But the auditor's own "Recommended next step" said inline patches would reach GREEN; the defects were architecturally local. Surgical was the auditor-endorsed pragmatic path AND lower-risk (less surface area for new defects introduced by the rewrite). Ricardo chose surgical. (Recorded as a soft precedent: when auditor verdict-shape says "large" but auditor recommendation says "small," the recommendation is the load-bearing signal.)

- **Standalone patch-verification-trail doc.** Ricardo asked for "a note for a future audit so it can verify what happened what went wrong and how did you fix it." Three options offered: standalone in `00_META/proposals/`, appendix in the audit report, or journal-only. He chose standalone — most discoverable for a future auditor, doesn't mutate the original adversarial document, and reads cleanly in isolation. Lives at `00_META/proposals/2026-05-14_plan-01a-patch-verification-trail.md`.

- **End session, defer Plan 01a execution to a new session.** Tasks 1-11 estimated 4-6h; subagent-driven-development benefits from a clean context; no calendar pressure (execute due 2026-05-27, 13 days out). Ricardo agreed.

## Disambiguation moments

- **Audit dispatch pattern.** Default (general-purpose + risk-auditor inlined) vs direct `risk-auditor` subagent invocation. Defaulted per CHECKPOINT.md guidance; pattern worked cleanly again — 416-line structured report, 7 HIGH findings, clear severity rationale per finding.

- **Patch path choice.** 4-option question to Ricardo (full rewrite vs surgical vs mixed vs pause-to-read). Recommended surgical. Ricardo agreed.

- **Audit-trail doc format.** 3-option question to Ricardo (standalone proposal-style vs appendix on audit report vs journal-only). Recommended standalone. Ricardo agreed.

- **End session vs continue.** Recommended end (clean context for next session's execution). Ricardo agreed; asked for the trail doc explicitly to support future audits.

## What I learned this session

- **Verdict-rubric mismatch is a real signal.** When the auditor's quantitative rubric ("7 HIGH = YELLOW-large = rewrite") disagrees with their qualitative recommendation ("inline patches → GREEN"), the recommendation captures information the rubric doesn't (architectural soundness, fix locality). Worth surfacing the tension explicitly rather than blindly following one or the other.

- **The pkill-P / passphrase-hang / on-disk-vs-staged bugs are a class.** They're test scripts that *appear* to test the closure but exercise a different path than the production code. The pattern: write the test, watch it FAIL in red, write the prod code, watch it PASS — but never ask "could this test PASS even if the prod code were completely broken?" Findings 2 and 3 both share this shape. Worth flagging in future plan reviews: every load-bearing test should be paired with a "false-PASS adversarial check."

- **Signal-attachment as a delivery primitive.** JP Light-mode means git-on-his-side is optional. Signal is the natural cross-boundary channel for small artifacts that need to flow without committing to a public-ish path. The C2 reverse-roundtrip fix establishes the pattern; other future flows can reuse it (sending recipients-file updates, sentinel verifications, transient encrypted shares).

- **Audit-response notes in plan headers pay off.** The "Re-audit response (2026-05-14)" block at the top of Plan 01a (lines 27-37) makes the patch lineage obvious to anyone opening the plan — no need to cross-reference commits or audit reports first. Worth adopting as a convention for any plan that gets re-audited.

## Open follow-ups (for future me)

- **Deferred MEDIUMs (5) + LOWs (3)** from the audit report — Findings 8-15. Listed in the patch-verification-trail doc with brief rationale for each deferral. None block Plan 01a execution.
- **Verify the patches don't introduce new bugs.** The patch-verification-trail doc's last section ("What this trail does NOT cover") flags three specific unknown-unknowns: the `MODE="git-hook"` hook branch under partial-stage-with-deletion; the broader scope of `git add -A` in Task 7; the `AGE_ERR=$(mktemp)` file living outside `/dev/shm` and not shred-cleaned. A future re-audit should treat these as new code under scrutiny.
- **`subagent-driven-development` next session.** Open the next session with Tasks 1-11 of the patched Plan 01a. The plan is now execute-ready. Pause cleanly between Task 11 and Task 12 for the JP coordination gate.

## Files written this session

```
00_META/proposals/2026-05-14_plan-01a-audit-report.md             (NEW)  ─ committed in 6ca022c
00_META/plans/2026-05-14_plan-01a-foundation.md                   (MOD)  ─ committed in 6ca022c
tasks.json                                                        (MOD)  ─ committed in 6ca022c
00_META/proposals/2026-05-14_plan-01a-patch-verification-trail.md (NEW)  ─ session-end commit
00_META/journal/2026-05-14_plan-01a-reaudit-and-patches.md        (NEW, this file) ─ session-end commit
STATUS.md                                                         (MOD)  ─ session-end commit
CHECKPOINT.md                                                     (MOD)  ─ session-end commit
```

No edits to CLAUDE.md / GEMINI.md / README.md → no `00_META/CHANGELOG.md` entry. No Gemini handoff this session — both handoff files remain TEMPLATE.

## Next session opener (suggested)

Ricardo types "Start Session." Claude reads CHECKPOINT.md (rewritten this session) + STATUS.md + tasks.json + calendar.json + this journal entry, then proposes the Batch 3 step 2 sequence:

1. Confirm `t-plan-01a-execute` is the next critical action (it is).
2. Verify the working tree is clean and on `main` (it should be).
3. Optionally run the patch-verification-trail's "one-pass spot-check" block to confirm all 7 HIGH patches are still live before starting execution.
4. Dispatch Plan 01a execution via `superpowers:subagent-driven-development`. Tasks 1-11 in one session (~4-6h); pause cleanly at Task 12 gate; resume on JP age pubkey landing via Signal.
5. After Tasks 1-11 commit cleanly: optional mid-execution checkpoint update.
6. When JP key lands: run Tasks 12-18; tag `v0.1a-foundation`; close `t-plan-01a-execute`.

If the patch-trail spot-check FAILs at any line, do NOT proceed to execution — investigate the regression (something in the working tree drifted between sessions).
