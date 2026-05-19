# CHECKPOINT — trixx-logistics (Client-Owner)

**Updated:** 2026-05-18 (PM, session 4)
**By:** ricardo (via Claude Code at /srv/Nexostrat/)
**Persona:** Client-Owner

## What just happened

Cliente scaffolded vía `infra/scripts/new-client.sh` con `pilot=true`. Intake llenado a partir del WhatsApp inicial de Andrea Chávez (referido vía Sofía Estavilo) + URL del sitio oficial enviada por la contacto. Comunicación inicial archivada en `communications/2026-05-18_initial-contact.md` con extracción de señales factuales + análisis del trade-off de pre-encuesta (decisión: no enviar formulario; alternativa = WhatsApp ligero a Andrea preguntando audiencia de la reunión).

**Estado factual locked:**
- Marca: Trixx Logistics (dos X — sitio oficial). LinkedIn corporativo usa una X (anomalía).
- País: México. Sede operativa de la contacto: Tijuana.
- +20 años de operación (cita verbal de la contacto).
- Auto-percepción: *"muy atrás en programas y tecnología"* (cita textual).
- Intención inicial: *"automatizaciones y más"*.
- Contacto principal: Andrea Chávez (+52 1 664 533 3512). Trabaja con su "tío" (dueño, en sentido tijuanense — relación familiar real por confirmar). Madre también trabaja en la compañía.
- Audiencia de reunión: no confirmada.

## In flight — concrete next action

**Skill 01 (company-analyst) COMPLETADO 2026-05-18 PM.** Outputs:
- `01_company_analysis/runs/2026-05-18_mode-a/final_report.md` (35 KB, 13 secciones completas con etiquetas ✅/⚠️/❓)
- `01_company_analysis/runs/2026-05-18_mode-a/Trixx_AnalisisCompania_20260518.docx` (80 KB)

**Hallazgos de Skill 01 que cambian el mapa:**
- ⚠️ LinkedIn `linkedin.com/company/trix-logistics/` es de empresa UK distinta (Leicester, 4 empleados, paquetería). Trixx MX **no tiene página corporativa LinkedIn**.
- ✅ Fundación 2002 (24 años — coherente con +20 verbal de Andrea).
- ✅ 5 sedes (descubierta CDMX adicional a TJ/GDL/Vernon/SD).
- ✅ Dos entidades legales: Trix Importaciones Comerciales S. de R.L. de C.V. (MX) + Trixx Logistics Corp (US).
- ✅ Dueño identificado: Hector Leyva.
- ✅ USDOT 2045279 activo, flota 12 trucks + 9 drivers, 0 crashes 24m, OOS rates mejores que media nacional.
- ⚠️ Patente aduanal NO expuesta públicamente — señal a verificar.
- ⚠️ Sitio con bugs en producción ("0 Años" + fish-species placeholder en /home-logistic/).
- ✅ Madurez digital 2/5 confirmada (coherente con auto-evaluación de Andrea).

**Siguiente:** revisión humana de Ricardo del .md → si OK → Skill 02 (industry-analyst) sobre logística cross-border MX-USA / agencia aduanal.

**Update 2026-05-18 PM continuación:** Ricardo revisó Skill 01 .md, marcó 3 correcciones (contador "0 Años" es animado JS no bug, página /home-logistic/ no enlazada en nav principal, página /contacto/ sí tiene click-to-WhatsApp + iconos sociales). Correcciones aplicadas al .md + .docx regenerado. Memoria `feedback_animated_counters_not_bugs.md` guardada para evitar el patrón en futuros clientes. Task #6 abierta para Skill 04: calibrar nivel de preguntas (las de Skill 01 se sintieron muy técnicas para primera reunión — Ricardo prefiere discovery abierto + relationship-building, no auditoría técnica).

**Skill 02 COMPLETADO 2026-05-18 PM.** Outputs:
- `02_industry_analysis/runs/2026-05-18_mode-a/LogisticaCrossBorder_MX_20260518.md` (10 secciones, ~5,500 palabras, 40+ fuentes)
- `02_industry_analysis/runs/2026-05-18_mode-a/LogisticaCrossBorder_MX_20260518.docx` (83 KB)

**Hallazgos de Skill 02 que importan para la reunión:**
- Sector mexicano de autotransporte de carga = 3.8% PIB nacional, USD 92B mercado 2025 → USD 141B 2034 (CAGR 4.41%)
- Pero PIB sectorial estancado en 2025 (+0.02%); el nicho cross-border Tijuana sí está creciendo (+8% YoY freight)
- Reforma Ley Aduanera vigor 1-ene-2026: patentes ya no vitalicias, responsabilidad solidaria del agente, certificación cada 3 años
- Carta Porte 3.1 multas $850-$53,650 MXN + cárcel 3-6 años por contrabando presunto
- USMCA Review decisión 1-jul-2026
- IA aduanera mexicana ya tiene 5 players activos (AduanApp 95% precisión 7-13s, Taxer 56% ahorro tiempo, Moco AI, Camtom, Experta) — early-adopter window 18-30 meses
- **Competidor real de Trixx no son los agentes locales — es Nuvocargo** (USD 74M funding, US-MX foco, expandió 2024 a todos los crossings)
- Trixx = Arquetipo A (dueño-operador), no Arquetipo B (corporativo) — lenguaje matters

