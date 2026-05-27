# Pipeline Redesign — Skill 5 internalization + Skill 6 client deliverables + Skill 7 placeholder

> **Status:** PROPOSED (brainstorm session 2026-05-27)
> **Author:** Ricardo + Claude (brainstorming session)
> **Inputs that fed this spec:**
> - JP whiteboard photo `photo_2026-05-27_09-19-53.jpg`
> - Prior pipeline analysis deck `Nexostrat_Analisis_Pipeline.html` (session 17)
> - Ricardo↔JP call transcript `/srv/meetings/nexostrat/2026-05-27/2026-05-27_06-58_skill6-redesign/transcript.txt` + summary
> - Trixx session-20 outputs as test-skeleton input for Skill 6
> - Existing skill inventory (5 production + 2 design-strategy + 2 technical = 9 skills)

---

## 1. Executive Summary

The Nexostrat delivery pipeline is being restructured into two clear stages with explicit human-in-the-loop checkpoints. Skill 5 changes from a client-facing report to an **internal Nexostrat-facing** analysis. A new Skill 6 produces the **standardized client deliverables** (.docx 5 pages + .pptx 10 slides) after a structured Claude↔Ricardo curation conversation. A future Skill 7 (placeholder spec only today) produces the full paid roadmap if the client accepts the Skill 6 invitation.

The redesign also introduces a multi-engine transcription canon, folder renames, and an internal HTML deck documenting how Nexostrat works for any current/future operator.

---

## 2. Context & Motivation

**Trigger** — Session 20 (2026-05-26) ran the existing Skill 5 (`opportunity-report`) end-to-end on Trixx Logistics and produced a 10-opportunity client-facing deliverable. JP joined Nexostrat the day those deliverables were sent to him for review. The Ricardo↔JP call on 2026-05-27 designed the new flow we are now formalizing.

**The 3 problems the old pipeline had:**

1. **Skill 5 mixed two audiences**: it tried to be both Nexostrat's analytical depth and the client's reading deliverable in a single artifact. The result was 90% client-facing + 10% Nexostrat invitation — but in practice Ricardo wanted a different cut for each audience.
2. **No standardized client deliverable**: each pilot (Bodai, Ascenso, Scarab, Trixx) produced reports in slightly different shapes. Hard to scale, hard to recognize.
3. **No structured curation step**: Ricardo's judgment of "what to surface, what to hide, what tone" lived only in his head between Skill 5's output and whatever he sent the client. The redesign makes this curation an explicit artifact.

**What changes:**

| Aspect | Before | After |
|---|---|---|
| Skill 5 audience | Client (90%) + Nexostrat hook (10%) | Nexostrat 100% (internal) |
| Client-facing deliverable | Skill 5's `.docx` (~30-50 pages) | Skill 6's standardized `.docx` (5pp) + `.pptx` (10 slides) |
| Curation step | Implicit in Ricardo's head | Explicit `brief_cliente.md` artifact, Claude conducts the conversation |
| Hoja de Ruta + costos | Inside Skill 5 (free) | Mini preview in Skill 6 + full version in Skill 7 (paid, post-acceptance) |
| Standardization | Ad-hoc per client | 4-section structure rigid across all clients; densidad flexible |

---

## 3. Pipeline Overview

```
ETAPA 1 — PRE-MEETING (preparación)

  Skills 01-04 ejecutados serialmente con revisión humana entre cada uno:
    Skill 01 company-analyst       (current, no change)
    Skill 02 industry-analyst      (current, no change)
    Skill 03 competitor-analyst    (current, no change)
    Skill 04 discovery-meeting     (current, no change)
    └─ Conversación Claude↔Ricardo post-Skill-4:
       ajusta el output de Skill 4 → produce script final de reunión

REUNIÓN CON CLIENTE
  Grabación → transcripción (multi-engine, WhisperX default)
  Stack: WhisperX large-v3 + diarización pyannote + Apple Voice Memos +
         Gemini multimodal (summary only) + screen-recorder built-in + Claude

ETAPA 2 — POST-MEETING (diagnóstico + entrega)

  Skill 05 internal-report        (RENAMED, REPROFILED)
    Audiencia: Nexostrat (Ricardo + JP)
    Contenido: análisis completo + posibilidades + procesos automatizables
              + implementaciones que Nexostrat puede entregar + gaps
              internos + cosas a NO decir al cliente
    └─ Conversación Claude↔Ricardo (Claude conduce):
       lee Skill 5 + transcript + reportes Skills 01-03
       pregunta una-a-una los campos del template
       → produce brief_cliente.md (artefacto-puente versionado)

  Skill 06 client-deliverables    (NEW)
    Input: brief_cliente.md + reportes upstream + transcript
    Output: <Cliente>_Diagnostico_<date>.docx (5pp)
            <Cliente>_Diagnostico_<date>.pptx (10 slides)
    Renderers:
      - .docx via nexostrat-editorial-designer + docx (técnico)
      - .pptx via nexostrat-pptx-expert + pptx (técnico)
    Revisión obligatoria Ricardo + JP antes de envío.

  Entrega manual al cliente (siempre personal, nunca automatizada en primer envío).

SI CLIENTE APRUEBA (post-presentación)
  Skill 07 implementation-roadmap (PLACEHOLDER — spec-only hoy)
    Hoja de Ruta completa + propuesta paga con scope detallado.
    Construcción real: después de 1-2 corridas reales de Skill 6.
```

