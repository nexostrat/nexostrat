# 2026-05-12 — JP v3 presentation + cheat sheet + FAQ + Plan dual

**Session type:** work
**Duration:** ~3 hours
**Agent:** Claude Code (Opus 4.7 1M context)

## What was done

- **Cheat sheet del presentador** creado en español como guion para Ricardo presentar v2 a JP: `00_META/proposals/2026-05-12_jp-presentation-cheatsheet.md` (544 líneas). Una entrada por sección del HTML con bloque Qué es / Propósito / Por qué lo usamos / Cómo presentarlo. Sección final con tabla ejecutiva de decisiones + preguntas anticipadas + recordatorios de disciplina de presentador.
- **FAQ estructurado para JP** después de su ronda 1 de preguntas: `00_META/proposals/2026-05-12_jp-respuestas-ronda-1.md`. Tres partes: (a) respuestas directas a 5 preguntas/comentarios (revocación de llaves, Claude+secretos con analogía de caja fuerte + 6 capas de defensa, Notion compartido aceptado, transcripts vía Notion AI con revisión inmediata, walkthrough confirmado); (b) FAQ con 8 preguntas anticipadas organizadas por las 5 preocupaciones de JP (privacidad, seguridad, escalabilidad, despliegue, costo); (c) Plan dual de herramientas como propuesta nueva — paid en producción + libre en shadow + futura línea de servicio para clientes. Marcado cada cambio con `[ENMIENDA v2 → v3]`.
- **v3 del HTML construida y desplegada** en `00_META/proposals/2026-05-12_jp-presentation-v3.html` (2923 líneas, 123 KB, +25 KB sobre v2). v2 preservada intacta como histórico. Cambios concretos en v3:
  - Hero + footer + nav actualizados a v3 · 2026-05-12; nav agregó "Plan dual" y "Servicios".
  - Cimientos card Vault reescrita con analogía de caja fuerte digital + protocolo de revocación (emergencia vs rutinaria).
  - Cimientos card Secretos reescrita con paso a paso del descifrado a "pizarra de memoria" (RAM).
  - **NUEVO sub-bloque "Los 6 candados"** al final de Cimientos: callout azul con analogía del asistente humano + 6 sub-cards (caja fuerte, pizarra, guardia, reglas, permisos, rotación) + callout final sobre Anthropic ZDR + callout resumen.
  - Personas/events.jsonl re-redactado con "cuaderno de bitácora" + "sistema nervioso".
  - Stack: Notion ahora `$0 · cuenta de JP`, Whisper.cpp removido (movido a shadow), callout dorado al final que enlaza a Plan dual.
  - **NUEVA sección "Plan dual de herramientas"** entre Stack y Odoo: lede + 2 tarjetas (¿Por qué? + ¿Cómo se opera?) + tabla de 9 pares producción↔shadow + cronograma 4 semanas (Nextcloud + Jitsi, Ollama, Whisper, Anytype) + callout de honestidad.
  - Odoo reframe — ya no es caso aislado, primer ejemplo de la familia "Servicios".
  - **NUEVA sección "Servicios"** después de Odoo: 5 servicios numerados con tickets aproximados (Notion→Anytype USD 800-1500, Drive→Nextcloud USD 1.2-2.5K, Meet→Jitsi USD 600-1.2K, Whisper USD 800-1.5K, Odoo USD 5-25K) + callout "¿Por qué tú usas Notion entonces?".
  - Otras decisiones reorganizada: privacidad de grabaciones marcada CERRADA por JP con badge verde; agregadas 2 nuevas (Plan dual + Split de costos pre-revenue); Odoo extendida a "Odoo + línea de servicio en software libre".
  - Camino paso 2 ampliado: "Scaffold + Skills 2-5 + **shadows del plan dual** en paralelo".
  - Firma: nuevo radio group `dual-choices` (aprobar Stage 1 / después / solo Odoo) registrado en el JS.
  - "¿Qué estás viendo?" con callout "Nuevo en v3" listando las novedades + lenguaje más amigable con analogías.
- **Cheat sheet realineado a v3** después de construir el HTML: removidos los 3 marcadores `[PRESENTAR VERBAL]` (ya son secciones reales del HTML), renumeradas las secciones (11.5 → 12 Plan dual, 12 → 13 Odoo, agregada 14 Servicios, 13 → 15 Install, 14 → 16 Otras, 15 → 17 Camino, 16 → 18 Firma), tabla ejecutiva de decisiones re-mapeada a las nuevas secciones HTML, recordatorios expandidos con glosario de analogías. Marcadores `[NUEVO EN V3]` agregados a las 3 secciones nuevas.
- **FAQ realineado a v3** después de construir el HTML: header apunta a v3 como activo; sección "Resumen de enmiendas para v3" renombrada a "Enmiendas aplicadas en v3 del HTML" con 15 items detallados de qué cambió y cómo aparece en el HTML; agregada lista de pendientes documentales (key-rotation, meeting, cost-sharing, compliance protocols) que se crearán durante el scaffold.

