# Protocolo S1 — Catálogo de Capacidades Nexostrat

**Fase del roadmap:** F4 del spec v2 (`00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md`)
**Task tracker:** `t-nexostrat-capabilities-catalog` (tasks.json, high, due 2026-05-31)
**Estado:** DRAFT
**Prerequisitos:** JP disponible (sincrónico en reunión o asíncrono vía Telegram con turnaround <24h)
**Tiempo estimado:** 1-2 h sesión

---

## Objetivo

Construir el **catálogo de capacidades reales de Nexostrat**: un documento de 1 página (markdown + PDF) que enumera qué servicios podemos entregar HOY, a qué precio fijo, en qué tiempo, con qué stack técnico, y qué quedaría explícitamente fuera del alcance ("cannot deliver today").

Este catálogo es input para:
- Sección "Propuesta" del entregable Skill 6 (precios concretos vs vapor)
- Conversación con prospects: si preguntan "¿pueden hacer X?", contestamos con dato firme
- Decisión Neo: cuando un cliente pide algo fuera del catálogo, sabemos derivarlo

## Por qué necesita JP

JP es co-fundador y owner del lado de "qué se entrega". Sin su input las capacidades quedan especulativas. Ricardo conoce capacidad técnica; JP conoce realismo comercial + tiempos de entrega + precios que cierran.

## Contexto necesario al inicio de sesión

Leer en este orden:
1. `CHECKPOINT.md` (baton estándar)
2. `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` (decisiones $3K USD baseline + lenguaje "sistemas de consolidación" + modelo Neo)
3. `00_META/proposals/2026-05-27_preguntas-jp-pipeline-v2.md` § "Resultado de la reunión 2026-05-28" (refrescar respuestas JP)
4. `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-26_mode-a/Trixx_ReporteOportunidades_20260526.md` (las 10 oportunidades identificadas — primera aproximación de qué tipo de cosas surgen en pilotos reales)

## Procedimientos paso por paso

### Paso 1 — Decidir formato de la sesión

Preguntar al inicio: **¿es esta sesión con JP en vivo (Ricardo + JP en call con Claude transcribiendo) o asíncrona (Ricardo dirige, intercambios con JP por Telegram)?**

- **Sincrónica:** Claude facilita un Q&A estructurado (12-15 preguntas) que Ricardo + JP responden en chat. Claude consolida en el documento final al cierre.
- **Asíncrona:** Claude redacta un cuestionario para enviar a JP, espera respuestas, integra cuando lleguen.

### Paso 2 — Inventario inicial de capacidades candidatas

Listar como hipótesis (basado en lo que ya hicimos sobre Trixx + pilotos):

1. **Asistente WhatsApp** (recibe info + organiza en documento) — TRIXX QW1
2. **Centralización Google Workspace / OneDrive** con archivo Excel consolidado — TRIXX QW2
3. **Bot de filtrado de correos con IA** — propuesto en pilotos
4. **CRM ligero / dashboard de prospects** (post-decisión Odoo vs Notion)
5. **Automatización Excel → PDF / formatos regulatorios** (CBP, Carta Porte) — TRIXX pain point #1
6. **Pipeline de transcripción de reuniones + acciones extraídas** (lo que usamos internamente)
7. **Configurador de productos con IA** (intentado en Scarab piloto — flag: declarado fuera del alcance ágil)
8. **Plataforma a la medida desde cero** (declarado fuera, deriva a Neo)

Por cada candidato, llenar la matriz:

| Capacidad | ¿Entregamos hoy? | Stack | Tiempo estimado | Precio baseline | Notas |
|---|---|---|---|---|---|
| ... | Sí / Con Neo / No | ... | 2-3 semanas / 4-6 semanas / etc | $3K / $5K / $X / TBD | ... |

### Paso 3 — Para cada capacidad pendiente de respuesta de JP

