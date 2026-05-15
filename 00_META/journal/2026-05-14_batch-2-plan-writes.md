# 2026-05-14 — Batch 2 plan-writes (01a + 01b + 01c shipped)

**Session type:** work · plan-writing
**Duration:** ~3 hours focused
**Agent:** Claude (Opus 4.7, 1M context) at root in driver session with Ricardo

## Session shape

Single-purpose session: take the three Plan-01 split headers from `00_META/plans/README.md` (locked in Batch 1c commit `d5ebbf9`) and expand each into a full task-by-task implementation plan via the `superpowers:writing-plans` skill. The CHECKPOINT baton from the prior session laid out the per-plan audit-finding inheritance precisely; Ricardo's session opener was a single line ("Procede with the next step of the setup"), which I read as authorization to run the entire Batch 2 sequence end-to-end without intermediate checkpoints.

Three plans written, three commits pushed to Gitea origin. Working tree clean at session end.

## What we built

**Commit `7d588ed` — Plan 01a (Repository Foundation: scaffold + identity + crypto).** 18 tasks · 3319 lines at `00_META/plans/2026-05-14_plan-01a-foundation.md`. Coverage:

- Pre-flight checks (cwd, clean tree, age installed, pandoc installed, jsonschema + PyYAML available)
- Task 1: 3-bucket folder scaffold via single mkdir + .gitkeep pass
- Task 2: Comprehensive .gitignore (F23) with TDD coverage test
- Task 3: Pre-commit secret-scan hook (basic; full surface in 01c) — TDD with planted-secret + clean-file harness
- Task 4: pipeline/clients/_template/ — 12 stations + 3 cross-cutting (F16, F19) with state.json template + checkpoint placeholder + README
- Task 5: JSON Schemas — nexostrat-tasks-v1 + nexostrat-calendar-v1 (F21) + validator script
- Task 6: 7 per-machine YAML profiles (F13, F26) + bootstrap-machine.sh skeleton
- Task 7: Move parked skills 00_META/skills/ → skills/<NN>_<name>/
- Task 8: Migrate questionnaires (F15) — pandoc Plan_Maestro_*.docx → md + archive originals + move Consultoria PDF
- Task 9: 00_PARTNERSHIP/ canonical files (CONFLICT_PROTOCOL, REVENUE_DISTRIBUTION, ROLES, KPIs, cost-sharing, qualified-prospect, raised_hand_log)
- Task 10: vault/ scaffold + sensitive_index.md template (F10 namespace split documented)
- Task 11: Verify Ricardo's age setup (terrain-prep VERIFY only)
- ⏸ JP coordination gate cleanly marked between Tasks 11-12
- Task 12: Add JP pubkey to recipients (C2)
- Task 13: Bidirectional encrypt-decrypt roundtrip (both founders)
- Task 14: Create secrets.env.age (encrypted to both recipients)
- Task 15: Implement run-with-secrets.sh with C1 fix (explicit cleanup, no exec leak) + leak-detection TDD harness
- Task 16: infra/secrets/MANIFEST.md (plaintext audit surface)
- Task 17: Sign + encrypt + commit partnership PDF (F5) + markdown summary
- Task 18: Final verification + tag v0.1a-foundation

**Commit `42c4c4a` — Plan 01b (Mirrors + warm-standby).** 12 tasks · 1751 lines at `00_META/plans/2026-05-14_plan-01b-mirrors.md`. Coverage:

- Pre-flight (Plan 01a tag, Gitea origin, GitHub + Codeberg account/SSH/repo, systemd 248+, rsync, Tailscale)
- Task 1: Verify Gitea bare-repo path + draft 00_GOVERNANCE/system_map.md (F22-subset, F25)
- Task 2: GitHub mirror remote + PAT in secrets.env.age + first push
- Task 3: Codeberg mirror remote + PAT (F7) + first push
- Task 4: nexostrat-mirror-github systemd path-watcher (C4 fix replacing the dead Gitea-internal hook) + mirror-push.sh + install-systemd-units.sh
- Task 5: nexostrat-mirror-codeberg path-watcher (F7) — same pattern, different remote
- Task 6: 60-second mirror window stopwatch verification
- ⏸ Warm-standby gate marked between Tasks 6-7
- Task 7: Standby host inventory — fill placeholders in hp-standby.yaml
- Task 8: Standby initial clone + install age key + verify decrypt
- Task 9: nexostrat-warm-rsync timer + service (nightly 03:00 America/Tijuana, Persistent=true, RandomizedDelaySec=300) + warm-rsync.sh reading STANDBY_HOST from .gitignored per-machine config
- Task 10: Real warm-rsync smoke test (F24 — replaces --dry-run false-positive)
- Task 11: HP-down failover runbook at docs/runbooks/hp_down.md + dry-run
- Task 12: Final verification + tag v0.1b-mirrors

