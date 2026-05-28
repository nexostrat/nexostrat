# Per-client template — 2 etapas + 2 cross-cutting

This folder is the canonical empty client. The interim scaffolder
`infra/scripts/new-client.sh` copies it to `pipeline/clients/<slug>/` and
substitutes placeholders in `state.json`, `checkpoint.md`, and `README.md`,
then drops the two ADR-027 intake templates (`research_input.md` +
`our_hypotheses.md`) from `skills/shared/` into
`etapa_1_preparacion/00_intake/`. Plan 07 will replace this with a fuller
scaffolder that also emits to `events.jsonl` and exposes a Telegram trigger.

## Estructura por cliente

```
pipeline/clients/<slug>/
├── etapa_1_preparacion/         ← todo lo pre-reunión
│   ├── 00_intake/                  ← research_input.md + our_hypotheses.md (ADR-027)
│   ├── 01_analisis_compania/       ← Skill 01 (company-analyst) output
│   ├── 02_analisis_industria/      ← Skill 02 (industry-analyst) output
│   ├── 03_analisis_competencia/    ← Skill 03 (competitor-analyst) output
│   └── 04_guia_reunion/            ← Skill 04 (discovery-meeting / PrepLlamada) output
├── etapa_2_diagnostico/         ← todo lo post-reunión
│   ├── transcripciones/            ← audios + transcripts de la reunión
│   └── reporte_interno/      ← Skill 05 (internal-report) output — el deliverable
├── communications/             ← email + WhatsApp + Telegram captures (cross-cutting)
├── archive/                    ← superseded artifacts (forensic record; never deleted)
├── checkpoint.md
├── state.json
└── README.md
```

## Por qué 2 etapas

Mapeo al 6-fase pipeline de JP:

| Etapa local | Skills | JP Fase |
|---|---|---|
| `etapa_1_preparacion/` | 01-04 | Fase 1 (Contacto/Agendamiento) + Fase 2 (Preparación Pre-Llamada) + Fase 3 (Primera Llamada en `transcripciones/`) |
| `etapa_2_diagnostico/` | 05 | Fase 4 (Generación Reporte) + Fase 5 (Revisión Interna) + Fase 6 (Entrega + Seguimiento via `communications/`) |

Etapas futuras (propuesta comercial, contrato, implementación, seguimiento, retainer) se añaden como `etapa_3_*`, `etapa_4_*` etc. **cuando un cliente realmente alcanza esa etapa** — no se pre-construyen vacías.

**Folders never move.** Phase tracked in `state.json`.

## Cross-cutting folders

| Folder | Holds |
|---|---|
| `communications/` | Email + WhatsApp + Telegram captures across all stages |
| `archive/` | Superseded artifacts (kept for forensic record; never deleted) |

**Note:** `transcripciones/` vive dentro de `etapa_2_diagnostico/` porque las transcripciones son input para el Skill 05 (no son cross-cutting — son producto post-reunión).

## `state.json`

Schema: `nexostrat-client-state-v1` (full schema landed in Plan 03 alongside the
event-spine validators). Required fields: `client`, `name`, `country`, `sector`,
`started`, `owner`, `phase`, `phase_history[]`, `pilot`, `pricing`, `next_action`,
`kpis`, `blockers[]`, `tags[]`, `recording_preference`.

Phase values activos:
- **Pre-engagement:** `prospect → intake → exploring → diagnostico_pendiente`
- **Post-diagnostico:** `diagnostico_delivered → propuesta_pendiente → propuesta_sent → propuesta_{accepted,rejected,revising}`
- **Active:** `cliente_firmado → diseño → implementación → seguimiento_30 → seguimiento_60 → seguimiento_90 → retainer_active`
- **Terminal:** `churned`, `nurture`, `retainer_paused`
- **Pilot-only:** `pilot_archived` (companies used for toolchain validation; never engaged)

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
- `README.md` replaced with a per-client stub.
- `etapa_1_preparacion/00_intake/research_input.md` + `our_hypotheses.md` copied from `skills/shared/` and slug-stamped.

## Post-scaffold workflow (the canonical handoff)

1. **Fill `etapa_1_preparacion/00_intake/research_input.md`** — facts only. Identity, presence, contacts, origin of the prospect, 5-min LinkedIn pre-trabajo. **Do NOT write hypotheses here.**
2. **Fill `etapa_1_preparacion/00_intake/our_hypotheses.md`** — judgment only. What we think the dolor is, the decisor read, presupuesto estimate, tono, sensibilidades, capability-fit hypotheses, things we expect research to confirm or refute. **This file is SEALED during Skills 01-03** per ADR-027 — the operator must not paste its content into the model while running the research skills.
3. **Trigger the pipeline.** In Claude Code at `/srv/Nexostrat/`, say:

   > `Analiza <slug>`

   Claude reads `state.json` (confirms fresh `prospect` intake), reads `etapa_1_preparacion/00_intake/research_input.md`, and invokes Skill 01 (company-analyst). Output lands at `etapa_1_preparacion/01_analisis_compania/runs/<ts>_mode-a/final_report.{md,docx}`.
4. **Human review** entre cada skill. Read Skill 01's output, correct what we know better, then continue to Skill 02 → review → Skill 03 → review → Skill 04. Skill 04 (PrepLlamada) is the **first skill that reads `our_hypotheses.md`**.
5. **30-min discovery call** con el cliente, grabado. PrepLlamada es la guía. El audio + transcripts caen en `etapa_2_diagnostico/transcripciones/<fecha>_<topic>/`.
6. **Skill 05 (internal-report)** consume 01+02+03+notas-reunión+our_hypotheses → produce el Reporte de Oportunidades en `etapa_2_diagnostico/reporte_interno/runs/<ts>_mode-a/`.
7. **Revisión interna obligatoria Ricardo+JP** (Fase 5 en JP's pipeline diagram) antes del envío manual.

## What's NOT here

Per Plan 01a scope, this template is structural only. Skill-specific scaffolding
(prompts/v1.md, templates, benchmarks) lives at `skills/<NN>_<name>/` and is
populated in Plans 05-06.
