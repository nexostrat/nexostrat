# Sesión 26 — 2026-05-28 (mid-day, ricardo-desktop, ~4h wall-time)

**Topic:** Pipeline v2 update completo + organización raíz + F2/F3 renames + 3 protocolos próximas sesiones + Phase 5 calendar cache smoke-test con symlink canónico fix.
**Persona:** Founder (root).
**Host:** ricardo-desktop.

## Contexto de apertura

Sesión 25 (morning del mismo 2026-05-28) ya había cerrado el commit del meeting-summary PDF template y reconciliado la divergencia GitHub. Esta sesión abrió ~3 horas después con el meeting JP-Ricardo 07:05 (sobre buyer-persona-Trixx-pipeline) ya transcrito y resumido por el meetings pipeline. El CHECKPOINT predecía el flujo (A) "JP respondió las 14 por escrito o las cerramos en la reunión" → escribir spec v2 oficial + abrir tasks técnicos. Eso es exactamente lo que pasó, con scope expandido por Ricardo a lo largo de la sesión.

## Lo que se hizo

### 1. Raíz organizada (5 archivos)

Ricardo pidió primero organizar la carpeta principal. Encontrados 5 archivos fuera de lugar:

| Antes (raíz) | Después | Tipo |
|---|---|---|
| `Cerrar_a_Don_Carlos.mp4` (34.7 MB) | `operations/marketing/buyer_personas/Cerrar_a_Don_Carlos.mp4` | gitignored (heavy, regla agregada a `operations/marketing/.gitignore`) |
| `Nexostrat_BuyerPersona_DonCarlos_Formulario - JP.docx` | `operations/marketing/buyer_personas/Nexostrat_BuyerPersona_DonCarlos_JP_2026-05-28.docx` | trackeado |
| `Nexostrat_Analisis_Pipeline.html` (tracked, 51 KB sesión 17) | `00_META/proposals/2026-05-20_nexostrat-analisis-pipeline.html` | git mv (historia preservada) |
| `photo_2026-05-27_09-19-53.jpg` (tracked, 147 KB whiteboard JP) | `00_META/proposals/2026-05-27_whiteboard-jp-pipeline-v2.jpg` | git mv |
| `May 27 at 06-27.m4a` (en pipeline/clients) | `pipeline/.../transcripciones/2026-05-27_ricardo-notes/audio/2026-05-27_06-27_ricardo-notas-reporte.m4a` | sigue patrón existente |

`AskUserQuestion` se usó solo para el .mp4 (¿dónde va? + ¿qué es?) y el .m4a (¿transcribir? ¿de qué reunión?). El resto tenía destino canónico claro.

### 2. 6 symlinks rotos reparados

Ricardo flagged que `etapa_2_diagnostico/reporte_oportunidades/runs/2026-05-26_mode-a/` tenía "muchos archivos que no puedo abrir, link is broken". Investigación: los 6 symlinks habían sido creados con paths en inglés (`01_company_analysis`, etc.) pero las carpetas reales están en español (`01_analisis_compania`, etc.), y además tenían un nivel `../` faltante (apuntaban con `../../../` cuando debían ser `../../../../` para subir hasta `trixx-logistics/` y bajar a `etapa_1_preparacion/`). Reparados los 6 con `ln -sf` apuntando a los targets correctos:

- `LogisticaCrossBorder_MX_20260526.md` → `../../../../etapa_1_preparacion/02_analisis_industria/runs/2026-05-26_mode-a/...`
- `Trixx_AnalisisCompania_20260526.md` → `../../../../etapa_1_preparacion/01_analisis_compania/runs/2026-05-26_mode-a/final_report.md`
- `Trixx_Competencia_MX_20260526.md` → análogamente
- `Trixx_PrepLlamada_20260526.md` → análogamente
- `Trixx_TranscriptFinal_1010_20260526.md` → `../../../transcripciones/2026-05-26_formal-meeting/1010_main-meeting_transcript_final.md`
- `Trixx_TranscriptFinal_1205_20260526.md` → análogamente

### 3. Audio Ricardo transcrito

El audio de 5:40 min (`2026-05-27_06-27_ricardo-notas-reporte.m4a`, 2 MB, single speaker) se procesó con `transcribe-x.sh` (WhisperX large-v3, NO_DIARIZE=1, hotwords Trixx). Outputs movidos a `transcripciones/2026-05-27_ricardo-notes/whisperx/` siguiendo el patrón canónico. Creado README + `notas_curadas.md` con síntesis estructurada de los 6 ejes que cubre Ricardo en la grabación:

