---
file_type: our_hypotheses
adr: ADR-027
slice: judgment (3) — hypotheses + people-judgments + Nexostrat-side constraints
read_by: [skill-04-discovery-meeting, skill-05-opportunity-report]
sealed_during: [skill-01-company-analyst, skill-02-industry-analyst, skill-03-competitor-analyst]
companion: research_input.md
---

# Our Hypotheses — `<slug>`

> **Qué es esto:** lo que **creemos / intuimos / asumimos** sobre la empresa, sus dolores, su decisor, su tono.
> **Quién lo lee:** Skills 04 (PrepLlamada) y 05 (Reporte de Oportunidades). **NUNCA Skills 01-03.**
> **Por qué sellar durante research:** ADR-027 — si Skills 01-03 leyeran esto, sus salidas estarían contaminadas por nuestras hipótesis y perderíamos la capacidad de comparar **"lo que esperábamos vs lo que la investigación encontró"** en la síntesis.
> **Disciplina del operador:** al invocar `Analiza <slug>` (Skill 01) y los siguientes Skills 02 y 03, **NO** pegar el contenido de este archivo en el contexto. Pasarlo solo a partir de Skill 04.

---

## 1. Hipótesis sobre el dolor del cliente

- **¿Qué creemos que les duele?** *(hipótesis nuestra — Skills 04+05 la confirmarán o refutarán contra lo que dijo el cliente en la reunión)*

- **¿Por qué creemos que están abiertos a hablar con nosotros AHORA?** *(evento detonante, momento de la empresa, oportunidad detectada — nuestra lectura del timing)*

- **¿Qué problema NO se ha resuelto con consultorías previas, según lo que percibimos?**

## 2. Hipótesis sobre el decisor

- **¿El contacto principal es decisor o influenciador?** *(nuestra evaluación, no lo que dijeron ellos)*
- **¿Quién creemos que es el decisor final si no es el contacto?** *(nombre o rol)*
- **¿Qué presión interna podría estar sintiendo el contacto?** *(cuota, deadline, reorganización, etc.)*
- **Nivel de sofisticación tecnológica esperada del contacto:** [ ] bajo · [ ] medio · [ ] alto · [ ] muy alto

## 3. Presupuesto y disposición a pagar (estimado)

- **Señales de presupuesto que observamos:** *(tamaño, contrataciones recientes, inversiones visibles, expansión, prensa, etc.)*
- **Rango de inversión que CREEMOS pueden absorber para un piloto de IA:** [ ] < USD 5K · [ ] 5-15K · [ ] 15-40K · [ ] 40K+ · [ ] no tenemos pista
- **¿Por qué pensamos esto?** *(base del estimado)*

## 4. Tono y zonas sensibles

- **¿Tono apropiado para esta empresa?** [ ] formal · [ ] cercano · [ ] técnico · [ ] estratégico · [ ] mixto: ________
- **¿Hay temas sensibles que NO debemos tocar?** *(casos legales pendientes, cambios accionarios, despidos recientes, demandas, problemas reputacionales — todo lo que el equipo sabe pero la investigación pública no necesariamente captura)*
- **¿Cómo creemos que reaccionarán a la propuesta de "Hoja de Ruta de IA"?** [ ] receptivo · [ ] cauto · [ ] resistente · [ ] no sabemos

## 5. Capacidades de Nexostrat aplicables (hipótesis pre-investigación)

> Esto evita que Skill 05 proponga soluciones fuera de la capacidad real de Nexostrat.

Capacidades base actuales — marcar las que parecen aplicables:

- [ ] Agente WhatsApp + DM *(automatización de respuestas + lead capture)*
- [ ] CRM + lead scoring *(configuración + automatizaciones + reporting)*
- [ ] Dashboard sell-out *(visualización de datos comerciales)*
- [ ] Pipeline de contenido *(generación + publicación automatizada)*
- [ ] Análisis de procesos + automatización de tareas repetitivas
- [ ] Otra: ________________

**Capacidades que CLARAMENTE NO podemos entregar a esta empresa:** *(anti-overpromising — los skills posteriores no las propondrán)*

## 6. Lo que esperamos que la investigación confirme o refute

> Esta sección la lee Claude-as-Judge al sintetizar (Skill 05). Si la investigación encontró algo contrario, lo marca explícitamente.

- *(Hipótesis 1 — ej. "Creemos que su CRM es Salesforce")*
- *(Hipótesis 2 — ej. "Creemos que su ciclo de venta promedio es 4-6 meses")*
- *(Hipótesis 3 — ej. "Creemos que el CFO es el bloqueador principal")*

## 7. Riesgos comerciales que vemos

- **¿Qué podría hacer que esta oportunidad se cierre?** *(no del lado de Nexostrat — del lado del cliente: rotación, M&A, reestructura, agotamiento de presupuesto, decisión de no priorizar IA)*
- **¿Hay competidores nuestros con ventaja estructural aquí?** *(Bain, McKinsey local, consultora boutique de IA, partner integrador que ya está dentro, etc.)*

---

*Plantilla generada per ADR-027. **NO pegar este archivo como contexto al invocar Skills 01-03.** Solo se abre cuando se invoca Skill 04 (PrepLlamada) y Skill 05 (Reporte de Oportunidades).*