Si JP no está disponible para confirmar, dejar la fila con `TBD-JP` en el campo de precio + tiempo. NO inventar. Memoria honestidad: las propuestas con cifras inventadas matan credibilidad downstream.

### Paso 4 — Definir explícitamente lo que NO entregamos

Sección dedicada: "Lo que no hacemos en Nexostrat (deriva a aliado)". Lista corta:
- Desarrollo de plataformas a la medida desde cero → Neo
- Aplicaciones móviles nativas → externo
- Diseño UX puro (sin componente IA) → externo
- Marketing performance / SEO operativo → externo

Esto es tan importante como lo que sí entregamos: evita decir "sí" a algo que no podemos hacer bien.

### Paso 5 — Validación de coherencia con $3K USD baseline

Para cada capacidad confirmada, validar:
- ¿El precio fijo cubre la entrega + 1 mes garantía?
- ¿El tiempo es realista incluyendo entendimiento + diseño + validación + construcción + pruebas (no solo "coding time")?
- ¿La capacidad se puede entregar SIN reasignar tiempo de las otras?

Si alguna capacidad rompe estas validaciones, marcar como "REVISAR con JP".

### Paso 6 — Generar entregables

- **Markdown:** `operations/internal/<YYYY-MM-DD>_nexostrat-capabilities-catalog.md`
- **PDF:** convertir vía pandoc + weasyprint usando `00_META/templates/meeting-summary-prompt.md` recipe o adaptar.
- **Una sola página A4** (forzar concisión).

## Outputs esperados al cierre

1. `operations/internal/<YYYY-MM-DD>_nexostrat-capabilities-catalog.md` — el catálogo (1 página)
2. `operations/internal/<YYYY-MM-DD>_nexostrat-capabilities-catalog.pdf` — versión imprimible
3. `tasks.json` — `t-nexostrat-capabilities-catalog` cerrado
4. `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` — actualizar §3 "Lo que sigue abierto" cerrando pregunta (4)
5. Journal entry estándar
6. Update `CHECKPOINT.md` + `STATUS.md`

## Criterios de éxito

- Catálogo cabe en 1 página A4
- Cada capacidad tiene precio FIJO (no rango) y tiempo CONCRETO (no "depende")
- Sección "lo que NO hacemos" presente y explícita
- JP firmó / confirmó cada fila o quedó marcada como `TBD-JP`
- El catálogo es referenciable directamente desde la sección Propuesta del Skill 6

## Manejo de bloqueos

- **JP no contesta:** dejar versión DRAFT con `TBD-JP` en filas pendientes, programar siguiente touchpoint. NO completar inventando.
- **Surge una capacidad nueva durante la sesión:** evaluar contra los 3 criterios del Paso 5; si no pasa, sale de la versión inicial y queda como "candidata para v2 del catálogo".
- **El catálogo no cabe en 1 página:** consolidar capacidades similares (ej. "centralización de información" como umbrella en lugar de 3 filas separadas para Workspace + OneDrive + Excel).

## Tareas relacionadas a cerrar/actualizar

- `t-nexostrat-capabilities-catalog` — cerrar al final
- `t-build-skill-wrappers` — referenciar el catálogo como insumo para Skill 6

## Memorias relevantes

- `feedback_honestidad_brutal_evaluacion` — no inventar capacidades para llenar el catálogo.
- `feedback_outputs_premium_visual` — el PDF de 1 página debe verse consulting-grade.
- `feedback_no_emojis_no_symbols` — cero decoración en el catálogo.
- `project_ricardo_ceo` — Ricardo CEO + cara pública; JP rol técnico/comercial todavía sin título locked.

---

**Al cerrar la sesión, actualizar este protocolo agregando un bloque al inicio:**

```
## EJECUTADO — YYYY-MM-DD
- Journal: 00_META/journal/YYYY-MM-DD_<topic>.md
- Output: operations/internal/...
- Status: completo / parcial / blocked
- Next: ...
```