---

## 4. Strategic Decisions Locked (Q&A 2026-05-27)

| # | Decisión | Valor locked |
|---|---|---|
| Q1 | Lente del entregable Skill 6 | **(b) Mini-diagnóstico standalone con valor accionable independiente del cierre** |
| Q2 | Estructura del entregable | **(b2) Espejo del cliente → Espejo de lo posible (4 secciones)** |
| Q3 | Relación Word ↔ PPTX | **(ii) Dos entregables paralelos, brief compartido** |
| Q4 | Artefacto-puente | **(ii) Template estructurado `brief_cliente.md`; Claude conduce la conversación** |
| Q5 | Formatos de salida | **(α) Solo .docx + .pptx (HTML descartado del flujo automático)** |
| Q6 | Rigidez estandarización | **(II) Estructura rígida (4 secciones siempre), densidad flexible (rangos por sección)** |
| Sec 2 | Título Sección 2 | **"Movimientos del Sector"** (temporal — re-evaluar tras 2-3 pilotos) |
| Set títulos | Conjunto B refinado | Diagnóstico Operacional / Movimientos del Sector / Frentes de Oportunidad / Próximos Pasos |
| v1→v2 | Iteración (e.g., Andrea preview) | **Runs independientes** — no soporte nativo de versioning; Ricardo corre Skill 6 N veces |

**Reglas de lenguaje locked** (del transcript JP + Ricardo guardrails):

- **Decir QUÉ se puede hacer, no QUÉ comprar** — describir capacidades en lenguaje de operación, no de tecnología
- **Bajar la frecuencia de "AI"** — solo cuando aporte valor concreto al insight
- **Específico Trixx (y plantilla general)**: evitar "bot"/"agente" (la gente lo asocia con robots físicos) — usar "automatización", "compilador", "sistema que organiza", "asistente de información"
- **Lenguaje JP locked**: NO "menor impacto" → SÍ "menores disrupciones" + "mayor productividad"
- **Posicionamiento**: la solución hace al equipo MÁS productivo, NO reemplaza personas

---

## 5. Skill 5 — Internal Report (Reprofiled)

**Antes**: `skills/05_opportunity_report/` (slug `opportunity-report`) — client-facing.

**Después**: `skills/05_internal_report/` (slug `internal-report`) — Nexostrat-facing.

**Audiencia**: Ricardo + JP exclusivamente.

**Inputs** (sin cambio vs. hoy):
- `etapa_1_preparacion/01_analisis_compania/runs/<latest>/`
- `etapa_1_preparacion/02_analisis_industria/runs/<latest>/`
- `etapa_1_preparacion/03_analisis_competencia/runs/<latest>/`
- `etapa_2_diagnostico/transcripciones/<latest>/transcript_final.md`
- `etapa_2_diagnostico/transcripciones/<latest>/NotasCliente_*.md` (curado anti-hallucination con ✅⚠️❓)

**Outputs**:
- `etapa_2_diagnostico/reporte_interno/runs/<date>_mode-a/<Cliente>_ReporteInternoNexostrat_<date>.md`
- `<Cliente>_ReporteInternoNexostrat_<date>.docx` (renderizado vía `nexostrat-editorial-designer` + `docx`)

**Contenido del reporte interno** (estructura propuesta, ajustable):

1. Resumen ejecutivo para Nexostrat (3-5 líneas + decisión propuesta)
2. Diagnóstico operacional profundo (sin filtros, completo — sirve a Ricardo y JP)
3. Movimientos del sector + competidores relevantes (incluye benchmarks aspiracionales)
4. Catálogo completo de oportunidades (todas las identificadas, no recortadas — 10-15 típicamente)
5. **Implementaciones que Nexostrat puede entregar** (matched contra capabilities reales — esto es nuevo)
6. **Quick Wins recomendados** (con scoring del current Skill 5)
7. **Gaps + riesgos internos** (cosas que sabemos pero no contamos al cliente — esto es nuevo)
8. **Curaduría sugerida para el brief_cliente** (qué de lo de arriba SÍ va al cliente, qué NO — esto es nuevo)
9. Conclusiones para Ricardo + JP

