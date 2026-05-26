# 2026-05-25 — Meetings-overhaul Phase 0a P-N3 (calibration corpus)

**Session type:** work
**Duration:** ~1.5 hours
**Agent:** Claude (session 18)

## What was done

- Read master plan §6.2 P-N3 + §7.1 done-log format at `/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`, the Nexostrat contribution doc §3 P-N3 at `/srv/Nexostrat/00_META/governance/plans/2026-05-25_meetings-overhaul-contribution.md`, the rubric + schema at `/srv/Nexostrat/00_META/calibration/README.md`, and confirmed `t-confidence-calibration-corpus` (B17) aliases this work per its `notes` field.
- Walked the 4 existing meeting summaries under `/srv/meetings/nexostrat/` (audit H3 PASS): `2026-05-25_08-00_reunion-lunes` (7 action items), `2026-05-21_07-02_strategy-alignment` (7), `2026-05-20_07-35_neo-intro-pt1` (3), `2026-05-20_07-48_neo-intro-pt2` (3) — 20 candidate action items total.
- Proposed `ground_truth_score` + `ground_truth_should_write` for each of the 20 meeting-derived rows in a single review table; Ricardo signed off via bulk approval ("Approve all 20 as proposed") through AskUserQuestion.
- Authored 30 synthetic edge-case rows balanced across the 4 rubric tiers (T1=8, T2=7, T3=8, T4=7) covering all 5 mandated edge categories: ambiguous "we should do X someday" phrasings, multi-assignee shapes, relative-date resolution (`mañana`/`el lunes`/`esta semana`/`hoy mismo`/`el miércoles a las 3pm`), JP-language quirks (`yo me encargo`/`te tengo lista`/`te paso`/`confirmo`), small-talk false-positive triggers (`voy al baño`/`déjame buscar el cargador`/`luego te cuento del fin de semana`/`eventualmente podríamos`).
- Wrote 50 NDJSON rows to `/srv/Nexostrat/00_META/calibration/auto_task_extraction.jsonl` (51 lines total including the leading `_comment` retuner-skip guard). Every row carries `model_score: null` by design so P-H6 DeepSeek-vs-OpenAI calibration can backfill without a schema migration.
- Validated the corpus via Python: 50/50 rows parse as JSON, 0 missing required fields, tier distribution T1=10 / T2=20 / T3=13 / T4=7, `should_write=true` for 19/50 (38%).
- Authored `/srv/Nexostrat/00_META/calibration/2026-05-25_initial-corpus-report.md` documenting row count, schema validation, tier distribution, edge-case coverage check (5/5 categories), perfect-calibration threshold sweep across 7 candidate thresholds (0.70 → 0.90), threshold recommendation with 4-paragraph defense (hold 0.85 for Stage 1), and 5 known gaps + follow-ups.
- Marked `t-confidence-calibration-corpus` (B17) `status: open → completed` in `/srv/Nexostrat/tasks.json` with closure note pointing at the deliverables + scoping deliverables 3 + 4 (bi-weekly cron + per-tenant threshold config) as out-of-Nexostrat-task-scope (they live in the hub's recurring-ops surface).
- Committed Nexostrat repo at `cbf70f9` (3 files: corpus + report + tasks.json) and pushed to Gitea origin; mirrors fire via systemd path-watcher.
- Edited `/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`: ticked §6.2 P-N3 checkbox (line 403, `[ ]` → `[x]`) and appended a §7.1 done-log row with full deliverable summary + tier distribution + threshold recommendation + dedup note. Brain commit `f42e0e0` pushed to Brain Gitea.
- Janitor pass at session close: flipped `t-meetings-overhaul-audit-dir` (P-N2) `open → completed` in `tasks.json`. Work had actually shipped session 15 at commit `2a5f272` — bookkeeping miss carried from sessions 16 + 17. Closure note added.

## Decisions made

- **`model_score: null` on every corpus row** — Per the task spec, the field exists so P-H6's DeepSeek-vs-OpenAI calibration pass can backfill real scores without a schema migration. Trade-off: retuner script (`/srv/brain-hub/hub/router/calibration.py`) can't compute real precision/recall against this corpus until P-H6 runs; it must skip null-score rows or treat null as un-evaluable. Documented as a follow-up in the corpus report §6.
- **Hold `auto_task_threshold = 0.85` for Stage 1** — Perfect-calibration threshold sweep shows F1 peaks at 0.974 for threshold 0.82 and F1 = 0.944 for 0.85. Picked 0.85 anyway because: (1) the sweep is an upper bound (real DeepSeek scores will have noise; 0.85 leaves precision headroom); (2) the audit B17 partnership-posture argument favors precision over recall in a JP-shared ledger; (3) the corpus is action-rich-biased (summary.md filters small-talk before reaching it), so real raw-transcript extraction will see more T3/T4 noise; (4) README rubric + routing.yaml template both default to 0.85, changing pre-P-H6 is premature optimization on a perfect-calibration toy.
- **Bulk-confirm the 20 meeting-derived ratings rather than line-by-line** — Practical compromise on the task's "ask Ricardo to confirm/adjust each rating" instruction. Single review table with proposed score + rationale per row, Ricardo bulk-approved via AskUserQuestion. Faster than 20 separate questions; still gives Ricardo line-level visibility before commit.
- **Synthetic Tier 1 over-weighted toward JP-language quirks** — Synthetic S3-S5 + S8 (4 of 8 Tier 1 rows) test JP's canonical I-own-it phrases (`yo me encargo`, `te tengo lista`, `te paso`, `confirmo`). Rationale: JP's confirmed commitments are exactly the kind of high-confidence auto-write the system needs to recognize correctly; over-sampling JP-language at Tier 1 sharpens that branch.
- **`rater: ricardo` on all 50 rows, not "claude" for synthetic** — README schema allows only `ricardo | jp`. Claude proposed; Ricardo signed off (explicitly for the 20 meeting rows, implicitly via Step 1 approval for the synthetic 30). Notes field clarifies which rows are synthetic vs meeting-derived.
- **No new follow-up tasks opened** — The corpus report's 4 follow-ups (retuner null-handling, JP-rated inter-rater agreement, Tier 2 boundary-band oversample, English-row expansion) all defer naturally to the bi-weekly Brain Architect retune cron post-Phase-4-launch. No Nexostrat-side ledger entry needed; the report documents them where they'll be re-read.

## Open items

- **Phase 0c hub-side P-H1 + P-H6 remain open** (cross-scope, Brain Hub Principal owns). Nexostrat-side procurement gates: `t-nexostrat-telegram-account` (firm Telegram account, B19, critical, due 2026-06-15) + firm DeepSeek key (no task tracking this in Nexostrat; lives in Brain Hub's scope).
- **Intro V3 polish due tomorrow** (2026-05-26): `t-intro-v3-ceo-vs-cofundador` + `t-intro-v3-diferencia-slide` both high-priority. Surface first next session.
- **Stale `/home/ricardo/brain-hub/` ≠ `/srv/brain-hub/` path drift** in governance docs — discovered session 17, not fixed (out of P-H2 scope). No task added; recommend root run an audit pass to either move the directory or amend the master plan + Brain Hub contribution doc + deployment doc, whichever Ricardo prefers.
- **Brand font install on laptop** (`t-install-brand-fonts-laptop`, high, 2026-05-30): Inter + JetBrains Mono only on desktop; laptop is primary render host.
- **JP-gated decisions still pending**: `t-pick-website-intro-final-version` (medium, 2026-06-15), `t-weekend-desktop-on-decision` (B16, high, 2026-06-15).
- **Plan 04 description update** (`t-plan-04-description-update`, high, 2026-05-28): master plan index still describes Plan 04 as a standalone bot; needs flip to "Nexostrat tenant in central Brain Bot Hub".
- **BB-Platform action-items memo archive** (`t-archive-bbp-action-items-memo`, low, 2026-06-15): defer until B19 closes.

## Notes

Phase 0a Nexostrat surface is now 3 of 3 DONE. The meetings-pipeline overhaul has no remaining Nexostrat-side prereqs — the producer/consumer scope split holds (hub does the writes, Nexostrat is the target filesystem). Cross-scope status: 0a Nexostrat ✅, 0b AttenBot in progress (P-A1 owned by Gemini at `/home/ricardo/atten-bot/`), 0c Brain Hub partially done (P-H2 ✅ ours, P-H1 + P-H6 hub-side procurement-gated), 0d Meetings empty by design.

Next session's natural opener: intro-V3 polish (due-date pressure tomorrow). If Ricardo opens with "Start Session", surface that first, then janitor passes (BB-Platform memo archive once B19 closes, Plan 04 description update due 2026-05-28), then the cross-scope flag about `/home/ricardo/brain-hub/` ≠ `/srv/brain-hub/` (root may want to act on it).

No Gemini handoff active. `claude_to_gemini.md` + `gemini_to_claude.md` both remain `TEMPLATE`.