1. Filosofía: soluciones inmediatas primero (Héctor pidió entender complejidad antes de cambios grandes), mantener flujo existente.
2. Riesgo central: con 2 camiones nuevos + crecimiento, no podrán decidir rápido sin info a la mano.
3. Restricciones equipo Héctor: no quieren aprender procesos nuevos (les costó en Guadalajara), fricción de información.
4. Acciones concretas: reunión específica con María Helena, decidir UNA plataforma (Google Workspace vs Office), resolver proveedor IT externo, averiguar CRM actual.
5. Quick Wins propuestos por Ricardo: QW1 = bot/asistente WhatsApp en celular María Helena, QW2 = Workspace/OneDrive con Excel multi-usuario.
6. Estrategia general: empezar fácil, mostrar grandes como futuro, "información por un solo punto".

### 4. Análisis reunión JP 07:05

Meeting 2026-05-28 07:05 (49 min) sobre buyer-persona-Trixx-pipeline ya estaba procesado por la pipeline (`/srv/meetings/nexostrat/2026-05-28/2026-05-28_07-05_buyer-persona-trixx-logistic-pipeline/`). Leyendo `summary.md` + metadata, mapeé contra las 14 preguntas abiertas del doc `2026-05-27_preguntas-jp-pipeline-v2.md`:

**Cerradas (4):**
- (2) Estructura del Word: DOCX/HTML 10-15 páginas + PPTX 10 slides máximo.
- (3) Cifras concretas: baseline $3,000 USD por proyecto, sin cobro por horas.
- (6) Garantía 1 mes alcance: solo bugs + ajustes menores; features nuevos = proyecto aparte.
- (7) Garantía 1 mes precio: incluida en el precio estándar.

**Parcial (1):**
- (1) CRM herramienta: Notion (JP) vs Odoo (Ricardo) — Ricardo investiga Odoo.

**Abiertas (9):**
- (4) catálogo capacidades, (5) Ciclo 2 fases, (8) canales captación, (9) funnel etapas, (10)-(12) seguimiento (plantillas/canal/cut-off), (13) JP en flujo (modificado por modelo Neo), (14) "Cowork" nombre comercial.

**Decisiones nuevas que no estaban en las 14 preguntas (5):**
- Posicionamiento: evitar "bot"/"robot"/"agente"; usar "sistemas de consolidación de información" o "secretarios digitales".
- Modelo tercerización con Neo para proyectos fuera del alcance ágil.
- Facturación internacional USD vía empresa JP en Panamá (Consultores Butacos).
- Estrategia marketing contenido: grabar reuniones → IA → newsletter + LinkedIn + Twitter.
- Handles redes sociales: reservar `nexostrat_` en Instagram, Twitter, TikTok.
- Buyer Persona Don Carlos consolidado por JP (merge IA Ricardo + JP + video `Cerrar_a_Don_Carlos.mp4`).

### 5. Doc preguntas actualizado

`00_META/proposals/2026-05-27_preguntas-jp-pipeline-v2.md` editado para agregar bloque "Resultado de la reunión 2026-05-28" arriba con tabla de estado + decisiones nuevas + tasks abiertas, sin modificar el cuerpo original.

### 6. Spec v2 oficial — F1 conceptual

`00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` (~150 líneas) supersedes spec v1 en los puntos donde hubo refinamiento JP. Estructura:

- §1 Resumen ejecutivo
- §2 Decisiones locked (5 de sesión 24 + 5 nuevas de reunión 2026-05-28 + 5 que no estaban en preguntas)
- §3 Lo que sigue abierto (9 puntos)
- §4 Implicaciones constructivas para Skill 6 (DOCX/PPTX templates, lenguaje, sección Propuesta template)
- §5 Roadmap F1-F8 con bloqueantes
- §6 Cross-references operativos
- §7 Próximo paso

### 7. F2 ejecutado — rename del Skill 05

Rename mecánico de `skills/05_opportunity_report/` a `skills/05_internal_report/`. Acciones:

- `git mv skills/05_opportunity_report skills/05_internal_report` (historia preservada)
- Symlink `.claude/skills/opportunity-report` reemplazado por `.claude/skills/internal-report`
- Frontmatter slug `opportunity-report` → `internal-report` + description reescrita para audiencia interna + trigger phrases nuevas
- Body del prompt NO se reescribe — sigue v1 ("directo al cliente"); nota REPROFILE PENDIENTE al inicio del file + nueva task `t-skill5-reprofile-body` (medium, due 2026-06-15)
- `infra/scripts/test_skills.sh` registry actualizado: `05_internal_report:internal-report`
- `skills/README.md` + `skills/CLAUDE.md` + CHANGELOG v0.4 entry
- Test harness: 63 PASS · 0 SKIP · 0 FAIL post-rename

Tasks cerradas como efecto: `t-skill5-rename-and-reprofile` (sesión 21 placeholder de este mismo trabajo).

### 8. F3 ejecutado — rename folder clientes

Rename de `reporte_oportunidades/` a `reporte_interno/`:

- `git mv pipeline/clients/_template/etapa_2_diagnostico/reporte_oportunidades reporte_interno`
- `git mv pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_oportunidades reporte_interno`
- 6 symlinks dentro de Trixx runs verificados resueltos post-rename (paths relativos `../../../../` no cambian profundidad)
- Sed sweep en 8 archivos con referencias path-level + slug: `_template/README.md`, `new-client.sh`, Trixx state.json, checkpoint.md, our_hypotheses.md, Trixx_NotasCliente_20260526.md, 2 READMEs transcripciones