**Cambio del bug fix de session 20** (parser `Oportunidades encontradas: 0`): la patch v0.3 ya está aplicada. Conservar en la nueva versión Skill 5.

---

## 6. Bridge Artifact — `brief_cliente.md`

**Path**: `pipeline/clients/<slug>/etapa_2_diagnostico/brief_cliente/runs/<date>_mode-a/brief_cliente.md`

**Producido por**: La conversación Claude↔Ricardo posterior a Skill 5. Claude conduce. Cada run del Skill 6 puede tener su propio brief_cliente.md (runs independientes).

**Template** (versión 1.0 — evolucionará con experiencia):

```markdown
---
client_slug: <slug>
meeting_date: <YYYY-MM-DD>
run_date: <YYYY-MM-DD>
run_label: <e.g., "v1-andrea-preview" o "v2-formal-meeting">
target_audience: <e.g., "Andrea (preview)" o "María Helena + Hector (formal)">
---

# Brief al Cliente — <Cliente>

## 0. Metadata
- Sector: <e.g., Logística cross-border MX-USA>
- Decisor real: <persona + rol>
- Influenciador clave: <persona + rol>
- Tono dominante: <urgente | tranquilo | técnico | ejecutivo>
- Idioma: <es-MX | es-CO>

## 1. Sección 1 — Diagnóstico Operacional
### Hallazgos a destacar (3-4)
1. <título corto>
   - Descripción 2-3 líneas
   - Quote verbatim: "..."
2. ...

### Hallazgos del reporte interno que NO incluimos y por qué
- <hallazgo>: <razón>

## 2. Sección 2 — Movimientos del Sector
### Movimientos a mostrar (2-3)
1. <movimiento>: <por qué importa a ESTE cliente>
2. ...

### ¿Mencionamos competidor por nombre?
- <Competidor X>: SÍ / NO — <razón>

## 3. Sección 3 — Frentes de Oportunidad
### Frentes a presentar (3-5)
1. <título en lenguaje de operación, NO tecnología>
   - QUÉ resuelve (2-3 oraciones)
   - Beneficio en términos de productividad/claridad/menor disrupción
   - Términos a evitar: <e.g., "bot", "AI" — específico cliente>

### Frentes del reporte interno que NO mostramos y por qué
- <frente>: <razón>

## 4. Sección 4 — Próximos Pasos
### Mini-roadmap (3-4 pasos)
1. <paso>: <rango cualitativo: "inversión moderada · ~4 semanas">
2. ...

### Tipo de inversión
- Cualitativa ("inversión moderada") o cuantitativa ("USD X-Y"): <pick>

### CTA al Skill 7
- Soft ("conversemos los siguientes pasos") o explícito ("Plan Detallado de Implementación"): <pick>

## 5. Decisiones de curaduría cross-cutting

### Language guardrails (extensión del default)
- Términos baneados para ESTE cliente: <lista>
- Términos preferidos: <lista>
- Vocabulario JP global (siempre aplicado): "menores disrupciones" + "mayor productividad" + "el equipo más productivo, no reemplaza personas"

### Énfasis tonal específico
- <2-3 líneas>

### Distribución de densidad (override de defaults si aplica)
- Word: sec 1=<Xpp>, sec 2=<Xpp>, sec 3=<Xpp>, sec 4=<Xpp>, total=5pp
- PPTX: sec 1=<X slides>, sec 2=<X slides>, sec 3=<X slides>, sec 4=<X slides>, cover=1, total=10
- Defaults si no hay override:
  - Word: 1.5 / 1 / 1.5 / 1 = 5pp
  - PPTX: cover(1) + 2 + 2 + 4 + 1 = 10
```

**Conversational flow** (Claude conduce):

1. Lee Skill 5 internal report + Skills 01-03 outputs + transcript
2. Presenta el template vacío con metadata pre-llenada
3. Recorre las secciones en orden (Sección 1 → 2 → 3 → 4 → cross-cutting)
4. Por sección, hace 2-4 preguntas con opciones cortas (sí/no, listas pre-pobladas del reporte interno)
5. Si Ricardo salta a otra sección, Claude vuelve al orden cuando termina
6. Al final muestra el brief_cliente.md armado para confirmación
7. Una vez confirmado, invoca los renderers

---

## 7. Skill 6 — Client Deliverables (NEW)

**Path**: `skills/06_client_deliverables/`
**Slug**: `client-deliverables`

### Estructura de carpeta

```
skills/06_client_deliverables/
├── SKILL.md
├── CHANGELOG.md
├── scripts/
│   ├── conversation_runner.py     # Optional — todo puede vivir en SKILL.md
│   ├── generate_docx.py            # Llama editorial-designer + docx técnico
│   └── generate_pptx.py            # Llama pptx-expert + pptx técnico
├── templates/
│   ├── brief_cliente.template.md   # El template canónico
│   ├── word_master.docx            # Aurora-branded master (deriva de editorial-designer)
│   └── pptx_master.pptx            # Aurora-branded master (deriva de pptx-expert 12-layout template)
└── tests/
    └── test_skill6.sh              # Smoke tests
```

