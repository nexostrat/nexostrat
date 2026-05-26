# ADR-039 — Nexostrat bot runs as tenant in central Brain Bot Hub

> **Status:** Accepted
> **Date:** 2026-05-21
> **Decided by:** Ricardo (Nexostrat Founder persona session)
> **Supersedes:** ADR-020 (Independent bot codebase, 2026-05-11)
> **Cross-refs:**
> - Brain-side design: `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_design.md`
> - Brain-side audit (Session B notes are the canonical record of this decision): `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md`

## Context

The Brain side has designed a multi-tenant Telegram bot platform that adds Nexostrat as a third tenant alongside Personal and Mevillo. One Python process at `/srv/brain-hub/` runs all three bot identities under `asyncio.gather()`, sharing infrastructure (Whisper for voice transcription, Ollama via Tailscale for local LLM, OpenAI client for API path, APScheduler, events watcher, manifest validator). Cross-tenant isolation is enforced as a non-negotiable Strict Rule (B1 in the Brain design) with multiple defense layers: ScopedFS multi-scope per plugin, per-tenant queue + report directories, scope-keyed meeting-event routing, manifest declarations refused at boot if a plugin loads in the wrong tenant.

The original ADR-020 ("Independent bot codebase", 2026-05-11) committed Nexostrat to running its own bot codebase, separate from any other bot Ricardo operates. That decision predates the existence of the Brain Bot Platform design.

After reviewing the design + audit protocol on 2026-05-21, Nexostrat must decide: (a) accept the tenant model as designed, (b) reject and build an exclusive Nexostrat bot, (c) hybrid (shared libraries, separate process).

## Decision

Nexostrat accepts the tenant model with two binding amendments:

1. **Separate Telegram token (`NEXOSTRAT_BOT_TOKEN`).** Already in the Brain design. No deviation.
2. **Nexostrat-owned OpenAI API key with its own budget envelope.** This amends §11 of the Brain design: the `LLMBudget` ledger tracks per-key buckets, not a single global cap. Personal+Mevillo continue to share Ricardo's personal key under the existing $10/month global cap. Nexostrat operates under an independent cap (initial: $20/month; warnings at 50%, hard stop at 100%; raised as firm revenue justifies).

## Options considered

| | Central hub (Option A — chosen) | Exclusive Nexostrat hub (Option B) | Hybrid — shared libs, separate process (Option C) |
|---|---|---|---|
| Effort | Land as tenant 3 in already-designed system | Weeks of duplicate infra (router, scheduler, events watcher, manifest validator, Whisper client, etc.) | Brain libs packaged for reuse; Nexostrat owns process |
| Honors ADR-020 verbatim | ✗ (this ADR supersedes it) | ✓ | ✓ (separate process) |
| Cross-tenant bleed risk | Mitigated by defense-in-depth (ScopedFS + manifest validator + scope routing) | Zero by construction | Zero by construction; lib bugs still possible |
| Budget control | Per-key envelopes (after amendment) | Independent caps per entity | Independent caps |
| JP optics ("Nexostrat is its own thing") | Weak unless explained — JP's bot runs on shared infra | Strong | Medium |
| Operational surface | One systemd unit, one deploy | Two services to maintain | Two services, shared dependency |
| Failure isolation | Brain hub down → Nexostrat bot down | Independent failure domains | Independent |
| Meetings subsystem | Already routes by `scope:` | Need a Nexostrat-side events consumer | Same as B |

## Consequences

**Positive:**
- ~3-4 weeks of duplicate infrastructure work avoided (router subsystem, scheduler, events watcher, budget gate, manifest validator, group-chat extractor, manuals build, Whisper client).
- Meeting subsystem's `scope:`-keyed event routing is reusable as-is.
- Single deploy/restart surface; one observability pipeline.

**Negative (accepted risks):**
- A hub-side bug can take the Nexostrat bot down. Mitigation: hub adopts strict isolation tests (B1 + B8 enforcement gaps from Session B audit notes) as CI-blocking; deploy windows announced via the Nexostrat bot.
- "JP's bot runs on Ricardo's personal infrastructure" is a partnership-optics concern. Mitigation: documented explicitly in `MANUAL.es.md` (the Nexostrat manual JP reads), data flows traced from group chat → 19:30 local extraction → T-2h brief, with the explicit assertion that nothing from `/srv/brain/*` or `/srv/atten-bot/*` ever surfaces in Nexostrat outputs.

**Mandatory follow-ups before Stage 1 launch (tracked in Session B audit notes, OFF-CHECKLIST items B13–B20):**
- B13: per-tenant API key amendment to Brain `routing.yaml` + `LLMBudget` schema.
- B14: this ADR (✓ done in this commit).
- B15: CLAUDE.md Strict Rule #4 clarification (✓ done in this commit).
- B16: weekend desktop-on decision for the Sun 19:30 extraction (blocks Mon 08:00 brief).
- B17: confidence-score calibration corpus for the hybrid task-write posture.
- B18: client-meeting integration spec in Plan 08 (Meeting Pipeline).
- B19: firm-owned Telegram account for `@NexostratBot` (not Ricardo's personal Telegram).
- B20: JP-Light read paths for `MANUAL.es.md` + audit log (Telegram `/manual` and `/audit_tasks` commands before the FOSS dashboard ships).

## Anti-decision (what this ADR does NOT do)

- Does not commit Nexostrat to using the Brain hub for anything beyond the Telegram bot. Other shared-infra ideas (e.g., shared agents, shared CLI) require their own ADRs.
- Does not put Nexostrat data anywhere outside `/srv/Nexostrat/`. Hub reads/writes Nexostrat data via ScopedFS scoped to `(/srv/Nexostrat, [])`.
- Does not waive the no-`/srv/brain`-references-in-Nexostrat-artifacts rule. Citations like the one in this ADR's frontmatter are governance-traceability, not infrastructure-coupling — see CLAUDE.md Strict Rule #4 clarification.

## Reversal trigger

If any of the following happens, re-open this decision:
- A cross-tenant data leak occurs (Nexostrat data appears in a Personal/Mevillo surface, or vice versa).
- The hub becomes unreliable enough that Nexostrat's commercial cadence is materially harmed (>5% of meetings ship without their brief).
- JP requests separation, citing partnership-optics or any other reason.
- The Brain side's strict-isolation tests degrade or are removed.

Reversal path: write a new ADR (ADR-04X) "Nexostrat exits Brain Bot Hub", fork the hub repo to a Nexostrat-owned codebase, migrate state, retire `NEXOSTRAT_BOT_TOKEN` from the Brain `routing.yaml`. Estimated ~2 weeks calendar, mostly state migration.