## Decisions made

- **Plan dual de herramientas adoptado como propuesta v3** — usar pagado en producción + libre en shadow paralelo + futura línea de servicio para clientes. Razones: vender lo que sabemos operar, probar antes de prometer, reducir vendor lock-in, credibilidad real. Costo del shadow: USD 0. Esfuerzo: 5-7 días de Ricardo en las primeras 4 semanas + ~2-4h/sem ongoing. Decisión final pendiente de JP (radio button en Firma).
- **Privacidad de grabaciones cerrada con la respuesta de JP** — Notion AI Meeting Notes + disciplina de revisión inmediata (≤15 min al colgar) + export del resumen revisado al repo en `clients/<cliente>/transcripts/`. Audio se elimina del Notion después de revisar (a menos que haya razón explícita). Whisper.cpp baja de Stage 1 a shadow del plan dual.
- **Notion aportado por JP** — workspace de JP compartido con la compañía. Ahorra ~USD 10/mes en Stage 1. Cuando se constituya entity, transferir billing.
- **v3 del HTML armada AHORA, no después del walkthrough** — pivot mid-session a petición de Ricardo. Originalmente plan era construir v3 después del walkthrough; cambió a "v3 ya y v4 si hace falta tras enmiendas".
- **Lenguaje ELI5 con analogías estandarizado** — caja fuerte (encriptación), cuaderno de bitácora (events.jsonl), sistema nervioso (event-driven), pizarra de memoria (RAM), guardia en la puerta (hooks), asistente humano (Claude+secretos), shadow (herramienta libre paralela), segundo par de ojos (PR review), línea de ensamblaje (cadena de producción). Glosario incorporado a los recordatorios del cheat sheet.

## Open items

- **t-001 (updated):** Mandar v3 HTML + cheat sheet + FAQ a JP; capturar accept/edit/decline vía walkthrough. Critical, due 2026-05-13.
- **t-010 (NUEVA):** Agendar walkthrough con JP (60-90 min, pantalla compartida). Critical, due 2026-05-15. JP debe mandar 2-3 ventanas.
- **t-006:** JP vota top-5 brand HTML. High, due 2026-05-14 (sin movimiento esta sesión).
- **Post-walkthrough:** v4 del HTML solo si JP propone enmiendas adicionales. Open-ended.
- **Docs de gobernanza pendientes** (parte de scaffold t-002, blocked downstream): `00_GOVERNANCE/key-rotation-protocol.md`, `00_GOVERNANCE/meeting-protocol.md`, `00_PARTNERSHIP/cost-sharing-agreement.md`, `00_GOVERNANCE/compliance-checklist.md`.

## Notes

- v3 quedó balanceada estructuralmente: 18 secciones (16 originales + 2 nuevas) con 18 closes; 466 divs balanceados; 17 h2, 53 h3, 115 `<p>` todos cuadrados. Validado vía Python regex post-edición.
- Pivot mid-session (de "v3 después del walkthrough" a "v3 ya") fue acertado — permitió que cheat sheet + FAQ + HTML quedaran consistentes en un solo pase. Si JP llega al walkthrough con feedback adicional, v4 es edición sobre v3 (no rebuild from scratch).
- El plan dual tiene un riesgo real: tiempo de shadow compite con tiempo de cliente. Mitigación documentada en el callout de honestidad de v3: "cadencia mínima ~2 h/sem". Ricardo debe respetar esto si JP aprueba.
- Notion AI transcripts en inglés fue mencionado por JP — diagnóstico anotado en FAQ Parte 1 (probable setting de workspace/página/detección automática). Se revisa en el walkthrough.
- Cheat sheet quedó exclusivamente para Ricardo (no se entrega a JP). FAQ es para JP. HTML es para JP. Tres documentos con audiencias distintas.

## Files written this session

- **Creados:**
  - `00_META/proposals/2026-05-12_jp-presentation-cheatsheet.md` (544 líneas)
  - `00_META/proposals/2026-05-12_jp-respuestas-ronda-1.md` (3 partes)
  - `00_META/proposals/2026-05-12_jp-presentation-v3.html` (2923 líneas, 123 KB)
- **Modificados al cierre:**
  - `STATUS.md` (fase, recent activity, blockers, next milestone)
  - `tasks.json` (t-001 updated; t-010 added)
  - `00_META/journal/2026-05-12_jp-v3-presentation-and-supporting-docs.md` (este archivo)
- **Sin cambios:**
  - `events.json` (no events scheduled todavía — pendiente del walkthrough)
  - `00_META/CHANGELOG.md` (no se editaron archivos de contexto)
  - `2026-05-11_jp-presentation.html` (v2 preservada intacta como histórico)