### Inputs

| Input | Path | Rol |
|---|---|---|
| Reporte interno | `etapa_2_diagnostico/reporte_interno/runs/<latest>/*.md` | Análisis base |
| Brief al cliente | `etapa_2_diagnostico/brief_cliente/runs/<this-run>/brief_cliente.md` | Curaduría — output de la conversación |
| Transcript final | `etapa_2_diagnostico/transcripciones/<latest>/transcript_final.md` | Quotes verbatim |
| Notas cliente | `etapa_2_diagnostico/transcripciones/<latest>/NotasCliente_*.md` | Tags ✅⚠️❓ |
| Metadata cliente | `etapa_1_preparacion/00_intake/research_input.md` | Logo, nombre, sector, fecha reunión |
| Reportes upstream | `etapa_1_preparacion/0{1,2,3}_*/runs/<latest>/*.md` | Contexto para sec 1, 2 |

### Outputs

```
pipeline/clients/<slug>/etapa_2_diagnostico/entregables/runs/<date>_mode-a/
├── <Cliente>_Diagnostico_<date>.docx   # 5pp client-facing
├── <Cliente>_Diagnostico_<date>.pptx   # 10 slides client-facing
└── _generation_log.md                   # qué inputs se usaron, qué decisions del brief
```

### Estructura de los entregables — Word (5 páginas + carátula)

**Carátula** (página 0, separada — no cuenta)
- Logo Nexostrat (sup izq), Cliente + sector (sup der)
- Título: *Diagnóstico Operacional y Frentes de Oportunidad*
- Sub: *Preparado para [Cliente] · Reunión del [fecha]*
- Footer: *Nexostrat | [fecha emisión]* (sin "Confidencial" — decisión: muy legal-pesado)

**Sección 1 — Diagnóstico Operacional** (default 1.5pp, rango 0.5–2pp)
- Intro 2-3 líneas anclando la reunión
- 3-4 hallazgos numerados en prosa (no bullets):
  - Título corto (max 10 palabras)
  - 2-3 oraciones de descripción
  - Quote verbatim del cliente (cursiva, sangría)

**Sección 2 — Movimientos del Sector** (default 1pp, rango 0.5–2pp)
- Intro 1 oración
- 2-3 movimientos en prosa: QUÉ se mueve + POR QUÉ importa a este cliente
- Mención a competidor por nombre solo si brief_cliente lo aprueba

**Sección 3 — Frentes de Oportunidad** (default 1.5pp, rango 0.5–2pp)
- Intro 2 líneas conectando diagnóstico → frentes
- 3-5 frentes en prosa numerada:
  - Título en lenguaje de operación
  - 2-3 oraciones del QUÉ se resuelve
  - Beneficio en términos JP (productividad / claridad / menor disrupción)
  - SIN mención a herramienta específica, SIN "AI"/"bot" salvo valor concreto

**Sección 4 — Próximos Pasos** (default 1pp, rango 0.5–2pp)
- Intro 1 oración
- 3-4 pasos secuenciales numerados con nombre + 1 oración + rango cualitativo de esfuerzo
- Bloque de cierre con CTA al **Plan Detallado de Implementación** (nombre comercial cliente-facing; internamente Skill 7)

### Estructura de los entregables — PPTX (10 slides)

| Slide | Sección | Contenido |
|---|---|---|
| 1 | Carátula | Logo + cliente + título + fecha reunión |
| 2 | Sección 1 — Diagnóstico Operacional (1/2) | 1-2 hallazgos: visual dominante + título + 1 oración + quote discreto |
| 3 | Sección 1 — Diagnóstico Operacional (2/2) | hallazgos restantes |
| 4 | Sección 2 — Movimientos del Sector (1/2) | Movimiento 1: gráfico simple + título + 1 oración |
| 5 | Sección 2 — Movimientos del Sector (2/2) | Movimiento 2 |
| 6 | Sección 3 — Frentes de Oportunidad (1/4) | Frente 1: diagrama antes/después + título + beneficio |
| 7 | Sección 3 — Frentes de Oportunidad (2/4) | Frente 2 |
| 8 | Sección 3 — Frentes de Oportunidad (3/4) | Frente 3 |
| 9 | Sección 3 — Frentes de Oportunidad (4/4) | Frentes 4-5 en grid 2x2 (la "ola completa") |
| 10 | Sección 4 — Próximos Pasos | Timeline horizontal 3-4 pasos + CTA al pie |