**Siguiente:** revisión humana Skill 02 → si OK → Skill 03 (competitor-analyst) profundizando contra Nuvocargo + agentes locales TJ + AduanApp ecosystem.

**Skill 03 COMPLETADO 2026-05-18 PM.** Outputs:
- `03_competitor_analysis/runs/2026-05-18_mode-a/Trixx_Competencia_MX_20260518.md` (8 secciones, ~5,200 palabras)
- `03_competitor_analysis/runs/2026-05-18_mode-a/Trixx_Competencia_MX_20260518.docx` (78 KB)

**Hallazgos de Skill 03:**
- 5 competidores directos mapeados: Nuvocargo (USD 74M, AI-native, target 150-350 envíos/mes — EXACTO segmento Trixx), Flexport (e-commerce fulfillment dobló en 60 días post-tarifas 2025, AI auditor 0.2% error), TCI (+30 años, modelo espejo de Trixx sin tech), Integración Aduanal (OEA + ISO + patente 3743 visibles), Grupo Aduanal Arellano (chico, sin certs).
- 5 indirectos: Estafeta, DHL Supply Chain MX, Solistica, AduanApp (herramienta o competencia según ángulo), Aispuro Lavenant (sitio "en construcción" actualmente).
- Posición de Trixx en mapa: empata o gana contra locales (TCI, Arellano, Aispuro); pierde marcadamente contra tech-enabled (Nuvocargo, Flexport) en 5 dimensiones críticas (portal cliente, IA adoptada, madurez digital, certificaciones, funding).
- Las primeras 3 dimensiones son atacables en 6-12 meses con Nexostrat; las 2 últimas son estructurales.
- **5 talking points calibrados a primer encuentro** (sin profundidad técnica, basados en feedback de Ricardo sobre Skill 01): Nuvocargo como urgencia, diferenciadores ya en sitio (chino + multi-sede), trampa de responsabilidad solidaria 2026, gap silencioso de tracking, ventana de 18-30 meses.

**Siguiente:** revisión humana Skill 03 → si OK → Skill 04 (discovery-meeting / PrepLlamada). Antes de Skill 04, llenar `00_intake/our_hypotheses.md` (juicio: dolor, decisor, presupuesto, tono, capability-fit). PrepLlamada es el primer skill que SÍ lee our_hypotheses.md per ADR-027.

## Blocked on

Ninguno crítico para Skill 01. Pendientes paralelos:
- Sección 6 de research_input.md (audiencia de la reunión) — se cierra cuando Andrea confirme vía WhatsApp.
- `our_hypotheses.md` — sin tocar; se llena antes de Skill 04.

## Open questions

1. Spelling: Skill 01 confirma si LinkedIn `trix-logistics` (una X) es la grafía corporativa real o un artefacto del handle. El sitio oficial usa dos X.
2. Identidad del "tío" dueño de la compañía — Skill 01 puede mapearlo desde LinkedIn / DENUE.
3. RFC, año exacto de fundación, certificaciones (C-TPAT / OEA esperables en logística cross-border) — todas a investigar por Skill 01.

## Files modified but not yet committed

- `state.json` (NEW — vía scaffold)
- `checkpoint.md` (este archivo)
- `README.md` (NEW — stub per-cliente del scaffolder)
- `00_intake/research_input.md` (NEW + llenado con datos de primera mano del WhatsApp)
- `00_intake/our_hypotheses.md` (NEW — sin llenar todavía, sellado hasta Skill 04)
- `communications/2026-05-18_initial-contact.md` (NEW — transcripción + análisis)
- `01_company_analysis/.gitkeep` y demás stages (NEW — vía scaffold)

## Estimated time to finish

- Skill 01 + revisión humana: ~30-45 min.
- Skill 02 + revisión: ~30 min.
- Skill 03 + revisión: ~30 min.
- our_hypotheses.md (operador): ~15-20 min.
- Skill 04 (PrepLlamada): ~20 min + revisión.
- **Total a Monday 2026-05-25:** ~2.5-3h de sesión efectiva, distribuible entre hoy y el lunes en la mañana.

## After this, what's next

Reunión 2026-05-25 1pm Tijuana en oficina de Andrea. Llevar PrepLlamada (Skill 04 output) como guía. Grabar reunión. Post-reunión → Skill 05 (Opportunity Report) → revisión obligatoria Ricardo+JP (Fase 5) → entrega manual (Fase 6).
