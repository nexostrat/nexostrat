# Sesión 28 — 2026-05-29 — Auditoría Skill 6 + gold standard Andrea + Plan Maestro de skills

**Persona:** Founder (root, operator-driven; el trabajo sustantivo cae en pipeline/ y skills/).
**Operador:** Ricardo.
**Arco:** una sesión que arrancó como auditoría puntual y escaló a una estrategia de reconstrucción de skills.

## Qué pasó

Ricardo abrió pidiendo auditar los resultados del Skill 6 corridos el día anterior sobre Trixx (su primera prueba real del skill, con dos versiones: `skill_raw/` cruda + `version_limpia/` corregida a mano). La pidió como sesión de auditoría: él dictaba documento por documento lo que veía mal, yo lo organizaba.

### 1. Auditoría del Skill 6 (run Trixx)
Documenté todos sus comentarios en `pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/auditoria_skill6_trixx_20260529.md`, organizado en 10 transversales + secciones por documento (B-H) + "lo que sí funciona". El hallazgo dominante (T1) es que el skill afirma cosas que no podemos sostener ("estudiamos a sus competidores", "nos reunimos con el equipo") cuando solo hubo una reunión de 3h con la dirección + análisis online — hay que calibrar el lenguaje a lo que realmente sabemos. Otros: T2 sacar "IA" de los títulos, T3 pricing (luego resultó ya resuelto por JP), T4 "liberar no reemplazar", T5 nunca "robot", T7 emojis (Ricardo REVIRTIÓ la prohibición: bien usados se mantienen), T8 template (logo + footer + justificado), T9 assets de marca reales, T10 nombre legal "Trixx Logistics Corp" (no "Grupo Trixx").

### 2. Gold standard: deck + cheat sheet de Andrea
A mitad de sesión Ricardo pidió, urgente, una presentación HTML + cheat sheet para una reunión con Andrea (hija de María Helena, influenciadora clave). Brainstorm corto para fijar el diseño (relación + opinión, sin sección de agradecimiento, info puntual, sin precios, diseño premium), y lo construí a mano (NO vía Skill 6) en `reunion_andrea/`: `Trixx_Andrea_Presentacion.html` (deck 7 slides navegable), `Trixx_Andrea_CheatSheet.html` (la "hoja de trampa" de Ricardo: objetivo, perfil de Andrea, advertencias OJO en orden de la presentación, guion por slide, sonda de presupuesto sutil, glosario) y `build_andrea.py` (reproducible, logos reales embebidos en base64, paleta Aurora, Inter). Verificado en navegador vía servidor local. Ricardo lo declaró el **gold standard** y dijo que el cheat sheet es lo que querrá en todos los skills. Corrigió el nombre a "Trixx Logistics Corp" (este y futuros docs). La reunión con Andrea ya ocurrió después; su transcript quedó en `transcripts/` (untracked, lo maneja Ricardo).

### 3. De auditoría a estrategia: el Plan Maestro
Ricardo subió un zip con las versiones nuevas de tres skills. Comparé contra el repo en staging (`/tmp/skills_incoming_20260529/`):
- **client-deliverables (Skill 6):** versión nueva de JP, que ya arregló el pricing (3K/8K/15K + "depende del alcance") y el total de roadmap. Esta es la base.
- **pptx-expert del zip:** regresión (Century Gothic vs Inter del repo, más nuevo) → descartada.
- **editorial-designer:** idéntica al repo.

Explicamos la arquitectura (motores técnicos genéricos `docx`/`pptx` vs capas de marca `editorial_designer`/`pptx_expert`), decidimos crear un experto HTML dedicado (el canal HTML se volvió de primera: link privado + QR), y Ricardo reformuló el plan: reconstruir tres expertos especializados **00_nexostrat_{docx,pptx,html}** sobre las bases oficiales de Anthropic + la inteligencia de marca de Nexostrat, todos leyendo una sola fuente de marca, y luego cablear Skill 6 + una variante **6.A** gold-standard. Tras un Q&A de cuatro decisiones, quedó todo lockeado y escrito en `plan_maestro_skills_20260529.md` (supersede el plan de auditoría v1, que borré).

## Decisiones lockeadas (D1-D7)
- D1 Web expert dedicado (HTML).
- D2 Fuente de marca única, primero (Fase 0).
- D3 **Inter en todo** (reemplaza Century Gothic; gate: visto bueno de JP).
- D4 Base HTML = plugin oficial **frontend-design**.
- D5 Autoría de skills con **skill-creator + writing-skills**, sintetizando.
- D6 **Borrar** editorial_designer, pptx_expert, docx_technical, pptx_technical tras absorberlos.
- D7 Skill 6 base = versión de JP + nuestros cambios; crear **6.A** gold como segundo punto de comparación.

## Hallazgos de la exploración
- Los oficiales docx/pptx YA están vendorizados (`skills/docx_technical`, `skills/pptx_technical`).
- No hay skill HTML oficial estilo docx/pptx → base = frontend-design.
- 4 copias de logos (operations/marketing/brand/logos + operations/assets/brand/Logos + copia en cada skill) → consolidar.
- Persona Don Carlos en `operations/marketing/buyer_personas/`; brand guide en `operations/assets/brand/Nexostrat_Brand_Guide.docx`.

## Commits
`0823061` auditoría · `543f278` evidencia sesión-28 (skill_raw + version_limpia + diagnóstico refinado) · `66d3b04` entregables Andrea + T10 + gitignore · `32f0d13` plan auditoría v1 → `6301edc` plan maestro v2 → `d320bce` retiro v1 · + commit de cierre de sesión.

## Memorias
Actualizadas 2: `feedback_no_emojis_no_symbols` (emojis revertidos para entregables: criterio "con propósito, formales, no excesivos") y `project_trixx_team_structure` (nombre legal "Trixx Logistics Corp").

## Estado al cierre
- Working tree: limpio salvo dos untracked dejados a propósito — el zip de JP en `skills/` (input transitorio) y `pipeline/clients/trixx-logistics/transcripts/` (transcript Andrea, lo maneja Ricardo).
- Sin Gemini handoff, sin memos en inbox, sin cambios bajo `vault/`.
- Prompt de arranque de la próxima sesión en `edicion_correccion_trixx_skill6/PROMPT_proxima_sesion.md`.

## Qué sigue
Sesión dedicada (Skills-Master) para ejecutar el Plan Maestro, empezando por la Fase 0 (fundación de marca única), una vez JP dé el visto bueno a "Inter en todo". Tareas nuevas: `t-skills-trio-rebuild`, `t-jp-inter-blessing`, `t-skill6-apply-audit-findings`.
