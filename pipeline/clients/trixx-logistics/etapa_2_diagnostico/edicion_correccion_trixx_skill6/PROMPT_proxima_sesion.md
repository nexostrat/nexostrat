# Prompt para arrancar la próxima sesión (Fase 2 — construir el trío de skills)

> Pegar el bloque de abajo tal cual al inicio de la próxima sesión.
> Estado: Fases 0 y 1 del Plan Maestro YA ejecutadas y commiteadas (sesión 29, 2026-05-29).

---

```
Start Session.

Vamos a ejecutar la FASE 2 del Plan Maestro de skills: construir el trío de expertos de formato 00_nexostrat_{pptx,docx,html} sobre las bases oficiales de Anthropic + la marca única. Esto es trabajo de Skills-Master (carpeta skills/).

ANTES DE PROPONER NADA, lee estos archivos committeados:
1. Plan maestro (fuente de verdad):
   pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/plan_maestro_skills_20260529.md
2. Fuente ÚNICA de marca (leída por los tres expertos + Skill 6):
   operations/marketing/brand/brand-identity.md
3. Gold standard de referencia (deck + cheat sheet + builder, HTML hecho a mano):
   pipeline/clients/trixx-logistics/etapa_2_diagnostico/reunion_andrea/
4. Auditoría de Skill 6 (alimenta la Fase 4, no la 2):
   pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/auditoria_skill6_trixx_20260529.md

ESTADO YA HECHO (sesiones 28-29, NO re-litigar):
- Fase 0 (marca única): home en operations/marketing/brand/ — logos consolidados (18 PNG tracked), brand-identity.md canónico v2.0 (Inter en todo, LatAm México→Colombia, persona Don Carlos, pricing fuera, voz calibrada T1/T2/T4/T5/T7). brand.py + build_andrea.py repuntados. .gitignore con excepción para que el home llegue a mirrors.
- Fase 1 (base HTML): skills/frontend_design/ = vendorizado verbatim de frontend-design (Apache 2.0) + PROVENANCE.md.
- Bases oficiales ya vendorizadas: skills/docx_technical/, skills/pptx_technical/, skills/frontend_design/.
- Decisiones D1-D7 lockeadas. JP dio OK a Inter.

FASE 2 — construir el trío (con skill-creator + writing-skills, sintetizando; validar cada uno contra el gold standard):
- 2a) 00_nexostrat_pptx: auditar oficial pptx_technical vs pptx_expert; portar lo aplicable + conservar la capa estratégica/narrativa de pptx_expert + plantilla/reference. Inter (NO la regresión Century Gothic).
- 2b) 00_nexostrat_docx: comparar oficial docx_technical vs nexostrat_editorial_designer; llevar lo relevante de editorial_designer al oficial.
- 2c) 00_nexostrat_html: sobre frontend_design. El más completo (diseños propios + integra los de docx/pptx). Encodear los patrones del gold standard de Andrea (motor de slides, scroll, tokens de marca, responsive, logos base64, link privado, QR). IMPORTANTE: este experto debe OVERRIDE la guía del base frontend-design que prohíbe Inter — la marca manda (Inter es elección deliberada). Ver skills/frontend_design/PROVENANCE.md.
- Cada experto: lee SOLO operations/marketing/brand/brand-identity.md como fuente de marca, referencia los assets canónicos (logos en operations/marketing/brand/logos, persona Don Carlos, brand guide), y conoce a Don Carlos (mensajes enfocados al persona).

REGLAS:
- NO ejecutar borrados de skills (D6 / Fase 3: editorial_designer, pptx_expert, docx_technical, pptx_technical) sin confirmación explícita de Ricardo. Eso es Fase 3, después de validar el trío.
- Validación = render real end-to-end en Linux (no solo "existe el script"), comparado contra el gold standard de Andrea.
- Antes de tocar archivos, dame un resumen del estado y un plan de ataque para 2a/2b/2c.
```
</content>
