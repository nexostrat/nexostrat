# Protocolo S3 — Iteración Reporte de Oportunidades Trixx

**Fase del roadmap:** F5 del spec v2 (`00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md`) — variante "iteración previa al Skill 6"
**Task tracker:** `t-trixx-reporte-iteracion-notas-ricardo` (tasks.json, high, due 2026-05-30)
**Estado:** DRAFT
**Prerequisitos:** ninguno (insumos canónicos preparados en sesión 26)
**Tiempo estimado:** 1.5-2.5 h sesión (intensiva por el nivel de detalle requerido)

---

## Objetivo

Refinar el Reporte de Oportunidades Trixx con las notas de voz de Ricardo (2026-05-27 06:27 AM, 5:40 min) + las decisiones cerradas del Pipeline v2. Producir una versión definitiva del reporte que va a alimentar el Skill 6 (entregables cliente refinados) cuando JP entregue la versión ajustada del Skill 6.

Output esperado: nueva run `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/` con `.md` + `.docx` + `.pdf` refinados.

## Por qué necesita sesión dedicada

Memoria `feedback_complete_or_nothing` + `feedback_do_it_right_do_it_once`: este refinamiento es input directo del entregable cliente. Si queda parcial, el Skill 6 recibe basura. Mejor 2 horas concentradas que 30 min compactos.

## Contexto necesario al inicio

Leer en este orden:
1. `CHECKPOINT.md` (estándar)
2. **Insumo A — Reporte actual:** `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-26_mode-a/Trixx_ReporteOportunidades_20260526.md` (245 líneas, 10 oportunidades, 2 Quick Wins seleccionados)
3. **Insumo B — Notas curadas Ricardo:** `pipeline/clients/trixx-logistics/etapa_2_diagnostico/transcripciones/2026-05-27_ricardo-notes/notas_curadas.md` (síntesis estructurada de la grabación)
4. **Insumo C — Notas crudas Ricardo:** `pipeline/clients/trixx-logistics/etapa_2_diagnostico/transcripciones/2026-05-27_ricardo-notes/whisperx/2026-05-27_06-27_ricardo-notas-reporte.txt` (transcripción raw, lectura opcional para detalle no curado)
5. **Decisiones macro:** `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` §2 (locked) y §3 (abierto) — lenguaje + estructura + precios
6. **Notas cliente curadas:** `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-26_mode-a/Trixx_NotasCliente_20260526.md` — qué dijo el cliente directamente
7. **Equipo Trixx real:** memoria `project_trixx_team_structure` — Héctor founder, María Helena mano derecha decisora real, Andrea hija de María Helena. NO esposa, NO familia.

## Procedimientos paso por paso

### Paso 1 — Crear run nueva 2026-05-28_mode-a

```bash
cp -r pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-26_mode-a pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a
```

Después de copiar, ajustar:
- Renombrar el .md: `Trixx_ReporteOportunidades_20260528.md` (sed sobre fecha)
- Eliminar los .docx y .pdf viejos (se regeneran al final)
- Symlinks heredan; verificar resuelven

### Paso 2 — Aplicar cambios concretos al .md

Los 6 cambios enumerados en `t-trixx-reporte-iteracion-notas-ricardo.notes`:

#### (a) Decidir Google Workspace vs Microsoft Office

El reporte actual mezcla los dos. Ricardo en notas curadas pide unificar. **Acción concreta:** elegir Google Workspace (alineado con: ya tienen Gmail asumido por estructura Andrea + Héctor; Workspace tiene mejor cuenta business para PyMEs; Drive es donde Trixx ya tiene archivos compartidos según menciones reunión). Justificar la elección en una nota corta. Sed sweep `Microsoft Office` → `Google Workspace`. Eliminar referencias dobles ("Workspace **u** OneDrive" → solo Workspace).

#### (b) Reordenar Quick Wins

Reporte actual tiene QW1 = "filtrado IA correos" y QW2 = "centralización Google Workspace". Ricardo en notas curadas dice:
- QW1 nuevo = **asistente WhatsApp en celular María Helena** (partner que organiza la info que ella recibe)
- QW2 nuevo = **archivo general Excel/Workspace consolidado multi-usuario**

Acción concreta:
- Mover QW1 actual (filtrado correos) a "desarrollo futuro" o "oportunidad #3"
- Crear nuevo QW1 = asistente WhatsApp (con scope + métrica de éxito + precio $3K USD baseline)
- Mover QW2 actual hacia abajo, modificar texto para reflejar "archivo consolidado" no "centralización completa Workspace"
- Renumerar tabla de Quick Wins

#### (c) Lenguaje "bot" → "asistente" / "sistema de consolidación"

Memoria `project_trixx_team_structure` recuerda que Trixx asocia "bot" con robot físico. Sed sweep:
- `bot` → `asistente` o `sistema de consolidación` según contexto
- `chatbot` → `asistente`
- `agente IA` → `asistente IA`
- `robot` → `sistema` (cuando aplique al contexto IA, no a camiones físicos)

Adicionalmente, enmarcar todo en lenguaje `menores disrupciones + mayor productividad` (vocabulario JP locked sesión 21).

#### (d) Decisora María Helena (NO Héctor)

Verificar coherencia transversal del reporte. La corrección de sesión 23 ya tocó este archivo pero a esa altura el reporte se rehizo con notas de la reunión 2026-05-26 — verificar que cada sección que menciona "decisor" / "audiencia" / "persona que aprueba" se refiere a María Helena. Cualquier residue de "Héctor decide" → corregir a "María Helena decide; Héctor valida estratégico".

#### (e) Sección nueva "Restricciones del equipo"

