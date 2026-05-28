# Session 24 — Pipeline v2 JP Review: Diff + 5 Decisiones + 14 Preguntas para JP

**Date:** 2026-05-27 (late night, fourth wall-clock session on this date)
**Operator:** Ricardo
**Persona:** Founder
**Duration:** ~1h wall-time
**Outcome:** Diff conceptual entregado + 5 decisiones cerradas en chat + doc de 14 preguntas para JP en .md + .docx

## Lo que pasó

Sesión 24 abrió con un prompt autocontenido de Ricardo dejado al cierre de la sesión 23. La tarea: ingerir `pipeline-nexostrat-v2.html` (revisión visual de JP del pipeline brainstormeado en sesión 21), producir un diff conceptual contra el spec aprobado, y proponer cómo incorporar los cambios — sin tocar código de skills hasta confirmación.

Leí los 3 archivos pedidos en paralelo (spec original `2026-05-27_skill6-pipeline-redesign.md` + journal del brainstorm `2026-05-27_skill6-pipeline-redesign-brainstorm.md` + el HTML v2 de JP) más los archivos de session-start del protocolo (CHECKPOINT, STATUS, tasks, calendar).

### El diff conceptual

El v2 de JP mantiene la columna vertebral del spec (Skills 01-03 en cadena, Skill 04 interno, Skill 05 raw no-cliente, Skill 06 entregables cliente, revisión humana entre pasos) pero reabre tres decisiones y agrega dos workstreams nuevos:

**Cambios materiales que afectan implementación:**
1. Output Skill 6: de .docx 5pp + .pptx 10 slides a PDF completo + .pptx 10 slides
2. Skill 7 desaparece como entidad separada; hoja de ruta + propuesta viven dentro del PDF Skill 6 (gratis, pre-cierre)
3. Ciclo 2 (implementación) modelado en 6 sub-fases: Diseño → Construcción → Pruebas → Ajustes → Implementación final → Mantenimiento garantía 1 mes
4. Fase 1 nueva: Captación multi-canal + CRM automatizado por IA (no modelada en v1)
5. Seguimiento post no-cierre: D+7 manual Ricardo + D+15/30/60/90 automatizados con IA personalizado por etapa
6. brief_cliente.md no aparece — step 8 dice "revisión iterativa Ricardo+IA hasta documento final"

**Items ambiguos del v2:** brief_cliente.md (omisión por nivel de detalle vs rechazo consciente), CRM herramienta (no especificada), estructura del PDF (4 secciones espejo del v1 vs estructura nueva), garantía 1 mes (alcance + inclusión en precio), pricing concreto vs cualitativo.

### Las 5 decisiones que cerramos caminando pregunta por pregunta

Ricardo eligió ir bloque por bloque del documento de preguntas. En cada uno expliqué el spec v1, lo que dice el v2 de JP, por qué tenía que preguntar y qué cambia según la respuesta. Tres bloques completaron decisión locked:

1. **Output Skill 6 = `.docx` editable + `.pptx`** (no PDF como propuso JP). Ricardo overrules a JP en formato porque quiere editabilidad — el PDF queda como conversión derivada si se necesita. La cáscara es Word.
2. **Estructura interna del `.docx` = versión de JP** (hoja de ruta + propuesta dentro del entregable principal, no en Skill 7 paga). La estructura específica (4 secciones espejo del v1 + sección 5 propuesta? o estructura nueva?) queda como pregunta 20 abierta para JP.
3. **Reglas de entrega = JP como default no rígido.** PPTX se proyecta en reunión, .docx se entrega al cierre, pero hay flexibilidad caso por caso. La disciplina vive en el playbook, no en el código del Skill 6.
4. **Skill 7 muere.** Se cancela `t-skill7-placeholder-spec` esta sesión. Toda la hoja de ruta + propuesta vive en el `.docx` del Skill 6. El catálogo de capacidades sube en prioridad (sin él no puede haber pricing concreto en propuesta).
5. **`brief_cliente.md` eliminado.** Adopta la "iterativa" del v2 de JP. La curaduría tonal queda implícita en el diff del `.docx` entre versión 1 y N — sin artefacto intermedio versionado.

### Las 14 preguntas que quedaron abiertas

En el bloque D (Fase 1 Captación + CRM) Ricardo dijo "vamos TODO con la versión de JP" — pero el v2 visual de JP no especifica ni la herramienta CRM, ni los canales del MVP, ni si el funnel es fijo o flexible. Me detuve y le señalé la inconsistencia: "la versión de JP" no contiene decisión técnica concreta en este bloque. Ricardo respondió: "las cosas que no están definidas déjalas como preguntas para la conversación de mañana".