**Distribución default**: 1 cover + 2 + 2 + 4 + 1 = 10. Espejo exacto: 5 slides primera mitad / 5 slides segunda mitad.

**Reglas visuales globales**:
- Aurora palette + Inter
- 1 idea por slide
- Max ~50 palabras visibles por slide
- Whitespace > densidad
- Iconos y diagramas simples; cero stock photos
- Regla `nexostrat-pptx-expert`: cada slide comunica su idea en <5 segundos

**Distribución alternativa cuando material es flaco**: el brief_cliente.md puede override (e.g., 1+1+2+5+1 si Sección 3 tiene mucho material; 1+3+1+4+1 si Sección 1 tiene mucho material).

---

## 8. Skill 7 — Implementation Roadmap (PLACEHOLDER)

**Path**: `skills/07_implementation_roadmap/`
**Slug**: `implementation-roadmap`
**Estado hoy**: solo SKILL.md describiendo el contrato. Código real diferido hasta que tengamos 1-2 corridas reales de Skill 6.

**Contrato del Skill 7 (a refinar)**:
- **Trigger**: cliente aprueba el Diagnóstico de Skill 6 y firma contrato/pago de la fase paga
- **Inputs**: Skill 6 outputs + feedback del cliente en la presentación + nuevo intake post-aprobación
- **Outputs**: Hoja de Ruta detallada con scope, timeline mes-a-mes, milestones, costos cuantitativos exactos, criterios de éxito, riesgos, plan de comunicación

**Nombre comercial cliente-facing**: "Plan Detallado de Implementación" (más concreto que "Hoja de Ruta de IA" — menos riesgo de asustar con "IA" en el header)

---

## 9. Multi-Engine Transcription Canon

**Path del protocolo**: `00_META/protocols/meeting_transcription.md` (a crear)

| Engine | Rol | Estado | Validación |
|---|---|---|---|
| WhisperX large-v3 + diarización pyannote | **Primary** | ✅ Canon | Trixx session 20 + JP call hoy |
| Apple Voice Memos transcription | Secondary | ✅ Disponible | Trixx session 20 |
| Gemini multimodal | **Summary only** (NO transcription) | ⚠️ Hallucina en transcripción >20MB | Trixx session 20 — bug confirmado |
| Screen-recorder built-in | Experimental, comparativo | Probar en próximas reuniones | TBD |
| Claude multimodal | Experimental, comparativo | Probar en próximas reuniones | TBD |

**Stack canónico para una reunión cualquiera**:
1. Grabación (m4a / mkv / mp4)
2. `~/bin/summarize-meeting.sh "<file>" es --scope nexostrat --client-slug <slug> --topic <topic>` (o sin client-slug para internas)
3. WhisperX produce: `transcript.{txt,srt,vtt,tsv,json}`
4. Gemini multimodal produce: `summary.md`
5. (Opcional) Pasar el `.m4a` por Apple Voice Memos para segundo transcript comparativo
6. Reconciliar diferencias manualmente y producir `transcript_final.md` con speakers mapeados + 10-20 hotword corrections
7. Curar `NotasCliente_<date>.md` con tags ✅ (verbatim) / ⚠️ (estimado) / ❓ (hipótesis)

**Hardware**: si las reuniones presenciales requieren mejor audio, comprar micrófono — Ricardo dispuesto.

---

## 10. Skill + Folder Renames

### Skills

| Antes | Después | Tipo |
|---|---|---|
| `skills/05_opportunity_report/` | `skills/05_internal_report/` | Renombrado |
| Slug `opportunity-report` | Slug `internal-report` | Frontmatter SKILL.md cambia |
| SKILL.md audiencia: cliente | SKILL.md audiencia: Nexostrat | Reescrito |
| `pipeline/clients/<slug>/etapa_2_diagnostico/reporte_oportunidades/` | `.../reporte_interno/` | Cliente-side rename |
| (no existía) | `skills/06_client_deliverables/` (slug `client-deliverables`) | NEW |
| (no existía) | `skills/07_implementation_roadmap/` (slug `implementation-roadmap`) | NEW (placeholder) |
| (no existía) | `pipeline/clients/<slug>/etapa_2_diagnostico/brief_cliente/` | NEW dir |
| (no existía) | `pipeline/clients/<slug>/etapa_2_diagnostico/entregables/` | NEW dir |

### Migración de Trixx (precaución)

Trixx session 20 ya corrió bajo paths antiguos. El plan de migración debe:
1. Preservar los runs históricos en su path original (no romper trazabilidad)
2. Para el próximo run de Trixx, usar los nuevos paths
3. Documentar en `pipeline/clients/trixx-logistics/MIGRATION_NOTE.md` qué cambió

---

## 11. Inventory of Skills (State 2026-05-27 post-instalación)

### Instalados y activos (9)

