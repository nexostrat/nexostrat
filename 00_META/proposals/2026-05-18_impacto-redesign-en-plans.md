# Architecture Impact Map — 2026-05-18 Redesign vs Plans 02-10

> **Status:** Draft. Produced while awaiting JP confirmation on the 5 remaining `decisiones pendientes` from `2026-05-18_proceso-comercial-fases.md`.
> **Purpose:** Document the exact per-plan effect of the 4-phase commercial-process redesign, so the post-confirmation technical brainstorm has a complete inventory of what shifts.
> **Source of the redesign:** `00_META/proposals/2026-05-18_proceso-comercial-fases.md` (proposal + 7 pending decisions).
> **Source of the plans:** `00_META/plans/README.md` (master plan index, per-plan headers).
> **Bilingual rule:** internal/architectural artifact → English.

---

## TL;DR

Foundation (Plans 01a / 01b / 01c) is **untouched** — `v0.1-foundation` holds. Plans 02-08 each shift in scope or priority. Plans 09-10 are mostly unaffected. The largest impact lands on **Plan 07 (Per-Client Production Chain + Pipeline Orchestrator)** — the state machine roughly doubles and the human-checkpoint mechanic becomes a first-class workflow primitive. **Plan 08 (Meeting Pipeline)** moves earlier in priority because Skill 05 in Fase 0 needs meeting recording before any other plan deliverable consumes it. **Plan 02 (Docs / FOSS stack)** picks up a 5th role (booking tool) and a new binding constraint (client UX simplicity).

The redesign does not require any change to the spec's architectural decisions (ADRs 001-038) — but it likely warrants a new **ADR-039 "Four-phase commercial process"** to lock the redesign as the architectural source of truth for skill scope, state machine, and automation surface.

---

## Per-plan impact

### Plan 01a / 01b / 01c — Foundation

**Effect:** None. Foundation milestone (`v0.1-foundation`) holds. The redesign sits on top of the foundation, not under it.

---

### Plan 02 — Documentation System (FOSS docs stack)

**Original scope:** Set up `docs/` Diátaxis structure + paired-files drift hook + auto-generated reference docs + top ~10 how-tos. Per ADR-038, pick FOSS self-hosted replacements for Notion's 4 roles: meeting capture canonical, summary generation, CRM, collaborative docs workspace.

**Redesign effect:**
- **+1 role to evaluate: booking tool.** Calendly-equivalent for client self-scheduling (Fase 0 step 13 → Fase 1 trigger). Cal.com self-hosted is the obvious candidate. easyappointments is a leaner alternative.
- **New binding constraint: client UX simplicity.** Per Ricardo's 2026-05-18 directive, FOSS picks must look and feel as smooth as Calendly to the client — no client account creation, no installation, no complex navigation. This binds across all 5 roles, not just booking.
- **CRM role re-framed:** must track the new 4-phase state set (phase_0_intake → phase_3_retainer_active) per client, not just generic deal states. The CRM choice now has a structural requirement (custom state machine support).
- **Email tool requirements harden:** must support **delayed triggers** (Fase 0 day-7 auto-follow-up, day-14 call alert routing). Postmark / Mailgun / Listmonk self-hosted / etc. all support delayed sends, but the picked tool must integrate cleanly with the event router (Plan 03).

**Net change:** ~20 % scope growth (5 roles vs 4), ~10 % constraint tightening (client UX bar added). ADR-038 unchanged. Plan 02's brainstorm must be re-scoped before writing.

---

### Plan 03 — events.jsonl Spine + Python Agent Framework

**Original scope:** `events.jsonl` spine + ~80 event types per spec §9.2 + agent dispatcher + event-router daemon + systemd timer/service infra + agent template.