Ricardo en notas curadas marca esto como clave. Insertar después de la sección de Diagnóstico Operacional, antes de Frentes de Oportunidad:

> **Restricciones del equipo Trixx**
>
> El equipo actual de Trixx no está dispuesto a aprender procesos nuevos. Héctor ya advirtió que esfuerzos previos en Guadalajara y otras sedes fallaron por esta razón. Por lo tanto, toda solución que propongamos debe acomodarse a cómo trabaja el equipo HOY (WhatsApp como canal principal, manejo manual de información), no exigirles cambios de comportamiento upfront. Una vez la solución esté implementada y funcionando, los podemos llevar poco a poco hacia mejor disciplina informacional. Pero la primera versión debe ser invisible para ellos.

#### (f) Principio rector "información por un solo punto"

Insertar al inicio de la sección Frentes de Oportunidad (antes de los Quick Wins):

> **Principio transversal: información por un solo punto**
>
> Todas las soluciones propuestas comparten un eje común: la información tiene que llegar por un solo canal. Hoy WhatsApp es ese canal porque es donde el equipo ya trabaja. Las soluciones lo aceptan como punto de entrada y filtran hacia donde tiene que ir. En el mediano plazo, esto evoluciona hacia que el documento consolidado (el "archivo general") sea el segundo punto donde la información existe en forma estructurada.

### Paso 3 — Revisión final integral del .md

Lectura completa del archivo refinado, verificando:
- Tono: directo, datos-cuantificados, sin lenguaje de venta
- Anti-alucinación: tags ✅/⚠️/❓ siguen aplicados a cada dato
- Coherencia de cifras: las que estaban en el reporte 26 siguen siendo válidas (no regenerar números si no hay fuente)
- Estructura: respeta las 7 secciones de Skill 5 original

### Paso 4 — Regenerar .docx + .pdf

```bash
cd skills/05_internal_report/scripts && python3 generate_docx.py \
  --input ../../../pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/Trixx_ReporteOportunidades_20260528.md \
  --output ../../../pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/Trixx_ReporteOportunidades_20260528.docx
```

Después generar PDF:
```bash
libreoffice --headless --convert-to pdf \
  --outdir pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/ \
  pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/Trixx_ReporteOportunidades_20260528.docx
```

### Paso 5 — Copiar a Desktop Ricardo

```bash
cp pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/Trixx_ReporteOportunidades_20260528.pdf ~/Desktop/
```

### Paso 6 — Cerrar task + actualizar spec v2

- `t-trixx-reporte-iteracion-notas-ricardo` → done
- `t-014` (correr Skill 6 final Trixx) sigue OPEN — bloqueada hasta que JP entregue Skill 6 ajustado a 10-15 págs
- `00_META/proposals/2026-05-28_skill6-pipeline-redesign-v2.md` §5: marcar F5 "iteración previa" done

## Outputs esperados al cierre

1. `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/Trixx_ReporteOportunidades_20260528.md` — versión refinada
2. `.docx` + `.pdf` regenerados
3. `~/Desktop/Trixx_ReporteOportunidades_20260528.pdf` — copia para revisión visual
4. `t-trixx-reporte-iteracion-notas-ricardo` cerrada
5. Journal entry

## Criterios de éxito

- Los 6 cambios (a)-(f) aplicados explícitamente
- Cero residue de "Microsoft Office" / "bot" en el .md
- Quick Wins reordenados: WhatsApp asistente #1, Workspace consolidado #2
- Sección "Restricciones del equipo" presente
- Principio "información por un solo punto" presente
- María Helena como decisora consistente en todo el doc
- Tono "menores disrupciones + mayor productividad" detectable
- PDF cabe en formato Aurora-branded (no más de 12 págs idealmente)

## Manejo de bloqueos

- **Re-render falla:** verificar `skills/05_internal_report/scripts/generate_docx.py` no rompió con el rename del padre (test_skills.sh ya validó que funciona, pero el script puede tener paths hardcoded). Si falla, hacer .docx vía pandoc manual con plantilla Aurora.
- **Surge una contradicción entre notas Ricardo y reporte 26:** documentar la decisión y elegir la versión más reciente (Ricardo notas > reporte 26).
- **El reporte refinado queda muy largo (>20 págs):** consolidar oportunidades #3-10 en una sección "Desarrollo futuro" más sintética, sin perder los datos cuantificados clave.

## Tareas relacionadas

- `t-trixx-reporte-iteracion-notas-ricardo` — cerrar
- `t-014` (correr Skill 6 Trixx) — sigue OPEN, ahora con insumo más limpio
- `t-013` (escribir Andrea para agendar presentación reporte) — puede ejecutarse en paralelo
- `t-trixx-refresh-final-report` — REEMPLAZADO por esta sesión; cerrar como superseded

## Memorias relevantes

- `project_trixx_team_structure` — María Helena decisora; equipo no familia.
- `feedback_no_verbatim_quotes_in_copy` — reescribir en lenguaje propio, no pegar citas de notas Ricardo literales.
- `feedback_no_emojis_no_symbols` — cero decoración.
- `feedback_complete_or_nothing` — terminar los 6 cambios; no dejar parciales.
- `feedback_outputs_premium_visual` — PDF Aurora-branded consulting-grade.

---

**Al cerrar la sesión, actualizar este protocolo agregando un bloque al inicio:**

```
## EJECUTADO — YYYY-MM-DD
- Journal: 00_META/journal/YYYY-MM-DD_<topic>.md
- Output: pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_interno/runs/2026-05-28_mode-a/
- Status: refinado y listo para alimentar Skill 6
- Next: esperar entrega Skill 6 ajustado por JP, después correr t-014
```