| # | Skill | Folder | Slug | Tipo | Notas |
|---|---|---|---|---|---|
| 1 | Company Analyst | `skills/01_company_analyst/` | `company-analyst` | Productor | — |
| 2 | Industry Analyst | `skills/02_industry_analyst/` | `industry-analyst` | Productor | — |
| 3 | Competitor Analyst | `skills/03_competitor_analyst/` | `competitor-analyst` | Productor | — |
| 4 | Discovery Meeting | `skills/04_discovery_meeting/` | `discovery-meeting` | Productor | — |
| 5 | Opportunity Report | `skills/05_opportunity_report/` | `opportunity-report` | Productor (a reprofile) | Será renombrado a `internal-report` |
| 6 | Nexostrat PPTX Expert | `skills/pptx_expert/` | `nexostrat-pptx-expert` | Design strategy | — |
| 7 | Nexostrat Editorial Designer | `skills/nexostrat_editorial_designer/` | `nexostrat-editorial-designer` | Design strategy | **Instalado 2026-05-27**; pequeño fix pendiente (Century Gothic → Inter, "PYMEs colombianas" → LATAM) |
| 8 | Technical PPTX | `skills/pptx_technical/` | `pptx` | Technical execution | **Instalado 2026-05-27** desde Anthropic skills repo |
| 9 | Technical DOCX | `skills/docx_technical/` | `docx` | Technical execution | **Instalado 2026-05-27** desde Anthropic skills repo |

### A construir desde 0 (2)

| # | Skill | Cuándo | Bloqueado por |
|---|---|---|---|
| 10 | Client Deliverables (Skill 6) | Sprint próximo | Plan de implementación |
| 11 | Implementation Roadmap (Skill 7) | Placeholder hoy + código tras 1-2 corridas Skill 6 | Aprendizaje de corridas reales |

### Pending JP (3, sin fecha)

| Skill | Estado | Decisión al recibir |
|---|---|---|
| Nexus Thread PPT Expert | JP en construcción | Comparar contra `nexostrat-pptx-expert` actual; decidir si reemplaza o coexiste |
| Editorial Designer (versión JP) | **YA ENTREGADO 2026-05-27** | Instalado |
| HTML Interactive Presentations | JP en construcción | Potencial motor del deck interno Nexostrat (sec 13) |

### Nota de licencia (technical pptx + docx de Anthropic)

Los skills `pptx` y `docx` técnicos vienen del repo público `github.com/anthropics/skills`. Su LICENSE.txt es **source-available, NOT open source**: "Use of these materials... governed by your agreement with Anthropic regarding use of Anthropic's services." Restricciones: no extraer fuera de los Services, no redistribuir, no derivative works.

Interpretación operativa: Claude Code es un Anthropic Service; uso local dentro de él calza. Pero a largo plazo (post-pilotos), si la operación crece más allá de Claude Code como host, conviene migrar a wrappers propios sobre `python-pptx` + `python-docx` para eliminar dependencia.

**Acción en plan**: documentar este punto en `00_GOVERNANCE/decisions/`.

---

## 12. HTML Internal Deck — "Cómo funciona Nexostrat por dentro"

**Path**: `operations/internal/2026-05-27_nexostrat-pipeline-deck.html` (committed; subsiguientes versiones bumpean fecha)

**Propósito**: documento interno de uso Nexostrat (Ricardo + JP + cualquier futuro operator). Clear y organizado para que cualquier persona entienda y vea cómo funciona Nexostrat por dentro. NO es para clientes.

**Estilo visual**: hereda del Aurora deck `Nexostrat_Analisis_Pipeline.html` (Midnight + Sky Blue + Inter, single-page deck).

