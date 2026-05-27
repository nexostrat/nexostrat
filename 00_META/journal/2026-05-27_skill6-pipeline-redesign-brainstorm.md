# Session 21 — Pipeline Redesign Brainstorm (Skill 5 reprofile + Skill 6 NEW + Skill 7 placeholder)

**Date:** 2026-05-27
**Operator:** Ricardo
**Persona:** Founder
**Duration:** ~5-6 h wall-time
**Outcome:** Spec aprobado + HTML deck construido + 3 skills nuevos instalados + transcripción JP call

## Lo que pasó

Sesión 21 abrió en formato Q&A para reconfigurar el pipeline de consultoría Nexostrat. Trigger: JP se sumó formalmente a Nexostrat al recibir los entregables Trixx del session 20, y la llamada Ricardo↔JP de la mañana (2026-05-27 06:58 AM, 117 min) propuso una restructura significativa de cómo el flujo produce valor para el cliente.

El brainstorm se ancló en dos referencias visuales:
1. **Whiteboard de JP** (`photo_2026-05-27_09-19-53.jpg`) — diagrama hand-drawn del pipeline 6-skill que JP esbozó esta mañana, con Skill 5/6 explícitos + outputs y los loops de cierre/seguimiento.
2. **HTML deck previo** (`Nexostrat_Analisis_Pipeline.html`) — el Aurora-styled deck de sesión 17, como referencia de tono visual.

### El cambio de fondo

El pipeline viejo tenía Skill 5 ("opportunity-report") como entregable cliente-facing único — 90% valor + 10% gancho a la Hoja de Ruta paga. En la práctica, eso colapsaba dos audiencias en un solo artefacto y dejaba la curaduría tonal en la cabeza de Ricardo. El redesign separa:

- **Skill 5 reperfilada** → reporte interno Nexostrat, sin filtros, lo lee Ricardo + JP (no el cliente)
- **Conversación Claude↔Ricardo** → produce `brief_cliente.md`, un artefacto estructurado de curaduría versionado (Claude conduce, te pregunta una-a-una los campos del template; no es free-form)
- **Skill 6 nueva** → orquesta 2 renderers (.docx 5pp + .pptx 10 slides) en formato estandarizado para todo cliente (4 secciones espejo)
- **Skill 7 placeholder** → Hoja de Ruta paga completa, post-aprobación cliente; spec-only hoy

### Brainstorm Q&A — decisiones locked

Recorrí 6 preguntas estructuradas en orden, cada una con 2-3 opciones + recomendación. Ricardo eligió:

| # | Decisión | Pick |
|---|---|---|
| Q1 | Lente del entregable | (b) Mini-diagnóstico standalone — valor accionable independiente del cierre |
| Q2 | Estructura | (b2) 4 secciones espejo (cliente primero / posibilidad después) |
| Q3 | Relación Word ↔ PPTX | (ii) Paralelos, brief compartido — Word para reading, PPTX para presenting |
| Q4 | Bridge artifact | (ii) Template estructurado + Claude conduce la conversación |
| Q5 | Formatos output | (α) Solo .docx + .pptx (HTML descartado del flujo automático) |
| Q6 | Rigidez estandarización | (II) Estructura rígida + densidad flexible |

Refinamiento adicional: los títulos del Set B inicial los ajustó — "Lectura del Mercado" → **"Movimientos del Sector"** (temporal — re-evaluar tras 2-3 pilotos). Final:
1. Diagnóstico Operacional
2. Movimientos del Sector
3. Frentes de Oportunidad
4. Próximos Pasos

### Reglas de lenguaje destiladas de la conversación

Tres guardrails que salieron del transcript JP + brainstorm:
- **Decir QUÉ se puede hacer, no QUÉ comprar** — describir capacidades en lenguaje de operación, no de tecnología
- **Bajar la frecuencia de "AI"** — solo cuando aporta valor concreto al insight
- **Evitar "bot"/"agente"** (especialmente Trixx) — la gente lo asocia con robots físicos
- **Vocabulario JP locked**: NO "menor impacto" → SÍ "menores disrupciones" + "mayor productividad"; el equipo se vuelve MÁS productivo, NO se reemplaza

### Transcripción JP call (paralelo durante el brainstorm)

