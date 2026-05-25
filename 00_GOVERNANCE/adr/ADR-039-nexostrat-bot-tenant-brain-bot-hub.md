# ADR-039 — Nexostrat bot runs as tenant in Brain Bot Hub

**Status:** PROPOSED — pending Ricardo + JP review and formal sign-off
**Date:** 2026-05-24
**Proposed by:** Brain Bot Platform audit (audit B14), Brain-side session 2026-05-22
**Supersedes:** ADR-020 (Independent bot codebase, Accepted 2026-05-11) — partial supersession; see § Supersession scope
**Cross-references:**
- `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md` — originating audit
- `/srv/Nexostrat/00_META/inbox/2026-05-22_brain_bot_platform_action_items.md` — action item memo (audit B14)
- `/srv/brain/00_META/governance/adr/ADR-025_brain_bot_platform.md` — Brain-side ratification (to be cross-referenced once landed)

---

## Context

ADR-020 (2026-05-11, full body in `00_META/proposals/2026-05-11_company-system-design.md §ADR-020`) decided that the Nexostrat Telegram bot would be an **independent codebase** under `infra/telegram/bot/`. The rationale was sound at the time: Nexostrat is structurally different from Ricardo's personal Brain Telegram Hub (multi-user, multi-channel, firm context), and a clean break avoided version coupling and behavioral drift. The personal Brain Hub at `/srv/brain/` was designated read-only reference, never imported.

In the period between ADR-020 and this decision, Ricardo's Brain Bot Platform project matured into a **multi-tenant hub** (`/srv/brain-hub/`) with explicit per-tenant isolation: scoped filesystems, per-bot routing.yaml keys, per-bot LLM budgets, and plugin opt-in lists. The Brain Bot Platform audit (2026-05-21) evaluated three options for Nexostrat's bot: (A) run as a tenant in the shared hub, (B) standalone codebase sharing only libraries, (C) retain ADR-020 as-is. The audit ratified **Option A**.

The concerns that motivated ADR-020 (behavioral isolation, JP auditability, no version coupling) are addressed in the hub's tenant-isolation model rather than by code separation. ADR-020 is therefore superseded for the bot-deployment decision, not overridden in error — the prior decision was correct given what was known in May 2026; Option A emerged from a purpose-built audit once the hub existed.

## Decision

**Nexostrat's Telegram bot runs as a tenant in `/srv/brain-hub/`, not as an independent codebase under `/srv/Nexostrat/infra/telegram/bot/`.**

Tenant configuration lives in `/srv/brain-hub/routing.yaml` under a `nexostrat:` bot block (spec in Brain Bot Platform audit §Task 6.1). Nexostrat-side artifacts (specs, docs, content templates, calibration data) remain in `/srv/Nexostrat/` and are consumed by the hub via its `ScopedFS` per-tenant filesystem abstraction — Nexostrat's scope root is `/srv/Nexostrat/`.

Nexostrat-specific deliverables already scaffolded on the Brain side (Phase 6, branch `phase2-router`):
- `hub/google/calendar_filter_nexostrat.py` — calendar event filter (canonical rule: `/srv/Nexostrat/00_META/calendar_filter.md`)
- `/srv/Nexostrat/00_META/templates/` — brief template set (7 templates + README)
- `/srv/Nexostrat/00_META/calibration/` — calibration rubric, schema, and seed corpus
- `hub/router/calibration.py` — F1-based threshold retuner (audit B17)
- `routing_loader`: `jp` actor accepted (Task 6.1)

Live cutover (activating Nexostrat in `routing.yaml`) is blocked by four items outside the scope of this ADR: `@NexostratBot` Telegram account creation (audit B19), `NEXOSTRAT_BOT_TOKEN` + `JP_DM_ID` + `NEXOSTRAT_GROUP_ID` population, `NEXOSTRAT_OPENAI_API_KEY` provisioning, and formal sign-off on this ADR.

## Supersession scope

- **ADR-020 (Independent bot codebase):** The deployment decision is superseded. Nexostrat's bot is not built from scratch under `infra/telegram/bot/`; that directory is not created. The patterns ADR-020 planned to carry over (plugin framework, allowlist auth, systemd shape) remain available in the hub's shared infrastructure.
- **Spec `2026-05-13_nexostrat-system-design.md` ADR Map, ADR-020 row:** Status should be updated from `Accepted` to `Superseded by ADR-039` in a follow-up spec touchup commit. [TBD: Ricardo to schedule — can accompany any other spec amendment.]
- **`infra/telegram/bot/` directory:** Not created. The infra subtree under `/srv/Nexostrat/` that ADR-020 anticipated for a standalone bot does not need to be scaffolded.

## What is NOT superseded

- The principle that Nexostrat artifacts (`/srv/Nexostrat/` content, docs, vault) remain in the Nexostrat repo and are not stored in `/srv/brain-hub/` or `/srv/brain/`.
- Nexostrat's identity as a standalone git repo at `/srv/Nexostrat/`.
- All other ADRs. This supersession is narrowly scoped to the bot-deployment decision.

## Consequences

**Positive:**
- No duplicated bot infrastructure. Plugin development, LLM budget gates, meeting task writing, and future features ship once in the hub and become available to Nexostrat via config.
- Faster Nexostrat bot activation: Phase 6 scaffold is already on `phase2-router`; cutover requires credentials + sign-off, not a build.
- Tenant isolation in the hub provides the behavioral separation ADR-020 sought: Nexostrat's scope root, budget, and plugin list are independent of the Personal tenant.

**Negative:**
- Nexostrat's bot is now operationally coupled to Ricardo's Brain Bot Hub release cycle. Hub upgrades and breakages affect the Nexostrat bot.
- JP cannot audit the Nexostrat bot in isolation from Ricardo's personal infrastructure; he audits the hub's Nexostrat tenant configuration. [TBD: Ricardo + JP to agree on auditability posture — the tenant config in `routing.yaml` plus `/srv/Nexostrat/00_META/` content may be sufficient, but this should be confirmed with JP.]

**Operational:**
- Live cutover checklist lives in `/srv/Nexostrat/00_META/inbox/2026-05-22_brain_bot_platform_action_items.md §Phase 6 cutover`.
- Once the four cutover blockers clear, a hub restart activates the Nexostrat tenant.
- Brain-side: open `tasks.json::t-008` (ADR-025 ratification) becomes unblocked once this ADR is formally signed off and the two inbox action items are merged.

## Open items for Ricardo + JP review

- [ ] JP awareness: does JP understand and accept that the bot runs in Ricardo's hub rather than a fully isolated Nexostrat codebase? Needs async confirmation via Telegram or next joint session.
- [ ] Spec touchup: ADR-020 row in `2026-05-13_nexostrat-system-design.md` ADR Map needs status updated to `Superseded by ADR-039`. Schedule with next spec amendment pass.
- [ ] Formal sign-off: change Status from `PROPOSED` to `Accepted` once both founders confirm.