**Estructura propuesta — menús expandibles** (per Ricardo's directive: no saturar de información):

1. **Visión general** — qué es Nexostrat, propuesta de valor, posicionamiento explícito alejado de "robots físicos" (lenguaje JP del transcript)
2. **El pipeline en 1 imagen** — diagrama replicando el whiteboard de JP, cada nodo cliqueable
3. **Etapa 1 — Pre-meeting** (expandible)
   - Skill 01, 02, 03 con propósito de cada uno
   - Skill 04 + conversación post-Skill-4 (script de reunión)
4. **Reunión con cliente** (expandible)
   - Stack multi-engine de transcripción
   - Disciplina de captura
5. **Etapa 2 — Post-meeting** (expandible)
   - Skill 05 Internal Report
   - Conversación Claude+Ricardo → brief_cliente.md (con las 4 secciones)
   - Skill 06 Client Deliverables (.docx + .pptx)
   - Revisión interna obligatoria
6. **Si el cliente aprueba** (expandible)
   - Skill 07 Implementation Roadmap (paga, scope detallado)
7. **Inventario de skills** (expandible)
   - Instalados, faltantes, pending JP, a construir
8. **Decisiones de diseño** (expandible)
   - Lente (b), Set B títulos, Word↔PPTX paralelos, brief estructurado, formatos α, rigidez II, vocabulario JP
9. **Outputs por cliente** (expandible)
   - Folder structure final con árbol completo
10. **Cómo arranco un cliente nuevo** (expandible, operativo)
    - Comando a comando

**Anchored to JP's whiteboard**: el diagrama del pipeline en (2) debe replicar visualmente la imagen de JP (`photo_2026-05-27_09-19-53.jpg`) — un homenaje a la versión original + facilita el reconocimiento.

---

## 13. Brain-Side Plan Verification — SEPARATE WORKSTREAM

> **DECISIÓN 2026-05-27 (post-aprobación spec)**: Ricardo aclaró que el HTML deck de Nexostrat y la verificación del Telegram hub son **dos workstreams separados**. Esta sección queda como NOTA documentada — la verificación brain-side se levanta como tarea independiente DESPUÉS de cerrar el flow redesign completo (spec + HTML deck + skills 5/6/7). NO entra en la implementación de esta redesign.

Ricardo flag original: "Nexostrat cobra prioridad sobre todo el sistema, solo debemos verificar que cambios se debe implementar a la actualización e implementación del telegram hub."

**Step terminal del plan**: verificar impactos de este redesign en los 3 plans brain-side:

**IMPORTANTE**: los puntos abajo son **hipótesis de impacto SIN VERIFICAR** (los plans no se leyeron a fondo durante este brainstorm). El paso terminal del implementation plan lee los 3 plans y produce un findings doc real.

1. `/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-master-plan.md`
   - A verificar: ¿el meeting-pipeline overhaul brain-side referencia el path `reporte_oportunidades/` que estamos renombrando a `reporte_interno/`?
   - A verificar: ¿Phase 0a checkboxes Nexostrat-surface se ven afectadas por el rename de Skill 5?
   - A verificar: ¿el confidence-threshold 0.85 + tasks.json v2 schema siguen aplicando sin cambio?

2. `/srv/brain/00_META/governance/plans/2026-05-25_meetings-pipeline-overhaul-deployment.md`
   - A verificar: ¿el deployment-side asume paths o slugs Nexostrat que cambiamos?

3. `/srv/brain/00_META/governance/plans/2026-05-22_brain_bot_platform_implementation.md`
   - A verificar: ¿el Telegram bot Nexostrat-tenant ofrece slash commands que deban actualizarse (e.g., `/skill6 <cliente>`, `/brief <cliente>`)?
   - A verificar: ¿la tenant config del bot necesita conocer las nuevas paths (`reporte_interno/`, `brief_cliente/`, `entregables/`)?

**Mecánica**: al cerrar la implementación de Nexostrat-side, abrir un memo a brain-architect en `/srv/brain/00_META/inbox/` (Strict Rule 1 cross-scope: memo, no edición directa) listando los puntos arriba.

---

## 14. Implementation Order (sequencing)

Propuesta de orden — refinable en writing-plans:

```
Fase A — Dependencias + inventario (sin breaking changes)
  A1. ✅ Instalar editorial-designer (DONE)
  A2. ✅ Instalar pptx técnico + docx técnico (DONE)
  A3. Fix descripciones editorial-designer (Inter only + LATAM)
  A4. Crear 00_META/protocols/meeting_transcription.md
  A5. Documentar Anthropic license note en 00_GOVERNANCE/decisions/

Fase B — Renames + reprofile (breaking changes contenidos)
  B1. Renombrar skills/05_opportunity_report/ → skills/05_internal_report/
  B2. Cambiar slug opportunity-report → internal-report
  B3. Reescribir SKILL.md de Skill 5 (audiencia Nexostrat, no cliente)
  B4. Actualizar test_skills.sh registry
  B5. Actualizar todas las referencias (~9-15 archivos) en el repo
  B6. Renombrar paths client-side: reporte_oportunidades → reporte_interno
  B7. Crear MIGRATION_NOTE.md en trixx-logistics/
  B8. Verificar test harness: 32 PASS → ajustar a nueva cantidad esperada

Fase C — Construir Skill 6 (nuevo skill core)
  C1. Crear skills/06_client_deliverables/ skeleton
  C2. Escribir SKILL.md con flujo conversacional
  C3. Escribir templates/brief_cliente.template.md
  C4. Construir templates/word_master.docx (vía editorial-designer)
  C5. Construir templates/pptx_master.pptx (vía pptx-expert template)
  C6. Implementar scripts/generate_docx.py
  C7. Implementar scripts/generate_pptx.py
  C8. Escribir tests/test_skill6.sh
  C9. Smoke test contra reporte interno de Trixx (test-as-skeleton)
  C10. .claude/skills/client-deliverables symlink + verificar disponibilidad

Fase D — Skill 7 placeholder
  D1. Crear skills/07_implementation_roadmap/SKILL.md (solo descripción + contrato; sin scripts)
  D2. .claude/skills/implementation-roadmap symlink (opcional, decide si exponer ya)

Fase E — Smoke test end-to-end con Trixx (test-as-skeleton)
  E1. Correr Skill 5 nuevo (internal) sobre Trixx → producir reporte_interno
  E2. Conversación Claude↔Ricardo → producir brief_cliente.md
  E3. Correr Skill 6 → producir .docx + .pptx
  E4. Revisar entregables contra el doc client-facing original de session 20
  E5. Iterar lo que sea necesario
  E6. Documentar lessons learned para template v2

Fase F — HTML Internal Deck
  F1. Diseñar layout (Aurora-styled, expandible, single-page)
  F2. Escribir contenido por sección
  F3. Implementar interactividad (menús expandibles)
  F4. Diagrama del pipeline replicando whiteboard JP
  F5. Test en navegador

Fase G — Brain-side coordination (REMOVIDA — workstream separado)
  Por decisión 2026-05-27, esta verificación se levanta como tarea
  independiente DESPUÉS de cerrar el flow redesign. Ver sec 13.

Fase H — Cleanup + commits
  H1. Update STATUS.md
  H2. Update CHECKPOINT.md
  H3. Journal entry
  H4. Commits + push
```

**Bloqueos**:
- C depende de A2, A3 (dependencias instaladas)
- E depende de B + C (renombrado + skill 6 listo)
- F puede correr en paralelo a C/D/E
- G es terminal — corre último

**Estimación gross**: ~3-5 sesiones de trabajo dependiendo de qué tan profundo el smoke test en E.

---

## 15. Open Items / Deferred

1. **Iteración v1→v2 nativa**: descartada hoy (runs independientes). Re-evaluar si los pilotos generan fricción operativa.
2. **Sección 2 "Movimientos del Sector"**: si tras 2-3 pilotos sale floja, evaluar collapsar a 3 secciones.
3. **Distribución default 1+2+2+4+1 = 10 slides**: refinable según evidencia de los pilotos.
4. **Quick Wins scoring del Skill 5 actual**: preservar en Skill 5 internal; decidir si Skill 6 lo expone al cliente o solo informa el brief.
5. **Pricing concreto** ($1,500 USD setup + suscripción mensual del bot WhatsApp ejemplo): usar como punto de calibración del rango cualitativo de Skill 6, no como número público hasta confirmar.
6. **Buyer Persona doc pendiente** (Ricardo le debe respuestas a JP): no bloquea este redesign pero está en la cola.
7. **Skill 7 código real**: diferido post-pilotos.
8. **Skills incoming JP** (Nexus Thread PPT Expert + HTML interactive): integrar cuando lleguen.
9. **License migration off Anthropic source-available skills**: re-evaluar si Nexostrat opera fuera de Claude Code en el futuro.

---

## 16. Decisions Log (one-line summary)

| Decisión | Locked |
|---|---|
| Lente del entregable | Mini-diagnóstico standalone con valor accionable independiente del cierre |
| Estructura | 4 secciones espejo (Diagnóstico / Movimientos / Frentes / Próximos Pasos) |
| Densidad | Estructura rígida + densidad flexible (rangos por sección) |
| Páginas/slides | Word 5pp + PPTX 10 slides + carátula separada |
| Word ↔ PPTX | Paralelos con brief compartido |
| Bridge artifact | `brief_cliente.md` estructurado; Claude conduce conversación |
| Output formats | Solo .docx + .pptx (no HTML automático) |
| Sección 2 título | "Movimientos del Sector" (temporal) |
| Skill 5 audiencia | Nexostrat-internal, NO cliente |
| Skill 6 | NEW — `client-deliverables` |
| Skill 7 | Placeholder spec-only hoy |
| Vocabulario | Sin "AI"/"bot" excesivo; "menores disrupciones" + "mayor productividad"; "el equipo más productivo, no reemplazo" |
| Transcripción canon | WhisperX large-v3 + pyannote primary; Gemini summary only |
| Renames | 05 → internal-report; 06 + 07 nuevos; paths client-side actualizadas |
| HTML deck interno | A construir; estilo Aurora; menús expandibles; replica whiteboard JP |
| Anthropic license | Source-available — uso intra-Claude-Code OK; revisar largo plazo |
| Nexostrat priority | Prioritario sobre brain-side; verificar impactos en 3 plans al final |

---

## 17. Change Log

| Date | Description |
|------|-------------|
| 2026-05-27 | Initial spec from brainstorm session (Q1-Q6 + bloque presentation Claude+Ricardo) |