**Commit `508c160` — Plan 01c (Personas + hooks + smoke test) + master plan index README update.** 11 tasks · 2047 lines at `00_META/plans/2026-05-14_plan-01c-personas.md`. Coverage:

- Pre-flight (Plan 01a + 01b tags exist, clean tree, Python stdlib check)
- Task 1: 9 canonical shared stanzas at 00_META/shared/ (rule1, session_start, session_end, session_output_format, memo_protocol, gemini_handoff, vault_access, backup_posture, change_log) + STATUS.md template + F20 leak audit + F27 follow-through
- Task 2: inline_includes.py — ~50 lines stdlib Python with `--check` mode for drift detection (C3 fix) + TDD test harness
- Task 3: nexostrat-memos.py — ~80 lines stdlib Python (F8) + smoke tests
- Task 4: checkpoint-mtime-check.sh (R4 concurrent-session protection)
- Task 5: Founder root persona files regenerated via inliner (CLAUDE.md + GEMINI.md)
- Task 6: Skills-Master persona files (skills/CLAUDE.md + skills/GEMINI.md + CHECKPOINT placeholder + 00_META/inbox scaffold)
- Task 7: Client-Owner persona files (pipeline/CLAUDE.md + pipeline/GEMINI.md with F10 vault scope) + same scaffold
- Task 8: Pre-commit hook surface — orchestrator + 4 sub-hooks (secret-scan reuse, vault-age-only, docs-pair-basic, checkpoint validation per ADR-031)
- Task 9: F27 follow-through final sweep — grep for Hosted refs across the repo
- Task 10: Integration smoke test smoke-test.sh (R2 rich version) — 6 sub-tests covering crypto round-trip, mirror push + 60s GitHub HEAD parity, warm-rsync real trigger, run-with-secrets leak, inliner drift across 6 persona files, schema validation
- Task 11: Run smoke test, verify GREEN, tag v0.1-foundation

Plus the master plan index `00_META/plans/README.md` was updated in the same commit to mark all three rows READY (was DRAFT-PENDING), populate the file-column links, fix the inline `**File:**` lines under each per-plan header, and add a Batch-2 changelog row documenting plan sizes + audit-finding inheritance per plan.

## What the work looked like in practice

The `superpowers:writing-plans` skill was invoked once at the top of the session and its discipline applied across all three writes: header (Goal + Architecture + Tech Stack), file-structure map up front, bite-sized tasks with TDD for testable code (the inliner, the leak detector, the schema validator) and verification-only checks for pure scaffold work (folder creation, YAML profiles, README writing). Each task ends with a clean `git commit` step so per-task history stays granular at execution time.

Critical judgment calls during the writing pass:

1. **Task granularity vs amendment-plan estimate.** The amendment plan said ~15 tasks for 01a, ~10 for 01b, ~10 for 01c. I landed at 18/12/11. Slightly over for 01a but the audit-finding count plus the JP-coordination split made consolidation feel forced. Each task is a clean commit-sized unit; merging would have produced lumpy commits.

2. **Persona templates with `{{include}}` markers.** C3 fix was clear about needing the inliner. The persona files in 01c are templated at `00_META/templates/{<scope>}_{CLAUDE,GEMINI}.md.tmpl` and the actual `CLAUDE.md` / `GEMINI.md` files are generated. This means the existing terrain-prep root `CLAUDE.md` (which was hand-written, not template-generated) gets regenerated during 01c Task 5. The substantive content carries over — just the structure flips to template-driven.

3. **Coordination gates as first-class plan content.** Both 01a (JP age key gate) and 01b (physical second host gate) have explicit `⏸ GATE` sections inside the plan with a "what to do when pausing" + "what to do when resuming" pair. This treats coordination latency as part of the plan structure rather than a side-effect that derails execution.