Mientras corría la Q&A, lancé un proceso paralelo para transcribir + resumir la llamada Ricardo↔JP de esta mañana. Primer intento bloqueado (sandbox de sub-agente sin write); segundo intento desde main thread con `~/bin/summarize-meeting.sh` falló por prompt interactivo sin scope arg; tercer intento con `--scope nexostrat --topic skill6-redesign` + stdin vacío funcionó. Output en `/srv/meetings/nexostrat/2026-05-27/2026-05-27_06-58_skill6-redesign/` (transcript + Gemini summary).

Insights del summary que cambiaron el rumbo del brainstorm mid-flight:
1. **JP está construyendo 3 skills**: `Nexus Thread PPT Expert`, `Editorial Designer`, y un skill HTML interactivo (Editorial Designer ya entregado hoy en .skill)
2. **Pricing concreto**: $1,500 USD setup + suscripción mensual mantenimiento (bot WhatsApp ejemplo) — punto de calibración para "rango cualitativo de inversión" en Sección 4
3. **Iteración Andrea → reunión formal**: vos planeás escribirle a Andrea para feedback temprano; resuelto como "runs independientes" en Skill 6 (no soporte nativo v1→v2)
4. **Visita LA**: posiblemente este jueves 2026-05-28

### Instalaciones aplicadas

3 skills nuevos en `/srv/Nexostrat/skills/` + symlinks en `.claude/skills/`:
- **`nexostrat-editorial-designer`** — del `.skill` zip que JP envió hoy; 13 KB SKILL.md + 18 logos PNG + 3 reference docs (brand-identity, cover-designs, design-specs)
- **`pptx`** técnico — del repo `github.com/anthropics/skills/skills/pptx`
- **`docx`** técnico — del repo `github.com/anthropics/skills/skills/docx`

Nota de licencia: los technical pptx + docx son **source-available, NOT open source**. Uso dentro de Claude Code (Anthropic Service) calza dentro del envelope, pero a largo plazo conviene migrar a wrappers propios sobre python-pptx + python-docx si Nexostrat opera fuera de CC.

### Spec escrito

`00_META/proposals/2026-05-27_skill6-pipeline-redesign.md` — 17 secciones, ~580 líneas. Cubre: executive summary, contexto+motivación, pipeline overview, decisiones locked, Skill 5 reprofile, bridge artifact (template completo + conversational flow), Skill 6 spec (folder + inputs + outputs + Word section-by-section + PPTX slide-by-slide + reglas visuales), Skill 7 placeholder, multi-engine transcription canon, renames + folder restructure, inventory of skills, HTML internal deck spec, brain-side verification (luego confirmado out of scope), implementation order Fases A-H, open items, decisions log.

Self-review pasó con 2 fixes inline:
- Sec 13 (Brain-side verification): de "Impacto esperado" → "A verificar" (honestidad sobre que no leí los plans a fondo en ese momento)
- Sec 12 (HTML deck path): committed path explícito

### HTML deck construido

`operations/internal/2026-05-27_nexostrat-pipeline-deck.html` — 851 líneas, 50 KB. Single-page con:
- Top sticky bar + indicador de sección actual
- Hero con SVG diagrama vectorizado del whiteboard JP (5 stages, nodos clickables, tooltips on hover)
- 9 secciones colapsadas con `<details>` (Visión / Etapa 1 / Reunión / Etapa 2 / Si aprueba / Inventario / Decisiones / Outputs / Cómo arranco)
- Aurora palette dark + Inter + Caveat para anotaciones manuscritas
- Color coding por nodo: azul=skill, naranja=cliente, amber=review, verde=cierre, rojo=loop
- Click en nodo del diagrama → expande la sección correspondiente abajo + scroll

Ricardo lo abrirá + enviará a JP para feedback. Iteración visual pendiente según response (P1=ii prometía "Caveat dentro de boxes + wobbly borders" que implementé parcialmente — Caveat solo en anotaciones, no en box labels).

### Verificación brain-side (terminal step)

A pedido de Ricardo, verifiqué los 3 plans brain-side que él flageó:
- `2026-05-25_meetings-pipeline-overhaul-master-plan.md`
- `2026-05-25_meetings-pipeline-overhaul-deployment.md`
- `2026-05-22_brain_bot_platform_implementation.md`

**Resultado: cero cambios necesarios.** Los plans operan a un nivel arquitectónico más alto (transcripción → task auto-extracción → calibración 0.85 → tenant routing) y no bajan al nivel de skill names o folder paths que cambiamos. Grep para `opportunity-report` / `reporte_oportunidades` / `Skill 5/6/7` / `client-deliverables` / `internal-report` / `brief_cliente` / `entregables` / `reporte_interno` → **0 hits en los 3 plans**.

