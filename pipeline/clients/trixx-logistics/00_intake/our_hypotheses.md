---
file_type: our_hypotheses
adr: ADR-027
slice: judgment (3) — hypotheses + people-judgments + Nexostrat-side constraints
read_by: [skill-04-discovery-meeting, skill-05-opportunity-report]
sealed_during: [skill-01-company-analyst, skill-02-industry-analyst, skill-03-competitor-analyst]
companion: research_input.md
filled: 2026-05-19
filled_by: ricardo + claude (founder)
---

# Our Hypotheses — `trixx-logistics`

> **Qué es esto:** lo que **creemos / intuimos / asumimos** sobre la empresa, sus dolores, su decisor, su tono.
> **Quién lo lee:** Skills 04 (PrepLlamada) y 05 (Reporte de Oportunidades). **NUNCA Skills 01-03.**
> **Por qué sellar durante research:** ADR-027 — si Skills 01-03 leyeran esto, sus salidas estarían contaminadas por nuestras hipótesis y perderíamos la capacidad de comparar **"lo que esperábamos vs lo que la investigación encontró"** en la síntesis.
> **Disciplina del operador:** al invocar `Analiza <slug>` (Skill 01) y los siguientes Skills 02 y 03, **NO** pegar el contenido de este archivo en el contexto. Pasarlo solo a partir de Skill 04.

---

## 1. Hipótesis sobre el dolor del cliente

- **Qué creemos que les duele:**
  - **Reforma Aduanera 2026** (vigor 1-ene-2026) — responsabilidad solidaria del agente aduanal + multas Carta Porte ($850 – $53,650 MXN + cárcel 3-6 años por contrabando presunto). 24 años de operación = procesos legados que probablemente no están al día con la nueva exigencia documental. Esto convierte IA aduanera de "lujo" a "seguro de operación."
  - **Visibilidad cross-border fragmentada.** 5 sedes (Guadalajara, Tijuana, CDMX-Vallejo, Vernon CA, San Diego CA) + operación bilingüe es-zh + cliente directo USA-MX → muy probable que tracking, estatus de cruce, y comunicación con el cliente sean manuales (WhatsApp + email + Excel).
  - **Andrea ya nombró "automatizaciones y más."** El "más" probablemente apunta a back-office (cotizaciones, facturación, conciliación, reporting) más que a operación core.

- **Por qué creemos que están abiertos a hablar AHORA:** Andrea verbalizó *"estamos muy atrás en programas y tecnología"* sin que nadie le preguntara — auto-percepción dolorosa explícita. Probablemente catalizada por (a) ver Nuvocargo / competidores digitales tomando market share visible, (b) presión silenciosa de la Reforma 2026, (c) el "más" sugiere que algo específico ya les pegó.

- **Qué problema NO se ha resuelto antes:** hipótesis — no han trabajado con consultor de IA serio. La señal "estamos muy atrás" sugiere que cualquier intento previo (probablemente un ERP genérico o paquete contable mexicano tipo CONTPAQi) no resolvió la realidad cross-border ni la capa documental aduanal.

## 2. Hipótesis sobre el decisor

- **Andrea es influenciadora, NO decisora.** Es la puerta caliente vía Sofía, pero el dueño (Hector Leyva) firma cheques. Su rol específico aún no confirmado — probablemente operativo o administrativo dado que es la que contacta a un externo sin convocar al "tío" en el primer mensaje.
- **Decisor final: Hector Leyva.** "Tío" de Andrea en sentido tijuanense (a confirmar si sangre). 24 años fundando + manteniendo la empresa = perfil dueño-operador clásico, edad probable 50-65, pragmático, decide por relación + ROI tangible, NO por tecnología abstracta.
- **Presión interna que podría sentir Andrea:** ser la voz "joven/digital" dentro de una compañía donde la madre + el tío representan la generación previa. Probablemente le tocó ya argumentar "necesitamos modernizarnos" y busca un aliado externo que respalde su caso.
- **Sofisticación tecnológica esperada del contacto:** **[x] medio** — Andrea usa WhatsApp con fluidez, supo identificar "automatizaciones" como categoría, pero el "muy atrás" sugiere que no maneja vocabulario técnico profundo (no dijo "AI", "ML", "RPA"). Hector probablemente **bajo** en términos digitales pero **alto** en términos operativos aduaneros.

