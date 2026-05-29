# Prompt para arrancar la próxima sesión (ejecución del Plan Maestro de skills)

> Pegar el bloque de abajo tal cual al inicio de la próxima sesión.
> Prerrequisito: tener el OK de JP sobre "Inter en todo".

---

```
Start Session.

Vamos a ejecutar el Plan Maestro de reconstrucción de skills (docx/pptx/html) + Skill 6. Esto es trabajo de Skills-Master (carpeta skills/), aunque el plan vive en pipeline/.

ANTES DE PROPONER NADA, lee estos archivos committeados:
1. Plan maestro (fuente de verdad de esta tarea):
   pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/plan_maestro_skills_20260529.md
2. Auditoría de Skill 6 (hallazgos T1-T10 que alimentan la Fase 4):
   pipeline/clients/trixx-logistics/etapa_2_diagnostico/edicion_correccion_trixx_skill6/auditoria_skill6_trixx_20260529.md
3. Gold standard de referencia (deck + cheat sheet + builder, HTML hecho a mano):
   pipeline/clients/trixx-logistics/etapa_2_diagnostico/reunion_andrea/

CONTEXTO RÁPIDO (ya decidido la sesión anterior, 2026-05-29):
- Objetivo: reconstruir tres expertos especializados — 00_nexostrat_docx, 00_nexostrat_pptx, 00_nexostrat_html — sobre la base oficial de Anthropic + marca Nexostrat, leyendo UNA sola fuente de marca; luego cablear Skill 6 + una variante 6.A gold-standard.
- Decisiones lockeadas: (D3) Inter en TODOS los canales (reemplaza Century Gothic, que no está en Linux); (D4) base HTML = plugin oficial frontend-design; (D5) autoría con skill-creator + writing-skills, sintetizando; (D6) borrar editorial_designer, pptx_expert, docx_technical y pptx_technical tras absorberlos; (D7) Skill 6 base = versión de JP + nuestros cambios, y crear 6.A gold.
- Hallazgos clave: los oficiales docx/pptx YA están vendorizados (skills/docx_technical, skills/pptx_technical); NO hay skill html oficial; hay 4 copias de logos a consolidar en operations/marketing/brand/logos; persona Don Carlos en operations/marketing/buyer_personas/; brand guide en operations/assets/brand/Nexostrat_Brand_Guide.docx.
- Versión nueva de Skill 6 (de JP) está en el zip skills/drive-download-20260529T184628Z-3-001.zip. Ya resolvió pricing (3K/8K/15K + "depende del alcance") y el total de roadmap; NO re-auditar eso. El pptx-expert del zip es una regresión (Century Gothic) — descartar. El editorial-designer del zip es idéntico al repo.

PENDIENTES QUE NECESITAN A JP ANTES DE EJECUTAR (verificar al inicio):
- Visto bueno de JP a "Inter en todo" (bloquea la Fase 0).
- Modelo de integración Skill 6 ↔ trío (determinista / Claude-driven / híbrido); parcialmente cubierto por el par 6/6.A.

EMPEZAR POR: Fase 0 del plan (fundación de marca única) — consolidar las 4 copias de logos en operations/marketing/brand/logos, apuntar skills/shared/brand.py ahí, y consolidar UN brand-identity.md canónico (Inter). Antes de tocar archivos, dame un resumen del estado y confírmame que el OK de JP sobre Inter está dado. No ejecutes destructivos (borrados de skills) sin confirmación explícita.
```