Solapamiento de nombre (no bloqueante): el bot platform Phase 6 usa `/brief` para meeting-pre-reminders; el redesign usa `brief_cliente` para post-meeting curation. No es colisión técnica, pero conversacionalmente conviene siempre decir "brief_cliente" o "client-brief" cuando se refiere al del Skill 6.

## Decisiones locked esta sesión

1. **Lente (b) standalone valor**, no sales-asset puro
2. **Estructura espejo (b2)** — 4 secciones con primera mitad puro cliente
3. **Word + PPTX paralelos (ii)** — mismo brief, distintas autorías
4. **brief_cliente.md** versionado como artefacto-puente; Claude conduce la conversación con preguntas estructuradas
5. **Solo .docx + .pptx output** — HTML descartado del flujo automático
6. **Estandarización (II)** rígida en estructura, flexible en densidad
7. **Set títulos B refinado** con "Movimientos del Sector" temporal
8. **Vocabulario JP locked** — productividad/disrupciones/equipo-más-productivo
9. **Iteración runs independientes**, no v1→v2 nativa
10. **Skill 7 nombre comercial cliente-facing**: "Plan Detallado de Implementación", no "Hoja de Ruta de IA"
11. **Brain-side verification = workstream separado**, no parte del redesign
12. **3 skills nuevos instalados**: editorial-designer + pptx + docx técnicos
13. **License source-available Anthropic** — uso intra-Claude-Code OK; revisar largo plazo
14. **Trixx como test-skeleton** para Skill 6, no re-run forzoso

## Open items que quedan en cola

- Feedback de JP sobre spec + deck (bloqueante para arrancar implementación)
- Implementation plan vía `superpowers:writing-plans` (post-aprobación)
- Skill 6 build (Fases A-H del spec)
- Skill 5 rename + reprofile (Fase B)
- Skill 7 placeholder (Fase D)
- Folder rename `reporte_oportunidades` → `reporte_interno` (Fase B step 6)
- HTML deck iteration según feedback JP
- Crear `00_META/protocols/meeting_transcription.md` (no bloqueado)
- Fix descripción editorial-designer (Century Gothic → Inter; LATAM) (no bloqueado)
- Documentar Anthropic license note en `00_GOVERNANCE/decisions/` (no bloqueado)

## Notas técnicas / lessons learned

1. **`~/bin/summarize-meeting.sh` requiere flags explícitas + stdin vacío para correr sin TTY**: `--scope nexostrat --topic <topic>` + `</dev/null` evita los 2 prompts interactivos (scope + client-slug). Documentar en cheatsheet.
2. **Sub-agentes en sandbox no pueden escribir**: el primer intento de transcripción vía sub-agente falló porque el harness le dio sandbox solo-lectura. Main thread escribe fine; sub-agentes para tareas con writes requieren flag explícita o se delegan a Bash background del main.
3. **El `.skill` de JP** es un zip vanilla. Extraer a `skills/<slug>/`, symlinkear a `.claude/skills/<slug>`, archivar el zip en `skills/00_META/skill_packages/` por si JP envía updates.
4. **El `nexostrat-pptx-expert` y `nexostrat-editorial-designer`** son design-strategy skills que dependen de skills técnicos (`pptx` y `docx`) para ejecución real. Sin los técnicos, los strategy skills no pueden generar archivos. Ahora ambos par están instalados.

## Próxima sesión

**Trigger esperado**: Ricardo abre con feedback de JP sobre el spec + deck. Acciones probables según response:

- (A) JP aprueba sin cambios → invocar `superpowers:writing-plans` con el spec como input para detallar Fases A-H del implementation plan
- (B) JP pide cambios menores en deck → iterar HTML deck (whiteboard vibe más fuerte, contenido específico que falte)
- (C) JP propone cambios estructurales al spec → re-abrir brainstorm en los puntos específicos, actualizar spec, re-confirmar

Si JP demora, hay tareas no-bloqueadas que se pueden adelantar en paralelo:
- Crear `00_META/protocols/meeting_transcription.md` (codificar stack multi-engine)
- Fix descripción `nexostrat-editorial-designer` (Inter only + LATAM)
- Documentar Anthropic source-available license en `00_GOVERNANCE/decisions/`

---

**Commit referenciado**: ver `git log` para hash del commit de esta sesión.