## 3. Presupuesto y disposición a pagar (estimado)

- **Señales observadas:** 24 años de operación + 5 sedes (incluida sede US en Vernon CA + San Diego CA) + USDOT activo + flota propia 12 power units + 571,370 millas 2024 = ingresos estimados USD 3-8M anuales (típico para freight forwarder + brokerage MX-USA de ese tamaño). 0 crashes 24m + OOS rates buenos = operación financieramente sana. Patente aduanal (si la tienen) = USD 200K-500K de capital propio comprometido.
- **Rango que creemos pueden absorber:** **[x] 15-40K USD piloto** + retainer mensual **USD 2-5K** post-piloto. No 40K+ porque PyME familiar mexicana no firma cheques así sin track record previo. No <15K porque eso lee "esto es chiquito, no es prioridad."
- **Por qué:** Empresa con ingresos USD 3-8M típicamente reserva 0.5-2% para "experimentos" / consultoría = USD 15-160K/año. Un piloto bien escopeado entra ahí cómodo. Hector decidirá por **valor tangible demostrable**, no por presupuesto disponible — si no ve el ROI no firma ni USD 5K, si lo ve firma USD 30K.

## 4. Tono y zonas sensibles

- **Tono apropiado:** **[x] mixto: cercano + estratégico.** Andrea usó "Ricky", "platicar", signos de exclamación → cercano confirmado. Pero Hector + la naturaleza del negocio (cross-border, regulado, plata seria) → necesita gravitas estratégica en el contenido. NUNCA "técnico profundo" en primera reunión (feedback explícito de session 4).
- **Temas sensibles / NO tocar en primera reunión:**
  - **Patente aduanal:** si NO la tienen y operan vía patente de terceros (modelo común en TJ), preguntar directo puede leerse como acusación. Mejor sondear: *"¿manejan ustedes mismos la patente o trabajan con agente aduanal externo?"*
  - **Relación familiar Andrea-Hector:** asumir sangre y equivocarse es vergonzoso; preguntar directo es invasivo. Dejar que aflore.
  - **Comparación directa con Nuvocargo / "competencia digital":** Hector probablemente no quiere oír "te están comiendo el mercado." Mejor framing: *"el mercado está cambiando — ¿cómo lo están viendo ustedes?"*
  - **El sitio web actual:** tiene defectos visibles (placeholder fish-species, contador animado mal escalado). Mencionar = ofender. Dejar que el cliente lo mencione si quiere.
  - **"Por qué no han modernizado antes":** suena a juicio. Ricardo no es auditor.

- **Reacción esperada a "Hoja de Ruta de IA":** **[x] cauto.** Hector va a querer ver el reporte gratuito primero, validar que entendemos su negocio, y SOLO entonces escuchar el siguiente paso pagado. Empujar la Hoja de Ruta en primera reunión = cerrar la puerta.

## 5. Capacidades Nexostrat aplicables (hipótesis)

Capacidades que parecen aplicables al perfil Trixx:

- **[x] Análisis de procesos + automatización de tareas repetitivas** — el core probable: clasificación documental aduanera, generación Carta Porte, validación de pedimentos pre-cruce, reconciliación factura-pedimento-cruce.
- **[x] Agente WhatsApp + DM** — comunicación con clientes finales (status de embarque, ETA, documentación lista). Trixx opera bilingüe → agente bilingüe es-zh es diferenciador real.
- **[x] Dashboard sell-out** — adaptado a "dashboard operativo cross-border": cruces activos, tiempos por aduana, % docs incompletos, exposición por cliente. No "sell-out" en sentido retail pero la capacidad subyacente es la misma.
- **[ ] CRM + lead scoring** — Trixx no es lead-gen heavy. Probablemente NO es la primera entrada.
- **[ ] Pipeline de contenido** — no aplica al perfil B2B logística cross-border.

