# Brain Bot Platform — Session B (Nexostrat audit) executed

**Date:** 2026-05-21
**Session lead:** Ricardo (Founder persona at /srv/Nexostrat/)
**Claude:** Opus 4.7 (1M context)
**Duration:** ~2.5 hours
**Closing phrase:** "Great work! Finish session"

## What this session was about

Ricardo asked for an assessment: should Nexostrat's planned Telegram bot fold into the central Brain Bot Platform hub designed Brain-side on the same date, or should Nexostrat build an exclusive bot? Both reference docs already existed Brain-side — the design spec (`2026-05-21_brain_bot_platform_design.md`, commit `0b53a9c`) and the companion audit protocol (`2026-05-21_brain_bot_platform_audit_protocol.md`, commit `7ea48ec`). The audit protocol explicitly had a reserved `## Session B — Nexostrat audit` block awaiting Nexostrat-persona input. So the real task wasn't to design from scratch but to execute Session B from the Nexostrat side.

## Decision

**Option A — central hub, shared infrastructure** with two binding amendments:

1. Separate Telegram token (`NEXOSTRAT_BOT_TOKEN`) — already in the Brain design, no deviation.
2. Nexostrat-owned OpenAI API key with its own budget envelope — amends Brain design §11 from a single global $10/month cap to per-key buckets. Personal+Mevillo keep sharing Ricardo's key under the existing cap; Nexostrat gets an independent $20/month envelope.

Rejected alternatives: Option B (exclusive Nexostrat hub — ~3-4 weeks duplicate infra), Option C (hybrid shared-libs/separate-process — worst of both worlds for a 2-bot situation).

Captured as ADR-039 in the founding spec ADR table + full body at `00_GOVERNANCE/adr/ADR-039-bot-tenant-in-brain-hub.md`. Supersedes ADR-020 (Independent bot codebase, 2026-05-11).

## What Session B's notes actually contain

Twelve checklist items addressed:

- **B1** ✓ Bot identity `Nexostrat` / `@NexostratBot`
- **B2** ✓ Writers Ricardo DM + JP DM + JP+Ricardo group; both Telegram IDs in hand
- **B3** ✓ Group chat per-day JSONL, indefinite retention, JP consent
- **B4** ⚠ Mon 08:00 + Thu 07:00 TJ canonical; flagged: ad-hoc + client-meeting routing pattern needs `client_slug:` field in event schema
- **B5** ⚠ T-2h brief expanded to 6 blocks (recap + tasks + chat extracts + attendance + cross-inbox memos + active-client pipeline state); brief templates must live as separate editable files with documented data sources
- **B6** ⚠ Strict-mode task review relaxed to hybrid-by-confidence (≥0.85 auto-write + audit log; <0.85 review prompt)
- **B7** ⚠ Calendar interim posture: Ricardo's personal Google Calendar with mandatory Nexostrat-scope filter (JP can read the cache file)
- **B8** ⚠ FIVE concrete enforcement gaps raised (Ollama logs, OpenAI key routing, events subscription model, Whisper logs, manifest validator drift)
- **B9** ✓ Internal minutes at `/srv/Nexostrat/meetings/<slug>/`; client minutes at `pipeline/clients/<slug>/transcripts/<date>_minutes.md`
- **B10** ⚠ Spanish primary + English mirror; drift audit checks both
- **B11** ✓ Four `schedule.yaml` entries (07:30 daily morning brief, Sun 19:00 weekly review, Fri 17:00 EOW pipeline status, daily 18:00 inbox nudge)
- **B12** ✓ Hub owns lifecycle, single systemd unit

Eight OFF-CHECKLIST findings (B13–B20) flag follow-ups that Brain Architect Session C must absorb or Nexostrat must execute pre-launch:

- B13: per-tenant API key + per-key budget envelopes (Brain spec amendment)
- B14: ADR-020 supersession (Nexostrat-side, done in this session)
- B15: Strict Rule #4 clarification (Nexostrat-side, done in this session)
- B16: weekend desktop-on decision (blocks Mon 08:00 brief)
- B17: confidence calibration corpus (Plan 04 prerequisite)
- B18: client-meeting integration in Plan 08 (Meeting Pipeline)
- B19: firm-owned Telegram account for `@NexostratBot`
- B20: JP-Light read paths (`/manual` and `/audit_tasks` Telegram commands)

## Files written this session

Brain-side (cross-scope edit per audit-protocol allowance):
- `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md` — Session B Notes block (was empty placeholder). Commit `68a702f`, pushed to Brain Gitea.