4. **Three commits, not four.** The CHECKPOINT baton said "~3 commits expected." I considered splitting the master-index README update into a 4th commit, but folding it into the 01c commit kept the narrative cleaner (the README update is logically "all three plans are now ready," which is the same milestone 01c completes).

5. **Single-shot delivery.** Ricardo's prompt was minimal ("Procede with the next step of the setup"). I read this as authorization for the full Batch 2 sequence per the CHECKPOINT baton — three plans, three commits — without checkpointing between plans. The Aurora HTML session on 2026-05-14 had already established this single-shot pattern; this session followed it. The end-of-session "excelent work!" feedback validated the call.

## Surface-area discoveries

- **JSON Schema additionalProperties=false constraint will need careful handling at Plan 01a execution.** The schema I defined in Task 5 forbids fields outside the named set. The existing tasks.json (current state) uses only allowlisted fields, but any future migration needs to treat the schema as a hard contract. Captured in the plan as "stop and surface to Ricardo" if validation fails on existing data.

- **The C1 leak test had to be carefully designed.** A naive "check for files in /dev/shm" misses the case where the wrapper IS using /dev/shm during the wrapped command's lifetime — that's correct behavior, not a leak. The leak is: files left over AFTER the wrapper exits. Plan 01a Task 15 Step 5 makes this distinction explicit in the smoke-test code.

- **Skills folder relocation has implications for the existing 4 skills.** Plan 01a Task 7 does a `git mv` per skill from `00_META/skills/{company-analyst, industry-analyst, competitor-analyst, discovery-meeting}/` to `skills/{01_company_analyst, 02_industry_analyst, 03_competitor_analyst, 06_discovery_meeting}/`. The skills' internal contents (prompts, references, manifests) stay intact — only the parent path changes. Any external references to the old path will break; nothing currently has external references because terrain prep is the only thing that put them at `00_META/skills/`.

- **The Founder root CLAUDE.md regeneration is non-trivial.** The current hand-written CLAUDE.md is ~15 KB with detailed session protocols, strict rules, vault access, etc. The Plan 01c Task 5 regeneration via inliner aims to preserve substantive content while flipping structure to template-driven. There's a real risk of losing nuance in translation. The plan acknowledges this — Step 5 Sanity-check via `git diff` is explicit.

## What's queued for next session

**Batch 3 step 1: Re-audit Plan 01a.** Same dispatch pattern as 2026-05-14 audit (general-purpose agent with risk-auditor persona inlined; or invoke `risk-auditor` subagent type directly per the second-opinion option mentioned in Step 1). Target GREEN. If YELLOW with ≤3 amendments, fix inline. If more, re-write affected tasks.

After 01a re-audit lands GREEN: execute via `superpowers:subagent-driven-development`, tag `v0.1a-foundation`. Then 01b re-audit, 01b execute, tag `v0.1b-mirrors`. Then 01c re-audit, 01c execute, tag `v0.1-foundation` (the original Plan-01 milestone).

JP-side coordination items remain in flight via Signal — drip-feed expected over the next several days. Independent of next session's main work (re-audit doesn't need JP).

## Memory hygiene

No new durable memory entries this session. Existing memories (no Brain refs, drop n8n entirely, Notion via JP personal, user role) were active throughout. The single-shot delivery pattern is now twice-validated (Aurora HTML + Batch 2 plan-writes) but doesn't warrant a separate memory yet — it's emerging as Ricardo's preferred mode for large-mandate sessions, but the data points are still few.

## Files modified this session

**New / created:**
- `00_META/plans/2026-05-14_plan-01a-foundation.md` (commit `7d588ed`)
- `00_META/plans/2026-05-14_plan-01b-mirrors.md` (commit `42c4c4a`)
- `00_META/plans/2026-05-14_plan-01c-personas.md` (commit `508c160`)
- `00_META/journal/2026-05-14_batch-2-plan-writes.md` (this file, session-end commit)

**Modified:**
- `00_META/plans/README.md` (commit `508c160` — 4 surgical edits + Batch-2 changelog row)
- `STATUS.md` (session-end commit)
- `tasks.json` (session-end commit)
- `CHECKPOINT.md` (session-end commit)

**No edits this session to:**
- CLAUDE.md / GEMINI.md / README.md → no `00_META/CHANGELOG.md` entry needed
- `00_META/handoff/` → no Gemini handoff this session
- Spec, ADR ledger, secrets — Batch-2 was pure plan-writing