Inventario completo de los 14 abiertos, agrupados:

**Bloqueantes para arrancar implementación (7):** qué CRM (Baserow/otra/manual), estructura interna del `.docx` (4 secciones espejo + 5a propuesta vs nueva), cifras concretas o rango en propuesta, catálogo de capacidades antes del primer cliente o después, 6 fases Ciclo 2 skills/humano/mezcla, alcance garantía 1 mes, garantía incluida o aparte.

**Importantes pero no bloquean Skill 6 técnico (5):** canales captación MVP, funnel CRM fijo/flexible, quién escribe plantillas D+7/15/30/60/90, canal del seguimiento, qué detiene la cadena.

**Operacionales / afinamiento (2):** JP en el flujo (opcional o algunos obligatorios), "Cowork" como nombre comercial o solo etiqueta visual.

### El documento para JP

Tras inventariar las 14 preguntas, Ricardo pidió un documento JP-friendly para mandar antes/durante la reunión de mañana. Específicamente: "documento simple, corto, fácil de leer y ENTENDER" + exportar a `.docx`.

Reescribí `00_META/proposals/2026-05-27_preguntas-jp-pipeline-v2.md` con:
- Header de "lo que ya cerramos" (5 decisiones) para que JP no las re-litigue
- 14 preguntas en lenguaje JP-friendly (sin slugs técnicos, sin paths del repo)
- Cada pregunta con un "Por qué te pregunto" de 1-2 frases + opciones marcables A/B/C/D
- Cierre con próximos pasos

Conversión a `.docx` vía pandoc (default styling — el template del nexostrat-editorial-designer en el path probado no existía y caí al default). Tamaño: 15.9 KB. Ofrecí regenerar con branding Nexostrat aplicado vía el skill nexostrat-editorial-designer o copiar al Desktop para envío, pero Ricardo cerró sesión sin elegir — se queda como está, listo en `00_META/proposals/`.

## Decisiones locked esta sesión

1. **Output Skill 6 = `.docx` editable + `.pptx`** (no PDF puro como propuso JP).
2. **Estructura del `.docx` = la versión de JP** (incluye hoja de ruta + propuesta dentro). Estructura específica de secciones queda como pregunta 20 abierta.
3. **Reglas de entrega de JP como default no rígido.** PPTX primero en reunión, `.docx` al cierre; flexible caso por caso.
4. **Skill 7 muere.** `t-skill7-placeholder-spec` cancelled. Drop `skills/07_implementation_roadmap/` del plan de implementación.
5. **`brief_cliente.md` eliminado.** Revisión libre Ricardo + IA hasta consenso, sin template estructurado.
6. **Las cosas no especificadas por JP no se asumen.** Honestidad locked: si el v2 de JP no contiene decisión técnica, va como pregunta para reunión — no se inventan respuestas para acelerar.
7. **`pipeline-nexostrat-v2.html` movido a `00_META/proposals/2026-05-27_pipeline-v2-jp.html`** para trazabilidad versionada (igual que el spec v1).

## Stack state al cierre

```
/srv/Nexostrat/
├── 00_META/
│   ├── journal/
│   │   └── 2026-05-27_pipeline-v2-jp-review-questions.md  ← NEW (this file)
│   └── proposals/
│       ├── 2026-05-27_pipeline-v2-jp.html                  ← MOVED from root (was pipeline-nexostrat-v2.html)
│       ├── 2026-05-27_preguntas-jp-pipeline-v2.md          ← NEW (14 preguntas)
│       └── 2026-05-27_preguntas-jp-pipeline-v2.docx        ← NEW (15.9 KB para enviar a JP)
├── STATUS.md                                                ← MODIFIED (session-24 entry prepended)
├── CHECKPOINT.md                                            ← MODIFIED (rewritten para sesion 25)
├── tasks.json                                               ← MODIFIED (t-skill7-placeholder-spec cancelled + t-skill6-jp-feedback-await due 2026-05-28 + updated timestamp)
└── calendar.json                                            ← MODIFIED (e-jp-pipeline-v2-meeting added for 2026-05-28)
```

Archivos que arrastrábamos sin commit de session 23 y se commitearán en este push:
- `pipeline/clients/trixx-logistics/...` — 9 archivos con correcciones "NOTA 2026-05-27" de la tesis errada de familia
- `operations/marketing/buyer_personas/Nexostrat_BuyerPersona_DonCarlos_Ricardo_2026-05-27.{md,docx}` — buyer persona Don Carlos para revisión humana

Archivo que queda untracked (no se commitea):
- `pipeline/clients/trixx-logistics/etapa_2_diagnostico/May 27 at 06-27.m4a` — heavy audio sin transcribir; no pertenece al repo

