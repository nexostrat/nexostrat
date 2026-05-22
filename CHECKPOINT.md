# CHECKPOINT — root (Founder)

**Updated:** 2026-05-21T17:38:51-07:00
**By:** ricardo (via Claude Code session 10 at /srv/Nexostrat/)
**Persona:** Founder
**Session topic:** Assess feasibility + convenience of a central Telegram hub (Brain Bot Platform) vs an exclusive Nexostrat hub. Execute Session B of the Brain-side audit protocol (which already had a reserved `## Session B — Nexostrat audit` Notes block awaiting Nexostrat-persona input). Land ADR + Nexostrat-side amendments + tasks for pre-launch follow-ups.

## What just happened (last session — read once, don't re-litigate)

Single ~2.5-hour arc driven by Ricardo's framing: "assess the possibility to implement the general Telegram hub with the Telegram bot we were planning to implement for Nexostrat... see if it's possible and convenient to do a central Telegram hub or if it's better to create an exclusive Telegram hub for Nexostrat." The Brain side had already designed the central hub on the same date (`/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_design.md` commit `0b53a9c`) with a companion audit protocol (commit `7ea48ec`) reserving a `Session B — Nexostrat audit` block exactly for this assessment. Session B is the canonical mechanism for the question; the right answer was to execute it from this side.

**Architecture decision arc:**

1. Read Brain design spec + audit protocol end-to-end (~50 KB combined).
2. Surfaced the load-bearing tension: Nexostrat CLAUDE.md Strict Rule #4 ("No /srv/brain references") + ADR-020 ("Independent bot codebase", 2026-05-11) versus the Brain design's tenant model.
3. Three options presented (A central hub, B exclusive Nexostrat hub, C hybrid shared libs + separate process) with trade-offs table. Ricardo's answer in one sentence: "open to sharing infrastructure, strict on a different Telegram token, we can use a different LLM API key." That pinned Option A + 2 amendments.
4. Walked Session B's 12 checklist items + 8 questions in four batched `AskUserQuestion` calls grouped by topic (identity/cadence/brief/manual). Plus one final batch for B8 isolation stress-test + Q8 parallel JP channel.

**Artifacts produced (all committed + pushed by session end):**