Nexostrat-side:
- `CLAUDE.md` — Strict Rule #4 clarified (shared bot infrastructure permitted; references in Nexostrat artifacts still prohibited)
- `00_META/proposals/2026-05-13_nexostrat-system-design.md` — ADR-020 marked superseded by ADR-039; ADR-039 row added
- `00_GOVERNANCE/adr/ADR-039-bot-tenant-in-brain-hub.md` — new full ADR body (context, decision, options table, consequences, mandatory follow-ups, anti-decision, reversal trigger)

Both bundled in commit `0293ed8` pushed to Gitea origin; mirrors (GitHub + Codeberg) fire automatically via Plan 01b path-watcher.

Session-end (this commit will include):
- `STATUS.md` — session 10 block prepended
- `tasks.json` — `updated` bumped; 5 new tasks added (B19 critical / B16 high / B17 high / Plan 04 update high / B18 medium)
- `00_META/journal/2026-05-21_brain-bot-tenancy-decision.md` — this file
- `00_META/CHANGELOG.md` — 2026-05-21 row added
- `CHECKPOINT.md` — rewritten baton

## Process notes

The audit protocol's design — pre-reading + checklist + questions + Notes-block-to-fill — proved efficient. The four-question-batch structure (identity/cadence/brief/manual) collapsed what could have been an hour of single-question brainstorming into ~15 min of structured Q&A. The protocol's "cross-scope edit allowance" (root CLAUDE.md Strict Rule #1, operator-driven) made it natural to write Nexostrat's findings directly into Brain's audit doc rather than producing a separate memo Brain-side would then have to integrate.

The "load-bearing tension" framing surfaced the right conflict early: Strict Rule #4 ("No /srv/brain references") + ADR-020 ("Independent bot codebase") versus the Brain design's tenant model. Ricardo's "open to sharing infrastructure, strict on separate Telegram token, separate LLM API key" pinned the architecture in one sentence; everything downstream was operational detail.

Verdict at session end: feasibility + convenience both confirmed. The amendments are tractable (per-key budget tracking is ~20 LOC on the Brain side; separate token is already in the design; Strict Rule #4 clarification + ADR-020 supersession are documentation changes done in this commit). The mandatory pre-launch items are concrete tasks with owners and deadlines.

## Decisions locked this session

1. **Central hub adopted (ADR-039).** Nexostrat bot runs as tenant 3 in `/srv/brain-hub/`. Reversal trigger documented in ADR-039: cross-tenant leak, hub unreliability, JP request, or Brain's isolation tests degrading.
2. **Strict Rule #4 reinterpreted.** Shared infrastructure permitted; references in Nexostrat-owned artifacts still prohibited. Cross-references to Brain (like this journal's pointer to `/srv/brain/00_META/governance/plans/`) are governance-traceability, not infrastructure coupling.
3. **Brief templates must be editable + documented.** Ricardo's emphasis: templates live as separate files under `/srv/Nexostrat/00_META/templates/` with a `README.md` that names every block's data source, so JP or any future contractor can edit them safely without reading code.
4. **Auto-execute Nexostrat queue items at 23:00 EOD sweep.** Using the Nexostrat-owned OpenAI key, capped at Nexostrat's own budget envelope. Same flow as Personal+Mevillo, different financial surface.
5. **Telegram-only at Stage 1.** No parallel email/Slack channel for JP — the FOSS dashboard from Plan 02 will eventually surface a web view but isn't a notification channel.

## Memory updates

None new. Existing memories applied — particularly:
- `feedback_do_it_right_do_it_once` — drove the choice to write a full ADR-039 body rather than a one-line ADR table row pointing nowhere
- `feedback_complete_or_nothing` — drove the decision to bundle CLAUDE.md amendment + ADR-020 supersession + ADR-039 body + audit notes + commits all in one session, rather than punting any piece to a future session
- `feedback_honestidad_brutal_evaluacion` — drove the five enforcement gaps list (B8) instead of waving the hand at isolation

## What's next

Critical path unchanged: **Trixx Logistics meeting 2026-05-25** is still T-4 days; Skill 05 post-Trixx still owed; Chunk B follow-ups + Chunk C still queued. The Brain Bot Platform decision lives on the architectural parallel track — Brain Architect's Session C (cross-cutting governance) is now unblocked and will likely run within the next week. Plan 04 description update is a small lift that should happen the next time the master plan index is touched for any reason.

Next session opens with: Ricardo's choice among the usual options (Chunk B systemd-creds, Chunk C, post-Trixx Skill 05, Plan 02b write, Desktop PC stack install, t-plan-01a-jp-and-tty-deferred TTY items) plus the new Brain-bot-related items if Brain Architect Session C lands.
