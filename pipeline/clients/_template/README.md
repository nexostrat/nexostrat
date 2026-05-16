# Per-client template — 12 stations + 3 cross-cutting (ADR-010, F19)

This folder is the canonical empty client. `infra/scripts/new-client.sh` (Plan 07)
copies it to `pipeline/clients/<slug>/` and substitutes placeholders in
`state.json`, `checkpoint.md`, and `README.md`.

## The 12 stations (sequential phases of the engagement)

| # | Folder | Plan Maestro mapping | Owning skill |
|---|---|---|---|
| 00 | `00_intake/` | Pasos 1-3 | (research_input.md + our_hypotheses.md per ADR-027) |
| 01 | `01_company_analysis/` | Fase B Skill 1 | Skill 1 (company-analyst) |
| 02 | `02_industry_analysis/` | Fase B Skill 2 | Skill 2 (industry-analyst) |
| 03 | `03_competitor_analysis/` | Fase B Skill 3 | Skill 3 (competitor-analyst) |
| 04 | `04_meeting_script/` | Fase B Skill 4 (PRIVATE) | Skill 4 (meeting_script) |
| 05 | `05_opportunity_report/` | Fase C — THE DELIVERABLE | Skill 5 (opportunity_report) |
| 06 | `06_proposal/` | Pasos 7-8 (Fase D) | (template-driven, no skill) |
| 07 | `07_contract_onboarding/` | Paso 9 (Fase E) | (template-driven, no skill) |
| 08 | `08_solution_design/` | Paso 10 | (template-driven, no skill) |
| 09 | `09_implementation/` | Paso 11 | (template-driven, no skill) |
| 10 | `10_followup/` | Paso 12 (30/60/90) | (template-driven, no skill) |
| 11 | `11_retainer/` | Paso 13 | (template-driven, no skill) |

**Folders never move.** Phase tracked in `state.json` (see schema below).

## The 3 cross-cutting folders

| Folder | Holds |
|---|---|
| `transcripts/` | Meeting transcripts (canonical = Notion AI per ADR-024; shadow = Whisper for internal) |
| `communications/` | Email + WhatsApp + Telegram captures |
| `archive/` | Superseded artifacts (kept for forensic record; never deleted) |

## `state.json`

Schema: `nexostrat-client-state-v1` (full schema landed in Plan 03 alongside the
event-spine validators). Required fields: `client`, `name`, `country`, `sector`,
`started`, `owner`, `phase`, `phase_history[]`, `pilot`, `pricing`, `next_action`,
`kpis`, `blockers[]`, `tags[]`, `recording_preference`.

Phase values: `prospect → intake → exploring → diagnostico_pendiente →
diagnostico_delivered → propuesta_pendiente → propuesta_sent →
propuesta_{accepted,rejected,revising} → cliente_firmado → diseño →
implementación → seguimiento_30 → seguimiento_60 → seguimiento_90 →
retainer_active`. Plus `churned`, `nurture`, `retainer_paused`.

Transitions emit events to `infra/events/events.jsonl` (Plan 03) and are
gated by Telegram commands (`/advance`, `/regress`, `/set-phase`, etc. — Plan 04+).

## `checkpoint.md`

Per ADR-031: client-scoped session continuity. Empty file = refused commit
unless `CHECKPOINT_NO_ACTIVE_WORK` token present (this template starts in that
state).

## What's NOT here

Per Plan 01a scope, this template is structural only. Skill-specific scaffolding
(prompts/v1.md, templates, benchmarks) lives at `skills/<NN>_<name>/` and is
populated in Plans 05-06.