**Redesign effect:**
- **MORE load-bearing.** Every phase transition + automation trigger emits an event. The event spine becomes the single source of truth for "where is each client in the pipeline."
- **New event types — phase transitions (~20-30):** `phase_0_intake.created`, `phase_0_skill_chain.started`, `phase_0_skill_chain.completed`, `phase_0_30min.scheduled`, `phase_0_30min.completed`, `phase_0_doc.sent`, `phase_0.dead_no_response`, `phase_1.booked`, `phase_1.paid`, `phase_1_skill_chain.started`, `phase_1_meeting_1.scheduled`, `phase_1_meeting_1.completed`, `phase_1_solutions.drafted`, `phase_1_pdf.sent`, `phase_1_meeting_2.scheduled`, `phase_1_meeting_2.completed`, `phase_1.closed`, `phase_2.implementation_started`, `phase_2.solution_delivered`, `phase_3.retainer_active`, `phase_3.retainer_cancelled`.
- **New event types — automation triggers (~15):** `calendly.booking_received`, `calendly.cancelled`, `calendly.rescheduled`, `payment.confirmed`, `payment.failed`, `email.day7_sent`, `email.day7_bounced`, `email.day7_replied`, `alert.day14_triggered`, `alert.day14_handled_by_ricardo`, `meeting.recording_started`, `meeting.recording_completed`, `meeting.transcript_ready`, `meeting.recording_failed`, `skill.checkpoint_awaiting_human`, `skill.checkpoint_approved_by_human`.
- **Event taxonomy in spec §9.2 grows from ~80 to ~120-130 types.**
- **Agent dispatch + router daemon unchanged structurally.** The schemas grow; the engine doesn't.

**Net change:** ~50 % event-taxonomy growth. Zero architectural change to dispatch / router / agents.

---

### Plan 04 — Telegram Bot Core + Unified Inbox

**Original scope:** Bot service + plugin framework + capture commands (`/note`, `/idea`, `/question`, etc.) + unified inbox + encrypted chat logger + per-user TZ scheduling + state-inspection plugins.

**Redesign effect:**
- **New commands needed:** `/phase <client> <new_phase>` (manual phase advance fallback), `/booking-received <slug>` (manual fallback if Calendly webhook fails), `/payment-confirmed <slug>`, `/call-alert-handled <slug>`, `/intake-form <slug>` (kicks off Fase 0 step 1), `/run-skill <skill_id> <client> <stage>` (manual skill invocation with checkpoint), `/approve-checkpoint <event_id>` (advances the orchestrator past a paused human-review checkpoint).
- **Notification surfaces grow:** day-14 call alerts route to Ricardo's DM with action buttons. Meeting-recording-failed alerts route to Ricardo immediately.
- **Existing capture commands unchanged.**

**Net change:** ~10 % new command surface. Zero architectural change.

---

### Plan 05 — Skill 1 End-to-End (Template for 2-5)

**Original scope:** Wire `01_company_analyst` into Mode A (manual) + Mode B (API parallel-then-judge), running on the Bodai benchmark fixture. Establish per-skill pattern for Plans 06 to clone.