Brain-side (cross-scope edit per audit-protocol allowance + Strict Rule #1):
- `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md` — Session B Notes block populated. 12 checklist items addressed (B1-B12, ✓ or ⚠), 8 questions answered (Q1-Q8), 8 OFF-CHECKLIST findings raised (B13-B20). Brain commit `68a702f` pushed to Brain Gitea.

Nexostrat-side:
- `CLAUDE.md` — Strict Rule #4 clarified (shared infrastructure permitted; references in Nexostrat artifacts prohibited; cross-refs in ADRs count as governance-traceability not infrastructure-coupling).
- `00_META/proposals/2026-05-13_nexostrat-system-design.md` — ADR-020 marked Superseded by ADR-039; ADR-039 row added in numeric order.
- `00_GOVERNANCE/adr/ADR-039-bot-tenant-in-brain-hub.md` — new full ADR body.
- Nexostrat commit `0293ed8` pushed to Gitea origin; GitHub + Codeberg mirrors fire via path-watcher.

**Result:**

- Brain Bot Platform Session B closed; Brain Architect Session C unblocked.
- Nexostrat bot has a locked architecture (tenant in central hub) + 8 mandatory pre-launch follow-ups tracked.
- ADR-020 cleanly superseded with explicit reversal trigger documented in ADR-039.
- 5 new tasks added with dates aligned to Stage 1 launch window (2026-06-30 to 2026-07-15).

## Decisions locked this session

1. **Option A — central hub adopted (ADR-039).** Nexostrat bot runs as tenant 3 in `/srv/brain-hub/` alongside Personal + Mevillo. Strict isolation enforced by ScopedFS multi-scope + manifest validator + scope-keyed event routing. Reversal trigger documented: cross-tenant leak, hub unreliability >5% of meetings without brief, JP request, or Brain isolation tests degrading → write ADR-04X "Nexostrat exits Brain Bot Hub" + ~2-week migration.

2. **Per-tenant OpenAI API key with per-key budget envelopes.** Amends Brain design §11 from single global $10/mo cap to per-key tracking. Personal+Mevillo continue sharing Ricardo's key under existing cap; Nexostrat gets independent envelope (proposed initial $20/mo, raised as firm revenue justifies). `LLMBudget` ledger schema gains `api_key_id`. Budget warnings via Nexostrat bot to JP+Ricardo group (not Personal bot — JP must see firm API spend in firm channel).

3. **Strict Rule #4 reinterpreted, not weakened.** Shared bot infrastructure at `/srv/brain-hub/` permitted as a documented exception; references in Nexostrat-owned artifacts (specs, docs, code, journal entries under `/srv/Nexostrat/`) still prohibited. ADR-039's cross-reference to `/srv/brain/` is governance-traceability, the documented exception.

4. **Brief templates editable + documented.** Per Ricardo's directive: T-2h pre-meeting brief templates live as separate files under `/srv/Nexostrat/00_META/templates/` with a `README.md` naming every block's data source. Hub plugin reads templates at render-time so edits apply immediately. JP or any future contractor can edit safely without reading code.

5. **Hybrid-by-confidence task review (relaxes Brain design Walkthrough 3's strict-mode).** Meeting-extracted + chat-extracted actions with confidence ≥0.85 auto-write to `tasks.json` + append row to `/srv/Nexostrat/00_META/audit/auto_tasks.log`. Confidence <0.85 surfaces as Telegram review prompt to addressee. Requires calibration corpus (B17, tracked).

6. **Telegram-only for JP at Stage 1.** No parallel email/Slack channel. FOSS dashboard from Plan 02 may eventually surface web view but isn't a notification channel.

## Stack state (live & verifiable next session)

```
HP (ricardo-hp-laptop, Tailscale 100.64.121.80) — unchanged from session 9:
  baserow + bookstack + bookstack-db + caddy all healthy.
  systemd nexostrat-foss-stack.service enabled.
  Two nightly timers still MASKED (reconcile @03:30, schema-check @Mon04:00) —
    waiting on t-plan-02a-chunk-b-systemd-creds (high, due 2026-06-01).

Recording + transcription stack — unchanged from session 9:
  OBS Studio 30.0.2 + pavucontrol 5.0
  Whisper.cpp /opt/whisper.cpp/ + models (small fallback, large-v3 preferred)
  ~/bin/transcribe.sh wrapper
  OBS profile audio-meeting

Vault discipline — unchanged from session 9:
  infra/age-recipients.txt: 2 keys (Ricardo, JP). C2 operationally closed.

NEW this session — Brain Bot Platform tenancy locked:
  ADR-039 in 00_GOVERNANCE/adr/ — full body, cross-refs Brain artifacts.
  ADR-020 marked Superseded by ADR-039 in founding-spec table.
  CLAUDE.md Strict Rule #4 clarified inline.
  Brain audit Session B Notes block filled (lives Brain-side, not in our repo).
  Commit 0293ed8 on local main; pushed to Gitea origin + mirrors at session-end.
```

## In flight — concrete next actions

```
NEXT SESSION:
  1. Open Claude Code AT /srv/Nexostrat/.
  2. Ricardo types "Start Session."
  3. Claude reads CHECKPOINT + STATUS + tasks + calendar + latest journal
     (00_META/journal/2026-05-21_brain-bot-tenancy-decision.md).
  4. Ricardo decides arc.

CRITICAL PATH (unchanged from session 9):

  ┌── 2026-05-25 1pm Tijuana ─────────────────────────────┐
  │  REUNIÓN TRIXX LOGISTICS                               │
  │  (t-trixx-meeting-execution, critical)                 │
  │  T-4 days. Materiales en Desktop intactos.             │
  └─────────────────────┬──────────────────────────────────┘
                        │
  ┌── 2026-05-27 ─▼─────────────────────────────────────────┐
  │  SKILL 05 (Opportunity Report)                          │
  │  (t-trixx-skill-05-opportunity-report, high)            │
  └─────────────────────────────────────────────────────────┘

BRAIN BOT PLATFORM PRE-LAUNCH (new this session, ordered by date):

  ┌── 2026-05-28 ─┐ NEW
  │  t-plan-04-description-update (high)                    │
  │  Master plan index README update — Plan 04 reframe      │
  │  from standalone bot to tenant integration.             │
  │  ~15 min. Touch when next opening the index.            │
  └───────────────┘

  ┌── 2026-06-15 ─┐ NEW
  │  t-nexostrat-telegram-account (critical)                │
  │  Provision firm phone + Telegram account + BotFather    │
  │  registration of @NexostratBot. Hard pre-deploy gate.   │
  │  Collect JP_DM_ID + NEXOSTRAT_GROUP_ID into vault.      │
  └───────────────┘

  ┌── 2026-06-15 ─┐ NEW
  │  t-weekend-desktop-on-decision (high)                   │
  │  Decide weekend desktop-on cadence. Blocks Mon 08:00    │
  │  Nexostrat brief (depends on Sun 19:30 extraction).     │
  │  Recommend (a) desktop on Sun 18:00-20:00 TJ.           │
  └───────────────┘

  ┌── 2026-06-22 ─┐ NEW
  │  t-confidence-calibration-corpus (high)                 │
  │  Build 50+ rated calibration examples for hybrid task   │
  │  write. Plan 04 implementation prerequisite.            │
  └───────────────┘

  ┌── 2026-07-15 ─┐ NEW (medium, not blocking)
  │  t-plan-08-client-meeting-integration (medium)          │
  │  When Plan 08 (Meeting Pipeline) drafts, include the    │
  │  client_slug routing pattern.                            │
  └───────────────┘

PARALLEL TRACK — Chunk B follow-ups (unchanged from session 9):

  ┌── 2026-06-01 ─┐
  │  t-plan-02a-chunk-b-systemd-creds (high)                │
  └───────────────┘

  ┌── 2026-06-10 ─┐
  │  t-plan-02a-chunk-b-renderer-hook-lift (medium)         │
  │  t-plan-02a-chunk-b-test-coverage (medium)              │
  └───────────────┘

CHUNK C — next major arc (unchanged from session 9):

  ┌── 2026-06-12 ─┐
  │  t-plan-02a-execute-chunk-c (medium)                    │
  └───────────────┘

  ┌── 2026-06-30 ─┐
  │  t-plan-02b-write (medium)                              │
  └───────────────┘

PARTIALLY CLOSED (unchanged from session 9):

  ┌── 2026-06-30 ─┐
  │  t-plan-01a-jp-and-tty-deferred (medium)                │
  │  Items (1)-(4) DONE. Items (6)(7)(8)(9) remain —        │
  │  Ricardo-side TTY-gated, no longer JP-coordination.     │
  └───────────────┘

OTHER OPEN (unchanged from session 9 — see tasks.json):
  - t-vault-backup-foss-env, t-whatsapp-andrea-audiencia, t-practice-meeting-jp,
    t-migrate-pilotos-to-clients, t-presentation-refresh-post-adr-038,
    t-plan-01b-execute-warm-standby (gated on physical second host),
    t-confidence-marking-company-analyst, t-nexostrat-capabilities-catalog,
    t-validate-pipeline-improvements, t-plan-01c-polish-pass,
    t-desktop-pc-recording-stack-install
```

## Architecture-conflict check (passed)

| This session's work | Verification |
|---|---|
| ADR-039 supersedes ADR-020 | Explicit supersession recorded in founding-spec ADR table + ADR-039 frontmatter. Reversal trigger documented. |
| CLAUDE.md Strict Rule #4 edit | Clarifies rather than weakens. ADR-039 cross-references to `/srv/brain/` documented as governance-traceability exception. Memory `feedback_no_brain_references` still applies to all artifacts under `/srv/Nexostrat/` except this documented exception. |
| Brain-side audit notes (cross-scope) | Permitted by audit protocol's `Cross-scope edit allowance` clause + root CLAUDE.md Strict Rule #1 (operator-driven, Ricardo in-session). Brain repo's own change log unchanged (not our scope). |
| Five new tasks | Dates aligned to Stage 1 launch window (2026-06-30 to 2026-07-15). Priorities match dependency reality (Telegram account = critical pre-deploy gate; Plan 04 description update = high but small lift). |
| No new memory entries | Existing memories applied (`do-it-right-do-it-once`, `complete-or-nothing`, `honestidad-brutal-evaluacion`). No surprising patterns surfaced. |

## Blocked on

**Brain Architect Session C:** Brain-side, not ours. Now unblocked (both Session A AttenBot and Session B Nexostrat are populated). Ricardo flips that trigger when ready; Brain side runs C and produces design-spec amendments + ADR-025-equivalent on their side.

**Trixx critical path:** materials ready, nothing on our side.

**5 new Brain-Bot-Platform pre-launch items:** all have concrete next actions documented in their `notes` fields. No external blockers beyond the Stage 1 launch window timing.

## Open questions (no blocking)

1. **When does Brain Architect Session C run?** Brain side decides; Nexostrat just needs to be reachable for follow-up amendments if Session C requests them.

2. **What's the right Telegram phone number for the firm account?** Options: firm SIM (most independent), Google Voice tied to contacto@nexostrat.com (cheap, US number), or some other VoIP. Decide when Ricardo provisions the account (target 2026-06-15).

3. **Nexostrat OpenAI key — when and how is it provisioned?** Could be the same OpenAI account Ricardo already has (just a separate API key + project), or a fully separate Nexostrat-owned OpenAI account. The latter is cleaner financially (separate billing) but requires firm-owned email + payment. Likely defers to t-nexostrat-capabilities-catalog rhythm.

## Files modified this session

Session-end commit (this one) will include:

- `STATUS.md` (header + session 10 block prepended)
- `tasks.json` (top-level `updated` bumped; 5 new tasks appended)
- `CHECKPOINT.md` (this file, rewritten)
- `00_META/CHANGELOG.md` (2026-05-21 row added)
- `00_META/journal/2026-05-21_brain-bot-tenancy-decision.md` (NEW)

Earlier this session (already committed + pushed):

- Commit `0293ed8` (Nexostrat) — `CLAUDE.md` Rule #4 clarification + founding-spec ADR table (ADR-020 superseded + ADR-039 row added) + `00_GOVERNANCE/adr/ADR-039-bot-tenant-in-brain-hub.md` (new full ADR body).
- Commit `68a702f` (Brain) — Session B Notes block populated in `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md`.

Untouched this session (pre-existing untracked, not ours):

- `00_META/journal/2026-05-21_strategy-meeting-transcript.md` — pre-existing untracked file from earlier today, not authored by this session.

## Memory updates this session

None new. Existing memories applied — particularly:

- `feedback_do_it_right_do_it_once.md` — drove writing a full ADR-039 body with Context + Decision + Options + Consequences + Anti-decision + Reversal trigger, rather than a one-line ADR table row pointing nowhere.
- `feedback_complete_or_nothing.md` — drove bundling CLAUDE.md amendment + ADR-020 supersession + ADR-039 body + audit notes + commits + tasks + journal + STATUS + CHANGELOG + CHECKPOINT all in one session, instead of punting any piece.
- `feedback_honestidad_brutal_evaluacion.md` — drove the explicit "five concrete enforcement gaps" list (B8) rather than a generic "isolation is solid".

## Estimated time to next milestones

- **Trixx meeting (2026-05-25 1pm Tijuana):** T-4 days. Materials intact.
- **Skill 05 post-Trixx:** ~30-45 min execution + ~70 min wall-time for large-v3 transcription + 30 min Ricardo+JP review.
- **t-plan-04-description-update:** ~15 min.
- **t-nexostrat-telegram-account:** ~30 min (phone provisioning + BotFather + group setup).
- **t-confidence-calibration-corpus:** ~3-5 hours over multiple sittings (50+ rated examples needs real meeting/chat data).
- **t-plan-02a-chunk-b-systemd-creds:** ~30-45 min (unchanged).
- **t-plan-01a-jp-and-tty-deferred items (6)(7)(8)(9) bundled:** ~45-60 min TTY-gated (unchanged).
- **Stage 1 launch realistic:** 2026-06-30 to 2026-07-15 (unchanged).

## After this, what's next

Ricardo picks. The Brain Bot Platform decision is locked at the architectural level; the remaining work is execution — Plan 04 description update (cheap), Telegram account provisioning (medium effort + external dependencies), calibration corpus (multi-session). Critical path remains Trixx 2026-05-25 + Skill 05 post-Trixx.

## For a future auditor reading this baton

This was the 19th execution arc since 2026-05-15 and the 10th end-to-end Claude session. It produced a load-bearing architecture decision (Nexostrat bot tenancy) cleanly: read the design + audit protocol, surfaced the load-bearing tension, presented 3 options with trade-offs, landed Option A with two specific amendments on Ricardo's one-sentence direction, executed the full Session B checklist, and locked the decision in an ADR with a reversal trigger documented. No drift, no half-measures, no "table this for later." Eight pre-launch follow-ups were converted into concrete tasks with owners + dates; five of them are net-new in `tasks.json`. The cross-scope edit pattern (Nexostrat persona writing to Brain repo) worked cleanly under the audit-protocol allowance + root CLAUDE.md Strict Rule #1; Brain Architect Session C will absorb the Notes block in their next session without further Nexostrat involvement (unless they request follow-up amendments).

The session-end bookkeeping commit (next) locks all of this. Next session opens with: Ricardo's choice among (a) Trixx Monday meeting prep if needed, (b) post-Trixx Skill 05 if meeting has occurred, (c) one of the 5 new Brain-Bot-Platform pre-launch items, (d) Chunk B follow-ups (recommended: systemd-creds first), (e) Chunk C, (f) Plan 02b write, (g) Desktop PC stack install, (h) `t-plan-01a-jp-and-tty-deferred` items (6)(7)(8)(9) bundled TTY session, (i) something else.

---

*This CHECKPOINT.md is the baton between sessions. Next session: type "Start Session" → Claude reads this + STATUS + tasks + calendar + latest journal → present the path forward.*
