# Per-client template — 12 stations + 3 cross-cutting (ADR-010, F19)

This folder is the canonical empty client. The interim scaffolder
`infra/scripts/new-client.sh` copies it to `pipeline/clients/<slug>/` and
substitutes placeholders in `state.json`, `checkpoint.md`, and `README.md`,
then drops the two ADR-027 intake templates (`research_input.md` +
`our_hypotheses.md`) from `skills/shared/` into `00_intake/`. Plan 07 will
replace this with a fuller scaffolder that also emits to `events.jsonl` and
exposes a Telegram trigger.

## The 12 stations (sequential phases of the engagement)

| # | Folder | Plan Maestro mapping | Owning skill |
|---|---|---|---|
| 00 | `00_intake/` | Pasos 1-3 | (research_input.md + our_hypotheses.md per ADR-027) |
| 01 | `01_company_analysis/` | Fase B Skill 1 | Skill 1 (company-analyst) |
| 02 | `02_industry_analysis/` | Fase B Skill 2 | Skill 2 (industry-analyst) |
| 03 | `03_competitor_analysis/` | Fase B Skill 3 | Skill 3 (competitor-analyst) |
| 04 | `04_prep_llamada/` | Fase B Skill 4 (PRIVATE) | Skill 4 (discovery-meeting) |
| 05 | `05_opportunity_report/` | Fase C — THE DELIVERABLE | Skill 5 (opportunity-report) |
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
| `transcripts/` | Meeting transcripts. Canonical source TBD per Plan 02 FOSS stack decision (ADR-038 superseded ADR-024's Notion-canonical posture; Whisper.cpp + Jitsi promoted to canonical pending Plan 02). |
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

## Scaffolding a new client

```bash
bash infra/scripts/new-client.sh <slug> <country-ISO2> '<Legal Name>' <sector> [--pilot]
```

Example:

```bash
bash infra/scripts/new-client.sh trixx-logistics MX 'Grupo Trixx' logistica --pilot
```

Effect:

- `pipeline/clients/<slug>/` created from this template (refuses to overwrite an existing target).
- `state.json` populated with `client`, `name`, `country`, `sector`, `started`, `owner=client-owner`, `phase=prospect`, optionally `pilot=true`.
- `checkpoint.md` slug-stamped and timestamped (status stays `CHECKPOINT_NO_ACTIVE_WORK`).
- `README.md` replaced with a per-client stub (the meta-README — this file — stays on `_template/`).
- `00_intake/research_input.md` and `00_intake/our_hypotheses.md` copied from `skills/shared/` and slug-stamped.

## Post-scaffold workflow (the canonical handoff)

1. **Fill `00_intake/research_input.md`** — facts only. Identity, presence, contacts, origin of the prospect, 5-min LinkedIn pre-trabajo. **Do NOT write hypotheses here.**
2. **Fill `00_intake/our_hypotheses.md`** — judgment only. What we think the dolor is, the decisor read, presupuesto estimate, tono, sensibilidades, capability-fit hypotheses, things we expect research to confirm or refute. **This file is SEALED during Skills 01-03** per ADR-027 — the operator must not paste its content into the model while running the research skills.
3. **Trigger the pipeline.** In Claude Code at `/srv/Nexostrat/`, say:

   > `Analiza <slug>`

   Claude reads `state.json` (confirms fresh `prospect` intake), reads `00_intake/research_input.md`, and invokes Skill 01 (company-analyst). Output lands at `01_company_analysis/runs/<ts>_mode-a/final_report.{md,docx}` per `skills/README.md`.
4. **Human review** between every skill. Read Skill 01's output, correct what we know better, then continue to Skill 02 → review → Skill 03 → review → Skill 04. Skill 04 (PrepLlamada) is the **first skill that reads `our_hypotheses.md`**.
5. **30-min discovery call** with the client, recorded. PrepLlamada is the meeting guide.
6. **Skill 05 (opportunity-report)** consumes 01+02+03+meeting-notes+our_hypotheses → produces the client-facing Reporte de Oportunidades.
7. **Mandatory Ricardo+JP internal review** (Fase 5 in JP's pipeline diagram) before manual send.

## What's NOT here

Per Plan 01a scope, this template is structural only. Skill-specific scaffolding
(prompts/v1.md, templates, benchmarks) lives at `skills/<NN>_<name>/` and is
populated in Plans 05-06.