Carpetas `brief_cliente/` y `entregables/` del spec v1 NO se crearon porque el spec v2 las eliminó (decisión sesión 24 #5: revisión libre sin template intermedio).

Tasks cerradas como efecto: `t-clients-folder-rename`, `t-008` (Buyer Persona consolidation; JP lo hizo + video), `t-skill6-jp-feedback-await` (JP dio feedback en la reunión).

### 9. 3 protocolos para próximas sesiones

Nuevo directorio `00_META/protocols/` con README + 3 protocolos:

- `sesion-S1-catalogo-capacidades.md` (F4 del roadmap, requiere JP, 1-2h)
- `sesion-S2-investigacion-odoo.md` (F6, Ricardo solo, 1-2h)
- `sesion-S3-reporte-oportunidad-trixx.md` (Trixx iteration, Ricardo solo, 1.5-2.5h, insumos preparados)

Cada protocolo incluye: contexto necesario, procedimientos paso por paso, outputs esperados, criterios de éxito, manejo de bloqueos, tareas relacionadas, memorias relevantes, + bloque "EJECUTADO" para llenar al cierre.

### 10. Git sync — integrado commit nuevo del remote

`git fetch --all` mostró que los 3 remotes habían avanzado de `db39049` a `ca4cea0` durante la sesión (1 commit nuevo `ca4cea0` "templates: Phase 5 T-2h pre-meeting brief template" pushed desde otro proceso — touched solo `00_META/templates/pre_meeting_brief_t2h.md`, 14 líneas). Mi local estaba en `ff3cfec` (1 commit detrás).

Sync flow: `git stash push -u -m session-26-wip` → `git pull --rebase origin main` (fast-forward limpio) → `git stash pop`. Sin conflictos.

### 11. Phase 5 calendar cache refresh smoke-test + canonical path fix

Ricardo pidió smoke-test del Phase 5 calendar cache refresh path. Ejecutado end-to-end (Steps 1-8):

- **Step 1:** Google Calendar MCP auth verificado (`list_calendars` retornó 2 calendarios: primary + Spain Holidays).
- **Step 2:** Smoke-test inicial con 7d primary devolvió 2 events Nexostrat. Después Ricardo eligió scope canónico (30d + ambos calendarios) → 10 upstream / 8 kept (8 recurrencias "Nexostrat" Mon/Thu + 2 holidays filtrados correctamente).
- **Step 3:** Filter aplicado importando desde canonical `/srv/brain-hub/hub/google/calendar_filter_nexostrat.py`. Todos los matches via `summary_contains_nexo`.
- **Path issue descubierto:** `/srv/brain-hub` no existía en este host (el módulo real está en `/home/ricardo/brain-hub/`). Solución: crear symlink `/srv/brain-hub` → `/home/ricardo/brain-hub` (sigue precedente `/srv/brain` → `/home/ricardo/brain`). Sin sudo (`/srv/` es `ricardo:ricardo`-owned).
- **Docs fix:** `COMMANDS.md` línea 151 actualizada de `/home/ricardo/brain-hub` → `/srv/brain-hub` + nota explicando: en server (ricardo-hp-laptop) es real install; en desktop (ricardo-desktop) es symlink. `docs/runbooks/new-workstation.md` Step 11 sub-sección nueva con el comando para crear el symlink en hosts desktop futuros.
- **Cache write atómico:** `tempfile.mkstemp` + `os.replace` para single-shot replacement (no torn writes).
- **2 commits separados pushed:**
  - `d17912c` docs: canonical /srv/brain-hub path + desktop symlink convention (COMMANDS.md +1/-1; new-workstation.md +15)
  - `0f2a76f` calendar: refresh cache (filter=nexostrat-v1, 8 events) (+50/-64 en calendar_cache.json)
- **Pushed a los 3 remotes** (origin gitea + github directo + codeberg vía path-watcher). Los 4 HEADs convergen en `0f2a76f`.

Nota disciplina: el push directo a github funcionó sin "cannot lock ref" porque llegó antes que el path-watcher de origin propagara. La regla locked sesión 25 (never push directo a mirrors) sigue siendo lo correcto a futuro; lo de esta vez está bien porque Ricardo lo pidió explícitamente como sanity check. La task `t-pre-push-hook-block-mirrors` sigue abierta como el fix mecánico pendiente.

## Decisiones locked esta sesión

1. **Canonical path Phase 5 filter = `/srv/brain-hub`.** En desktop = symlink; en server = real install. Future sessions importan desde el path canónico.
2. **Spec v2 oficial existe** y es la fuente de verdad para Pipeline v2 (supersedes v1 en los puntos refinados).
3. **5 decisiones nuevas del meeting JP locked** (posicionamiento + Neo + Panamá + marketing + redes).
4. **Skill 05 = audiencia interna** (no cliente). Rename mecánico hecho; reprofile body pendiente.
5. **`brief_cliente/` y `entregables/` no se crean** en el client template (decisión sesión 24 #5 confirmada en spec v2).
6. **Protocolos para sesiones dedicadas** como mecanismo de coordinación de scope cuando una sesión tiene meta clara + insumos preparados.

## Tasks closed esta sesión

- `t-008` (Buyer Persona consolidation)
- `t-skill6-jp-feedback-await` (feedback JP en meeting)
- `t-skill5-rename-and-reprofile` (rename hecho; body reprofile como task aparte)
- `t-clients-folder-rename` (renames hechos)

## Tasks nuevas esta sesión

- `t-skill5-reprofile-body` (medium, 2026-06-15) — reescribir body del SKILL.md a audiencia interna
- `t-trixx-reporte-iteracion-notas-ricardo` (high, 2026-05-30) — iteración Reporte Oportunidades con notas Ricardo + insumos preparados

Plus 6 tasks auto-extraídas del meeting JP (t-010..t-015) que ya estaban en tasks.json desde el `git pull` del inicio de sesión.

## Commits pushed esta sesión

- `d17912c` docs: canonical /srv/brain-hub path + desktop symlink convention
- `0f2a76f` calendar: refresh cache (filter=nexostrat-v1, 8 events)
- (pendiente al momento de escribir este journal) commit final de cierre con todo el resto del trabajo de sesión 26.

## Lo que NO se tocó (preservado)

- Memorias persistentes en `~/.claude/projects/-srv-Nexostrat/memory/` (sin cambios).
- Specs v1 (`2026-05-27_skill6-pipeline-redesign.md`) preservado como histórico; spec v2 lo supersedes pero no lo borra.
- Body del SKILL.md de internal-report (queda con tono cliente; reprofile separado en task).
- Audio Trixx 2026-05-26 formal meeting (ya procesado sesión 20, sin cambios).
- Pilotos folder (3 test companies Bodai/Ascenso/Scarab; migración a pipeline/clients/ sigue task abierta separada).

## Hand-off implícito para sesión 27+

La próxima sesión arranca con 3 protocolos listos:
- S1 (catálogo capacidades, requiere JP)
- S2 (Odoo investigation)
- S3 (iteración Reporte Oportunidades Trixx — insumos preparados)

Cualquiera de las 3 se puede invocar con `Start session siguiendo el protocolo 00_META/protocols/sesion-S<N>-<topic>.md`. El CHECKPOINT.md le da contexto adicional si Ricardo abre con tema distinto.