**Capacidades que CLARAMENTE NO podemos entregar hoy:**

- **NO** somos integradores SAP / Oracle / sistemas aduanales propietarios (CAAAREM, agentes aduanales certificados).
- **NO** podemos emitir/firmar pedimentos ni Carta Porte (eso requiere patente + responsabilidad solidaria — territorio del agente aduanal, no consultor).
- **NO** ofrecemos servicio operativo 24/7 (oncall tracking). Construimos el sistema; ellos lo operan.
- **NO** somos certificadores C-TPAT ni OEA.

## 6. Lo que esperamos que la reunión confirme o refute

> Esto lo lee Skill 05 al sintetizar el reporte final post-meeting.

1. **Que Hector es decisor único** (vs co-decisión con Andrea o la madre).
2. **Que NO han trabajado con consultor de IA antes** — si dicen que sí, cambia 100% el approach.
3. **Que el "más" en "automatizaciones y más" apunta a back-office / documentación aduanera**, no a marketing o ventas.
4. **Que NO son conscientes de Nuvocargo como amenaza directa** — si ya lo conocen y lo están evaluando, baja nuestra ventaja relacional.
5. **Que tienen patente aduanal propia** (vs operar vía terceros) — esto define el alcance de lo que podemos automatizar.
6. **Que la Reforma Aduanera 2026 ya les preocupa** — si nadie la ha mencionado internamente, somos los primeros en traerla = ganancia de credibilidad inmediata.
7. **Que Andrea tiene capacidad real de empujar el proyecto adentro**, no solo abrir la puerta y desaparecer.
8. **Que el volumen mensual de envíos northbound los pone en el rango Nuvocargo (150-350/mes)** — si están MUY por debajo, Nuvocargo no es competidor real y cambia el pitch.
9. **Que la operación es ~50/50 Chinese-import vs cross-border MX-US**, no 80%+ chino — si es 80% chino, el sector real es otro y Skill 02 quedó parcialmente desalineado.

## 7. Riesgos comerciales que vemos

- **Qué podría cerrar la oportunidad (lado cliente):**
  - **Hector decide "esto puede esperar"** — la Reforma 2026 ya entró en vigor y si no han colapsado todavía, podrían concluir "estamos bien." Mitigación: traer ejemplos concretos de multas Carta Porte aplicadas en los últimos 5 meses.
  - **Andrea pierde interés interno** — si Hector dice "ya veremos" sin compromiso, Andrea no va a empujar sola. Mitigación: dejar a Andrea con un win pequeño en mano (algo que le sirva a ELLA aunque Trixx no avance).
  - **Aparece un competidor con relación previa** — primo, sobrino, cuñado del dueño que "sabe de computadoras." Muy común en PyME familiar mexicana. Mitigación: distinguir nuestro alcance vs un IT-helper familiar.
  - **Decisión postpuesta por temporada alta de cruces** (sep-dic = pico cross-border). Si lo posponen "para enero" probablemente lo posponen para siempre.

- **Competidores con ventaja estructural aquí:**
  - **Nuvocargo** — ya identificado. USD 74M funding, AI-native, expandiendo activamente. Su debilidad: presencia física limitada en MX + modelo digital-first puede sentirse frío para Hector.
  - **Agente aduanal incumbente de Trixx** (si tienen uno) — relación de años, conoce sus pedimentos, probablemente intenta retener cualquier nueva inversión en tecnología "para mantenerlo dentro de la familia operativa." Esta es la competencia silenciosa real.
  - **Un sobrino/familiar técnico** ya mencionado arriba.
  - **NO competimos** con: McKinsey/Bain (no agarran cuentas de USD 3-8M de ingresos), Deloitte/PwC México (no entran a piloto de USD 15-40K), consultoras boutique de IA en CDMX (no tienen el componente relacional Tijuana).

---

*Plantilla generada per ADR-027. **NO pegar este archivo como contexto al invocar Skills 01-03.** Solo se abre cuando se invoca Skill 04 (PrepLlamada) y Skill 05 (Reporte de Oportunidades).*