## Open items que quedan en cola

**Bloqueante crítico:**
- Reunión 2026-05-28 con JP (`e-jp-pipeline-v2-meeting`). Resolver las 14 preguntas abiertas. Sin esto no arranca Fase A del implementation plan.

**Tasks que dependen de la reunión:**
- `t-skill6-jp-feedback-await` (high, 2026-05-28) — se cierra cuando JP responda
- `t-skill6-implementation-plan` (high) — invocar `superpowers:writing-plans` con spec v2 post-reunión
- `t-skill5-rename-and-reprofile` (high) — depende de confirmar el rename y la nueva audiencia
- `t-skill6-build-skeleton` (high) — depende del template definitivo del .docx (pregunta 20)
- `t-clients-folder-rename` (high) — depende de mantener o no el rename `reporte_oportunidades` → `reporte_interno`
- `t-internal-deck-iteration-feedback` (medium) — depende si JP conserva o no el HTML deck interno
- `t-nexostrat-capabilities-catalog` (high) — sube en prioridad si la respuesta a pregunta 3 es "cifras concretas"

**No bloqueados (se pueden adelantar):**
- `t-meeting-transcription-protocol-doc` (medium, due 2026-06-10) — crear `00_META/protocols/meeting_transcription.md`
- `t-editorial-designer-fix-description` (low, due 2026-06-15) — fix Century Gothic → Inter, "PYMEs colombianas" → LATAM
- `t-anthropic-license-decision-doc` (low, due 2026-06-15) — documentar nota source-available
- `t-plan-04-description-update` (high, due 2026-05-28) — overdue mañana

## Lessons learned / observaciones

1. **Honestidad sobre lo que JP no especificó.** El reflejo natural era llenar los huecos del v2 con suposiciones razonables ("ah, JP probablemente quiere Baserow porque ya está planeado..."). Resisitir esa tentación es lo que produjo las 14 preguntas en lugar de un spec v2 inventado. La memoria `feedback_honestidad_brutal_evaluacion` aplicó directamente.

2. **El v2 de JP es operativo, no spec.** JP dibujó un diagrama de flujo con 12 pasos numerados, no escribió un spec técnico. Por diseño el HTML omite detalles de implementación (qué CRM, qué canales, etc.). Confundir "no lo dibujó" con "lo descartó" hubiera llevado a perder decisiones del spec original que JP probablemente conserva.

3. **El `.docx` para JP en 11 KB es manejable; el `.docx` con branding completo del editorial-designer toma más tiempo.** Default styling de pandoc es suficiente para un doc interno entre co-fundadores. Premium visual va para clientes (memoria `outputs_premium_visual`). Aquí Ricardo cerró sin elegir branding — defaulteamos a pandoc default.

4. **Caminar pregunta por pregunta funciona mejor que entregar tabla bulk.** Ricardo entró a esta sesión con el HTML de JP y un diff complejo de 24 puntos en su cabeza. Caminar pregunta por pregunta, explicando cada decisión, deja el reasoning grabado en el journal — útil cuando JP pregunte "¿por qué decidieron X?".

## Próxima sesión

**Trigger esperado (95%+):** Ricardo abre con resultado de la reunión con JP del 2026-05-28. Acciones probables según response:

- (A) JP respondió las 14 por escrito + cerramos las 14 en chat o reunión → escribir spec v2 oficial en `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` + invocar `superpowers:writing-plans` para Fases A-H
- (B) JP respondió algunas, dejó otras para iterar → escribir spec v2 con las cerradas + dejar TBD las abiertas + plan parcial
- (C) JP rebatió alguna de las 5 decisiones ya cerradas → re-abrir esos puntos antes de avanzar

**Si JP no respondió aún:** las 4 tasks no-bloqueadas pueden adelantarse — meeting-transcription protocol doc, editorial-designer description fix, Anthropic license note, Plan 04 description update (este último ya overdue al 2026-05-28).

> **Recomendación al próximo Claude:** abrir leyendo CHECKPOINT + STATUS + este journal + el doc de 14 preguntas (`00_META/proposals/2026-05-27_preguntas-jp-pipeline-v2.md`) + las 5 decisiones cerradas en el header de ese mismo doc. Si Ricardo abre con respuestas de JP, ejecutar el flujo de escribir spec v2. Si abre vacío, ofrecer (a) escribir spec v2 con las 5 decisiones cerradas y las 14 abiertas marcadas TBD, (b) adelantar tasks no-bloqueadas, o (c) preparar materiales de presentación para la reunión.

---

**Commit referenciado:** ver `git log` para hash del commit de esta sesión.