**Redesign effect:**
- **Skill 1 itself unchanged.** Stays as `01_company_analyst`.
- **Template pattern grows:** needs to support 8-10 skills instead of 5. Same pattern, more skills.
- **New skill-content-delivery model:** JP owns content (prompts, output structures, tone) for Skills 04 (adjusted) + 05 + 06 + 07 + 07.5(?) + 08. Ricardo owns wrapping (folder structure, scripts, tests). The "skill pattern" effectively splits into JP-deliverable (markdown content) + Ricardo-wrappable (skills/NN_<name>/ scaffolding). The pattern doc at `skills/README.md` needs a "JP content delivery format" section.
- **Bodai benchmark fixture stays valid** for Skill 01. New fixtures needed for the new skills (built per-skill as they're delivered).
- **Anti-hallucination marker block** now also enforced on Skills 04-08 prompts (via pre-commit hook from Plan 05).

**Net change:** ~5 % pattern adjustment, no breaking change. The pattern travels cleanly to the larger skill set.

---

### Plan 06 — Skills 2-5

**Original scope:** Apply Plan 05 pattern to Skill 2 (industry), Skill 3 (competitor), Skill 4 (meeting script — private), Skill 5 (opportunity report — diagnóstico deliverable). Bodai benchmarks for each.

**Redesign effect — MAJOR RESTRUCTURE:**

| Original Skill | Status under redesign |
|---|---|
| Skill 2 — Industry Analyst | Unchanged (`02_industry_analyst`) |
| Skill 3 — Competitor Analyst | Unchanged (`03_competitor_analyst`) |
| Skill 4 — Meeting Script (private, 60-min post-pay) | **Renamed** `06_discovery_meeting` → `04_briefing_30min`; **content reshaped** (30-min pre-pay with paid-meeting hook). Content delivered by JP via `t-jp-deliver-skill-content`. |
| Skill 5 — Opportunity Report (diagnóstico) | **Replaced** by new Skill 05 (Resumen Pre-engagement: 2-page free doc with high-level opportunities + hook to paid Fase 1). |

- **New skills net-added:** Skill 06 (Análisis Profundo), Skill 07 (Soluciones Implementables), Skill 07.5 (Scoring — if JP confirms), Skill 08 (PDF Comercial Cliente).
- **Net skill count: 5 → 8 or 9** (depending on Skill 07.5).
- **Per spec §6, all skills still:** produce Spanish output, use anti-hallucination marker block, have Mode A + Mode B paths (Mode B = API parallel-then-judge), pass through judge synthesis.

**Net change:** ~70 % scope growth (skill count almost doubles). Structurally similar — the pattern doesn't change, the count does. May warrant splitting into **Plan 06a (Fase 0 skills: 04 + 05)** and **Plan 06b (Fase 1 skills: 06 + 07 + 07.5? + 08)** for cleaner shipping. Decision pending technical brainstorm.

---

### Plan 07 — Per-Client Production Chain + Pipeline Orchestrator

**Original scope:** 12-station per-client structure + `state.json` schema + transition validators + intake 2-file workflow + `/intake` plugin + pipeline orchestrator chaining Skills 1-5 with `/go` gates.

**Redesign effect — HEART OF THE REDESIGN:**

- **State machine roughly doubles in size.** Original: ~6 states (`prospect` → `exploring` → `diagnostico_delivered` → `cliente_firmado` → `implementacion_curso` → `retainer`). New: ~18 states across 4 phases:
  - Fase 0: `phase_0_intake`, `phase_0_skill_chain`, `phase_0_30min_scheduled`, `phase_0_30min_done`, `phase_0_free_doc_sent`, `phase_0_dead_no_response_2w`
  - Fase 1: `phase_1_booked`, `phase_1_paid`, `phase_1_skill_chain`, `phase_1_meeting_1_scheduled`, `phase_1_meeting_1_done`, `phase_1_solutions_drafted`, `phase_1_pdf_sent`, `phase_1_meeting_2_scheduled`, `phase_1_closed`
  - Fase 2: `phase_2_implementing_<solution-slug>` (one per active solution)
  - Fase 3: `phase_3_retainer_active`, `phase_3_retainer_cancelled`
- **Intake 2-file workflow folds into Fase 0 step 1 intake form** (the Spanish template at `operations/templates/fase_0_intake_form.md` being built in this same session).
- **Human-checkpoint enforcement becomes a first-class concept.** The orchestrator pauses after each skill, emits `skill.checkpoint_awaiting_human`, requires `/approve-checkpoint <event_id>` before chaining to the next skill. This is a new orchestrator behavior.
- **Orchestrator chains:** Skills 01/02/03/04/05 in Fase 0 (with 5 checkpoints), Skills 06/07/07.5?/08 in Fase 1 (with 4 checkpoints).
- **Per-client 12-station structure simplifies.** The new structure maps better to phases (4 phase folders + per-phase artifacts) than to 12 generic stations. The `pipeline/clients/_template/` shape needs a rewrite to match.

**Net change:** ~100 % scope growth in state-machine complexity + entirely new checkpoint mechanic + per-client template rewrite. **Largest single architectural impact of the redesign.**

---

### Plan 08 — Meeting Pipeline

**Original scope:** Dual capture (Notion AI canonical + Jitsi/Whisper shadow for internal; single canonical for client) + parity diff + AI extraction (actions/decisions/dates/questions) + morning brief + T-15 reminder + Google Calendar integration + meeting lifecycle protocol.

**Redesign effect:**
- **PULLED EARLIER in priority.** Skill 05 in Fase 0 consumes the 30-min meeting recording. Skill 07 in Fase 1 consumes the Reunión 1 (1hr) recording. Skill 08-followup consumes the Reunión 2 (1hr) socialization. The meeting pipeline is no longer post-skills infrastructure — it's mid-flow infrastructure that gates Fase 0 and Fase 1 deliverables.
- **Notion dropped (per ADR-038).** Meeting capture canonical role moves to FOSS (picked in Plan 02).
- **Single-canonical capture (no dual).** Internal meetings are out of scope of the commercial process; the new workflow only records client meetings (30-min Fase 0 + Reunión 1 + Reunión 2 in Fase 1). No parity diff needed — there's only one capture per meeting.
- **Whisper.cpp + Jitsi (or chosen FOSS equivalent) stays** for transcription.
- **Extraction agent unchanged.**
- **Brief jobs + Calendar integration shift** to fit the new booking flow (Calendly/Cal.com integration replaces Notion-driven calendar work).
- **Meeting lifecycle protocol simpler** without dual capture.

**Net change:** Earlier priority + ~20 % scope simplification (single capture vs dual; no parity diff). Tooling pick gated on Plan 02.

---

### Plan 09 — Ambient Chat Extraction

**Original scope:** Capture every Telegram group/DM message (encrypted) + Ollama-based extraction during office hours + confirmation loop + Wake-on-LAN for desktop.

**Redesign effect:** Minimal. The ambient extraction layer is orthogonal to the commercial workflow. It captures internal coordination (Ricardo ↔ JP), not client interactions. The redesign doesn't touch this surface.

**Net change:** ~0 %.

---

### Plan 10 — Observability + Go-Live

**Original scope:** All Telegram inspection plugins + daily brief + all failure-mode runbooks + recovery scripts + Stage 1 go-live checklist + v1.0 tag + `deploy.released` event.

**Redesign effect:**
- **New inspection plugins:** `/phase-status` (per-client current phase + last transition + days-in-phase), `/automation-status` (Calendly + payment + email + alert subsystem health), `/checkpoint-queue` (skills awaiting human approval).
- **Daily brief expands** to include phase-pipeline summary (how many clients in each phase, who needs Ricardo's attention today).
- **New failure-mode runbooks:** booking-tool down, payment webhook failed, email-trigger lost, meeting-recording-failed.
- **Go-live checklist** adds: "at least one client successfully passed Fase 0 → Fase 1 transition" as a Stage 1 acceptance criterion.

**Net change:** ~10 % scope growth.

---

## Cross-cutting concerns

### Anti-hallucination discipline

All 8-10 new skills must carry the anti-hallucination marker block (Plan 05 pre-commit hook enforces). Particularly important for:
- **Skill 07** (Soluciones Implementables): must not invent capabilities Nexostrat can't actually deliver. This is the failure mode the 2026-05-17 pilots surfaced — proposing "AI configurator + design assistant" for Scarab when Nexostrat can't deliver that in 3 months. Skill 07's prompt must constrain itself to the `t-nexostrat-capabilities-catalog` output.
- **Skill 05** (Resumen Pre-engagement): client-facing. Hallucinated opportunities damage trust faster than no opportunities at all.

### Foundation untouched

Plans 01a / 01b / 01c remain valid. Tags `v0.1a-foundation`, `v0.1b-mirrors-only`, `v0.1-foundation` are not invalidated by the redesign.

### ADR-038 holds with one expansion

The "drop Notion, pick FOSS" decision is unchanged. The redesign adds **booking tool** as a 5th role to evaluate alongside meeting capture / summary generation / CRM / docs workspace. ADR-038 should be amended (or a sibling ADR-038-bis filed) to reflect the 5-role scope.

### Possible new ADR-039: "Four-phase commercial process"

The redesign is a substantive architectural decision (not just a tactical pivot). It locks in:
- 4-phase pipeline structure
- JP-as-content-owner / Ricardo-as-engineering-owner skill split
- Human-checkpoint mechanic as first-class orchestrator behavior
- Skill count growth (5 → 8-10)
- Plan 08 priority shift
- Plan 02 scope expansion

This warrants an ADR for traceability. Draft after JP confirmation lands.

### Possible new milestone tag: `v0.2-redesign-confirmed`

After JP confirms the 5 remaining `decisiones pendientes`, before any plan rewrites or skill builds. Marks the point where the redesign is officially the architectural source of truth.

---

## Updated dependency graph

```
Plan 01a / 01b / 01c  ←  Foundation (unchanged, v0.1-foundation)
       │
       ▼
JP redesign confirmation gate  ←  Critical-path gate (t-redesign-jp-confirmation, target 2026-05-25)
       │
       ▼
Plan 02 (docs + FOSS stack with 5 roles)  ←┐
                                              │  parallel
Plan 03 (events spine + ~120 event types)  ←┤
                                              │  (all three only need
Plan 04 (bot + new redesign commands)  ←────┘   the confirmation gate)
       │
       ▼
Plan 05 (Skill 01 pattern — unchanged shape, growing skill count)
       │
       ▼
Plan 06 (Skills 04/05 [Fase 0]) → Plan 06b? (Skills 06/07/07.5?/08 [Fase 1])
       │                                       │
       └───────────────┬───────────────────────┘
                       │
                       ▼
Plan 07 (orchestrator with ~18-state machine + human-checkpoint mechanic)
       │
       ▼
Plan 08 (meeting pipeline, pulled earlier in priority; single capture)
       │
       ▼
Plan 09 (ambient extraction, unchanged)
       │
       ▼
Plan 10 (observability + go-live with redesign-aware inspection)
       │
       ▼
v1.0 ← Stage 1 launch
```

---

## Open questions for the post-JP-confirmation technical brainstorm

1. **Does the redesign warrant ADR-039 "Four-phase commercial process"?** Recommend yes — the structural impact is large enough.
2. **Split Plan 06 into Plan 06a (Fase 0 skills) + Plan 06b (Fase 1 skills)?** Smaller plans ship faster and the dependency on JP content delivery (which may be incremental) makes a 2-plan split cleaner.
3. **Booking tool — Plan 02 scope or a sibling Plan 02b?** If Cal.com self-hosted is the obvious pick, it could fold into Plan 02. If the booking tool surfaces strong integration requirements (webhook → Fase 1 trigger), Plan 02b may be cleaner.
4. **`v0.2-redesign-confirmed` tag after JP confirmation, before any plan rewrites?** Recommend yes — gives a clean revert point if any rewrite goes wrong.
5. **Should the per-client folder structure rewrite (Plan 07's new shape) happen before or after the new skills are delivered?** Recommend before — provides the destination for skill outputs.
6. **Where does Skill 07.5 (Scoring) live if confirmed — as its own skill folder or as a sub-routine inside Skill 07?** Recommend its own folder if confirmed; one-skill-one-folder is the canonical pattern.
7. **Mode B (API parallel-then-judge) for the new skills — same shape as Skill 01-03, or differentiate per skill?** Recommend same shape initially; differentiate only if a specific skill demands it.

---

*This document feeds the post-confirmation technical brainstorm. Once JP confirms, the brainstorm uses this map to scope the rewrite of Plans 02 / 03 / 04 / 05 / 06 / 07 / 08. Any decisions made in the brainstorm should update this map.*
