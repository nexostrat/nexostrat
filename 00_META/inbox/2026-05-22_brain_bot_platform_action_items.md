# 2026-05-22 — Brain Bot Platform: Nexostrat-side action items

**From:** Brain Bot Platform audit (Session B / Session C), `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md`
**To:** Nexostrat (action by a `/srv/Nexostrat/` Claude session)
**Recreated:** 2026-05-24 (original 2026-05-22 ship missing from inbox; rebuilt from audit's B14 / B15 wording per Phase 6 Task 6.7)
**Tracker:** Brain root `tasks.json::t-008` (ADR-025 ratification — depends on the two items below landing)

## Context

The Brain Bot Platform audit (2026-05-21) ratified **Option A** — Nexostrat runs as a tenant inside the shared hub at `/srv/brain-hub/`, not as a standalone bot codebase. Two Nexostrat-side artifacts need updates to align with this decision so the next Claude / Gemini session here doesn't reflexively block the integration as a Strict-Rules violation.

## Action item 1 — ADR-020 supersession (audit B14)

**Current state.** Nexostrat founding spec `2026-05-13_nexostrat-system-design.md` carries `ADR-020 "Independent bot codebase, Accepted 2026-05-11"`. That decision is now obsolete.

**Required edit.** Amend the Nexostrat spec to mark **ADR-020 superseded** by a new ADR in the next available number in Nexostrat's ADR sequence (likely ADR-024 or later — check Nexostrat's current ADR ledger). The new ADR's title:

> "Nexostrat bot runs as tenant in Brain Bot Hub"

The new ADR's body should:

1. Cross-reference `/srv/brain/00_META/governance/plans/2026-05-21_brain_bot_platform_audit_protocol.md` as the originating audit.
2. Cross-reference `/srv/brain/00_META/governance/adr/ADR-025_brain_bot_platform.md` (Brain-side ratification) when it lands.
3. Note that ADR-020 is superseded, not overridden in error — the prior decision was correct given what was known then; Option A emerged from the audit.

## Action item 2 — Strict Rule #4 clarification (audit B15)

**Current state.** Nexostrat `CLAUDE.md` Strict Rule #4 reads:

> `4. **No \`/srv/brain\` references.** Nexostrat is a standalone entity.`

**Required edit.** Replace with:

> `4. **No \`/srv/brain\` references in Nexostrat artifacts.** Shared bot infrastructure at \`/srv/brain-hub/\` is permitted; Nexostrat artifacts (specs, docs, code under \`/srv/Nexostrat/\`) still don't reference \`/srv/brain\` paths.`

**Why it matters.** Without this clarification, the next Claude / Gemini session at `/srv/Nexostrat/` will reflexively block any code that touches `/srv/brain-hub/` as a Rule #4 violation — mirrors the AttenBot A10 finding. This is the operational gate that lets the tenant integration actually function.

## Related action item — @NexostratBot Telegram ownership (audit B19)

Not strictly an inbox memo for Nexostrat's Claude session (this is a deployment-session concern), but worth surfacing here because it's a precondition for Phase 6 cutover:

> `@NexostratBot` should be created from a Telegram account **owned by the firm**, not from Ricardo's personal Telegram. If Ricardo's personal Telegram is ever compromised or transferred, the bot stays with the firm. Suggested provisioning: create `nexostrat-ops` (or similar) Telegram account; that account creates the bot via BotFather; both founders are admins of the JP+Ricardo group.

Until this lands, `NEXOSTRAT_BOT_TOKEN` stays unset in `00_INFRA/02_Compute/services_credentials.md` and the live `/srv/brain-hub/routing.yaml` cannot include the `nexostrat` bot entry without breaking boot.

## Implementation status on the Brain Bot Hub side

For reference (so this memo doesn't bottleneck waiting on Nexostrat's two edits):

- **Phase 1** — Foundation (ScopedFS multi-scope, manifest extension, manifest validator, routing.yaml per-key schema, LLMBudget per-key buckets, schedule.yaml registry, desktop liveness, no-hot-reload boot test) — **shipped** on `brain-bot-platform` branch.
- **Phase 2** — Router (Ollama client, queue, reports, OpenAI client, budget gate, dispatcher, EOD sweep, claude-session pickup, day digest, log scrubbing) — **shipped** on `phase2-router` branch.
- **Phase 3** — Plugin extensions (`/budget`, `/manual`, `/api`, `/status`, `/groceries`, `/run_schedule`, `/scope`) + partial router integration — **shipped** on `phase2-router`.
- **Phase 4a** — Events watcher subscription layer + meeting consumer + hybrid-by-confidence task writer + brief renderer + per-tenant schedule.yaml — **shipped** on `phase2-router`.
- **Phase 4a Task 4a.9** — Full router-stack integration in `_amain` (closed open-items a–h) — **shipped** on `phase2-router`.
- **Phase 5** — Group chats (listener / 19:30 extractor / @mention Layer-3 / desktop-off degrade) — **shipped** on `phase2-router`.
- **Phase 6** — Nexostrat tenant scaffolding:
  - Task 6.1 (routing_loader: `jp` actor) — **shipped**
  - Task 6.2 (calendar filter v1) — **shipped** with `/srv/Nexostrat/00_META/calendar_filter.md` (canonical rule) + `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py` (implementation)
  - Task 6.3 (brief templates) — **shipped** at `/srv/Nexostrat/00_META/templates/` (7 templates + README)
  - Task 6.4 (calibration corpus scaffold) — **shipped** at `/srv/Nexostrat/00_META/calibration/` (rubric + schema + seed file)
  - Task 6.5 (calibration retuner) — **shipped** at `/srv/brain-hub/hub/router/calibration.py`
  - Task 6.6 (path-prefix) — **verified** via `tests/test_tenant_infer.py`
  - Task 6.7 (this memo + Nexostrat-side ADR + Rule #4) — **this memo** completes the Brain-hub side; the two action items above are still pending on Nexostrat's side

**Phase 6 cutover** (activating Nexostrat in the live `routing.yaml`) is blocked by:

1. These two Nexostrat-side ADR + Rule #4 edits.
2. `@NexostratBot` Telegram account creation (B19).
3. `NEXOSTRAT_BOT_TOKEN` + `JP_DM_ID` + `NEXOSTRAT_GROUP_ID` populated in `00_INFRA/02_Compute/services_credentials.md`.
4. `NEXOSTRAT_OPENAI_API_KEY` provisioned (separate from Ricardo's personal OpenAI key per audit B13).

Once all four land, the live `routing.yaml` gets the `nexostrat:` bot block (spec in plan §Task 6.1) and a hub restart picks up the new tenant.

## Acknowledgement protocol

When the two action items above are merged on Nexostrat's side, drop a reply memo to `/srv/brain/00_META/inbox/` referencing this memo's filename so Brain root knows to flip `tasks.json::t-008` to `done`.
