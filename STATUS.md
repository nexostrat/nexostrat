# Mejía IA & Cía — STATUS

> **Last updated:** 2026-05-12

## Current phase

**Pre-launch / v3 architecture ready for JP walkthrough, brand top-5 also pending JP vote.** Twenty architectural ADRs captured 2026-05-11 → v2 HTML built. JP delivered ronda 1 de preguntas 2026-05-12 → answered + extended into a **v3 HTML** that incorporates all enmiendas plus a major new strategic addition: the **Plan dual de herramientas** (paid in production + free shadow + future line of service for clients) and a **Servicios** section cataloguing 5 billable service lines built on libre tools. Brand pivot tournament closed 2026-05-12 with Nexostrat as Ricardo's pick (8/10) and Aurora/The Architect tied on palettes (5/5). Plan 1 work and brand acquisition both gated on JP's reviews — walkthrough con JP es el cuello de botella.

## Recent activity

- **2026-05-12** — Set completo de deliverables para JP listo. Cheat sheet en español como guion de presentador (`2026-05-12_jp-presentation-cheatsheet.md`, 544 líneas) + FAQ estructurado respondiendo 5 preguntas directas + 8 preguntas anticipadas por 5 concerns (privacidad, seguridad, escalabilidad, despliegue, costo) más sección "Plan dual" (`2026-05-12_jp-respuestas-ronda-1.md`). **v3 del HTML** construida (`2026-05-12_jp-presentation-v3.html`, 2923 líneas, 123 KB) con: nuevo sub-bloque "Los 6 candados" con analogía caja fuerte al final de Cimientos, nueva sección "Plan dual de herramientas" entre Stack y Odoo (9 pares producción↔shadow + cronograma 4 semanas), nueva sección "Servicios" después de Odoo (5 líneas de servicio con tickets aproximados), decisión grabaciones marcada CERRADA por JP, Notion=$0 (cuenta JP), Whisper movido a shadow, nuevo radio button "Plan dual" en Firma. Lenguaje ELI5 con analogías (caja fuerte, cuaderno de bitácora, pizarra de memoria, guardia en la puerta, asistente humano, shadow). v2 preservada intacta como histórico.
- **2026-05-12** — Brand identity tournament complete. Four AIs ran in parallel across three rounds. Real availability audit via Verisign RDAP + Python DNS + WebFetch tested 41 names; only `nexostrat.com` and `criteriostrategy.com` genuinely available. StratiaLabs descartado. Final top-5 HTML deliverable at `00_META/proposals/2026-05-12_brand-final-top5.html`. Ricardo's ratings: Nexostrat 8 (top), Criterio Strategy 4, Consilea 3, Tervia Strategy 1, Veracta Partners 0. Palette ratings: Aurora 5/5 + The Architect 5/5 tied; Solera 4; Architectural Blue 4; Cosmos 3. Side findings: Gemini CLI preliminary Odoo research (feeds t-008); Fraunces serif banned (feedback memory).
- **2026-05-11** — Architecture locked across 20 ADRs. Full spec at `00_META/proposals/2026-05-11_company-system-design.md`. v2 HTML at `00_META/proposals/2026-05-11_jp-presentation.html`.
- **2026-05-11** — Project scaffolded under `01_VENTURES/04_MejiaIACia/`.

## Blockers

- **Agendar walkthrough con JP** — t-010, critical, due 2026-05-15. JP debe mandar 2-3 ventanas para sesión de 60-90 min en pantalla compartida. Cierre de decisiones obligatorias 1/2/3 (interfaz, plan dual, aprobación general) depende del walkthrough.
- **JP review de v3 HTML + cheat sheet + FAQ** — t-001 (updated), critical, due 2026-05-13. Mismo blocker pero captura el "send + capture accept/edit/decline". El walkthrough es el mecanismo de captura.
- **JP vote on top-5 brand HTML** — t-006, due 2026-05-14. Brand decision gates name/domain acquisition.

## Next milestone

JP firma v3 (con o sin enmiendas) + vota brand top-5 → desbloquear Plan 1 (Foundation + Scaffold + Skills 2-5 + shadows del plan dual en paralelo) y brand acquisition (t-007).

Open follow-ups beyond Plan 1:

- Manual verification + acquisition of winning brand name's surfaces — t-007, due 2026-05-16.
- Odoo opportunity memo — t-008, due 2026-05-25.
- Decide Heavy/Hosted/Light default with JP during architecture review — t-004.
- Brand propagation across project docs (Plan Maestro, README, scope) after name locked — t-009.
- First unpaid pilot client identification — t-005, target 2026-06-30.
- **Crear docs de gobernanza** durante scaffold (parte de t-002): `key-rotation-protocol.md`, `meeting-protocol.md`, `cost-sharing-agreement.md`, `compliance-checklist.md`.
