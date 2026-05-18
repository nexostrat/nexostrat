---
name: discovery-meeting
description: |
  Guía de Preparación para Primera Llamada — Nexostrat. Genera documento pre-llamada (.docx) para que Ricardo llegue sabiendo exactamente qué preguntar. Sin agenda de ventas. Estructura: resumen ejecutivo, terminología del sector, contexto competitivo, preguntas por área (almacenamiento, contabilidad, marketing, ventas, logística, licencias, seguridad), preguntas game-changer, objetivos y red flags. Output: [Empresa]_PrepLlamada_YYYYMMDD.docx.

  INPUTS REQUERIDOS: company-analyst + industry-analyst + competitor-analyst. Activar SIEMPRE ante: "prepárame para la llamada", "primera llamada con [empresa]", "quiero ir preparado", "guía para la llamada", "qué preguntar en la reunión", "siguiente paso después del análisis", o cuando el usuario comparte los reportes .md y pide preparación. Ante la duda, activar.
---

# Guía de Preparación para Primera Llamada

**Uso:** Interno — solo Ricardo  
**Inputs obligatorios:** Reportes .md de company-analyst + industry-analyst + competitor-analyst  
**Output:** `[EmpresaCamelCase]_PrepLlamada_YYYYMMDD.docx`  
**Propósito:** Que Ricardo llegue a la primera llamada siendo el consultor más preparado de la sala — y que el cliente sienta que lo conocen antes de que abra la boca

---

## SISTEMA DE CONFIANZA DE DATOS — REGLA ANTI-ALUCINACIÓN

### Etiquetas obligatorias

Este documento se construye 100% a partir de los 3 inputs obligatorios. Aplica estas etiquetas a todos los datos que aparezcan en el documento:

| Etiqueta | Significado | Cuándo usarla |
|---|---|---|
| ✅ | Verificado | Dato presente en los inputs con fuente citada |
| ⚠️ | Estimado | Inferido a partir de los inputs, no afirmado directamente |
| ❓ | A confirmar | No encontrado en ningún input — preguntar en la llamada |

**Formato obligatorio en la tabla de "Números clave":**
- La columna **Fuente** es obligatoria. Nunca dejarla vacía.
- Si el dato viene de Supersociedades → `✅ Supersociedades 2024`
- Si se infirió de LinkedIn → `⚠️ LinkedIn (estimado)`
- Si no está en ningún input → `❓ Preguntar en llamada`

### Reglas sin excepción

1. **Solo datos de los inputs.** Este skill NO hace búsquedas web nuevas. Todo dato viene de los 3 reportes de input. Si no está en los inputs, no está en la PrepLlamada.
2. **Hipótesis identificadas:** Si el documento incluye una inferencia no respaldada directamente por datos, marcarla con `⚠️ Hipótesis a validar con el cliente:`.
3. **"¿Por qué explorar esto?"** Cada justificación de área debe citar la evidencia específica del input que la motiva. Si no hay evidencia específica, escribir: `⚠️ Esta área se incluye por protocolo estándar — no hay evidencia específica en los reportes que la señale como prioridad para esta empresa.`
4. **Prohibido extrapolar:** No concluir que la empresa tiene un problema que no fue observado en los inputs. Las señales de oportunidad se basan en evidencia, no en suposiciones del sector.
5. **Datos de más de 2 años:** añadir `⚠️ (dato de [año] — verificar vigencia en la llamada)`.

---

## PASO 0 — Validar los inputs

Confirma que tienes exactamente estos 3 archivos .md:

- **company-analyst**: archivo tipo `*_AnalisisCompania_*.md`
- **industry-analyst**: archivo tipo `*_CO_*.md` o `*_MX_*.md` (sin "Competencia" ni "AnalisisCompania" en el nombre)
- **competitor-analyst**: archivo tipo `*_Competencia_CO_*.md` o `*_Competencia_MX_*.md`

Si falta alguno, NO generes el documento. Responde:

```
⚠️ Para generar la Guía de Preparación faltan los siguientes inputs:

❌ [Reporte faltante] — skill que lo genera: [skill name]
✅ [Reporte disponible] — encontrado en [path]

Genera el(los) reporte(s) faltante(s) con los skills correspondientes y vuelve a ejecutar.
```

---

## PASO 1 — Extraer inteligencia de los 3 reportes

Lee los 3 archivos y organiza la siguiente información:

**Del company-analyst:**
- Nombre, NIT/RFC, ciudad, sector, país (Colombia/México)
- Ingresos, empleados, tendencia financiera
- Productos y servicios principales
- Tecnología actual visible (ERP, CRM, herramientas mencionadas)
- Debilidades y señales de alerta del FODA
- Madurez digital (puntaje y evidencias concretas)
- Quick Wins sugeridos

**Del industry-analyst:**
- Jerga y términos técnicos del sector (los que usa la industria, no los nuestros)
- % de adopción de IA en el sector
- Procesos donde la IA tiene mayor ROI documentado
- Presiones competitivas actuales del sector

**Del competitor-analyst:**
- Top 3 competidores más relevantes para este cliente
- Qué tecnología/IA tienen los competidores que este cliente no tiene
- Brechas específicas identificadas

---

## PASO 2 — Generar el documento

Escribe el contenido completo siguiendo exactamente el template de abajo. Cada sección debe estar llena con datos reales de esta empresa — no texto genérico. Si un dato no está disponible en los inputs, márcalo claramente.

---

## TEMPLATE DEL DOCUMENTO

```
# Guía de Preparación: Primera Llamada con [Nombre Empresa]
**Preparado por Nexostrat — CONFIDENCIAL — Solo para Ricardo**  
**Fecha: [fecha] · Sector: [sector] · País: [Colombia/México]**

---

## 1. LA EMPRESA EN 5 MINUTOS

### Quiénes son
[2-3 oraciones en lenguaje conversacional. Quiénes son, qué venden, a quién, cuánto llevan en el mercado. Ricardo debe poder recitar esto sin leer el documento.]

### Números clave
| Indicador | Dato | Fuente |
|-----------|------|--------|
| Ingresos anuales | [dato en COP/MXN + USD aprox] | [fuente] |
| Empleados | [dato] | [fuente] |
| Años en el mercado | [dato] | [fuente] |
| Madurez digital | [X]/5 | company-analyst |
| Tendencia financiera | [creciendo / plana / cayendo] | [fuente] |

### Estado tecnológico conocido
[Qué herramientas, sistemas o software se identificaron en la investigación. Si no se encontró nada → "No se identificaron herramientas tecnológicas públicamente. Preguntar en la llamada."]

### Señales de alerta previas
[Máximo 3 señales de alerta del company-analyst que Ricardo debe tener en mente. Si no hay → "Sin señales de alerta identificadas."]

---

## 2. EL SECTOR EN 3 MINUTOS

### Para sonar como experto — terminología clave
[5 términos o conceptos que usa esta industria que Ricardo debe conocer antes de la llamada. Definición corta de cada uno en lenguaje de negocio, no técnico.]

- **[Término 1]:** [Definición en 1 línea]
- **[Término 2]:** [Definición en 1 línea]
- **[Término 3]:** [Definición en 1 línea]
- **[Término 4]:** [Definición en 1 línea]
- **[Término 5]:** [Definición en 1 línea]

### Lo que está pasando en el sector ahora
[2-3 oraciones: tendencias más relevantes del sector que pueden generar conversación con el cliente. Incluir cifras del industry-analyst si disponibles.]

### IA en este sector
[1-2 oraciones sobre el estado de adopción de IA en el sector. Qué % de empresas lo está usando. Qué tipo de soluciones son más comunes.]

---

## 3. POSICIÓN COMPETITIVA (2 minutos)

### Sus principales competidores
| Competidor | Ventaja principal | Adopción de IA | Debilidad |
|------------|------------------|----------------|-----------|
| [Comp 1] | [ventaja] | [sí/no + qué] | [debilidad] |
| [Comp 2] | [ventaja] | [sí/no + qué] | [debilidad] |
| [Comp 3] | [ventaja] | [sí/no + qué] | [debilidad] |

### La brecha más crítica
[1-2 oraciones directas: cuál es la diferencia más importante entre este cliente y sus competidores en tecnología/IA. Esto es lo que puede generar urgencia en la llamada.]

---

## 4. GUÍA DE PREGUNTAS POR ÁREA

**Cómo usar esta sección:**  
El objetivo de esta llamada es escuchar y entender — no vender. Usa estas preguntas para explorar cómo opera la empresa hoy. Sigue el hilo de lo que el cliente abre: no hay que hacer todas las preguntas en orden.

Para cada área, la lógica de exploración es: ¿Qué tienen? → ¿Cuánto cuesta / cuánto tiempo toma? → ¿Qué no funciona bien?

---

### 4.1 Almacenamiento y gestión de información

**¿Por qué explorar esto?** [1 oración basada en evidencia del company-analyst o industry-analyst — ej: "La madurez digital de 2/5 sugiere que la información está repartida en silos."]

**Preguntas de apertura:**
- *"¿Dónde guardan la información del negocio? ¿Tienen un sistema central o está repartida en emails y Excel?"*
- *"Cuando alguien nuevo entra a la empresa, ¿cómo aprende qué hay que saber?"*

**Si hay apertura — profundizar:**
- *"¿Cuánto tiempo toma encontrar un documento o un contrato específico?"*
- *"¿Ha habido alguna vez un problema porque alguien no encontró algo importante a tiempo?"*

**Señal de oportunidad:** Si mencionan múltiples lugares donde guardan cosas (correo, WhatsApp, carpetas locales, Google Drive, USB) → oportunidad de knowledge management con IA.

---

### 4.2 Contabilidad y registros financieros

**¿Por qué explorar esto?** [1 oración basada en evidencia]

**Preguntas de apertura:**
- *"¿Tienen un sistema contable o de ERP? ¿Qué usan?"*
- *"¿Cómo es el proceso de facturación? ¿Es manual, automatizado, o mixto?"*

**Si hay apertura — profundizar:**
- *"¿Con qué frecuencia hacen el cierre contable? ¿Cuántas personas participan?"*
- *"¿Hay algún proceso que todavía se haga en Excel o en papel que les gustaría automatizar?"*

**Señal de oportunidad:** Procesos manuales de conciliación, cierres que toman días, múltiples personas haciendo trabajo que podría automatizarse.

---

### 4.3 Marketing

**¿Por qué explorar esto?** [1 oración basada en la presencia digital observada en company-analyst]

**Preguntas de apertura:**
- *"¿Cómo se enteran los nuevos clientes de ustedes? ¿Qué canal genera más leads hoy?"*
- *"¿Tienen alguna estrategia de marketing digital activa, o es más de referidos y boca a boca?"*

**Si hay apertura — profundizar:**
- *"¿Miden el costo de adquirir un cliente nuevo? ¿Saben qué campañas o canales funcionan mejor?"*
- *"¿Alguien se encarga del marketing de tiempo completo, o es algo que hace el dueño/gerente?"*

**Señal de oportunidad:** Marketing basado en intuición sin datos, sin métricas de costo por adquisición, dependencia total de referidos.

---

### 4.4 Ventas

**¿Por qué explorar esto?** [1 oración basada en evidencia — tipo de cliente, ciclo de venta estimado del sector]

**Preguntas de apertura:**
- *"¿Cómo manejan el seguimiento a prospectos? ¿Tienen CRM o es más por correo y agenda personal?"*
- *"¿Cuánto tiempo toma cerrar una venta típicamente, desde el primer contacto hasta el contrato?"*

**Si hay apertura — profundizar:**
- *"¿Saben en qué paso del proceso se pierden más prospectos?"*
- *"¿Cuántas oportunidades se quedan sin seguimiento por falta de tiempo?"*

**Señal de oportunidad:** Seguimiento manual a prospectos, sin visibilidad del pipeline, ventas perdidas por falta de seguimiento oportuno.

---

### 4.5 Logística y operaciones

**¿Por qué explorar esto?** [1 oración — incluir solo si el sector o company-analyst sugiere logística relevante. Si la empresa es de servicios puros y logística no aplica → omitir esta sección y anotarlo en el template]

**Preguntas de apertura:**
- *"¿Cómo manejan el inventario o los pedidos? ¿Es manual o tienen un sistema?"*
- *"¿Cuál es el proceso más lento o frustrante en sus operaciones del día a día?"*

**Si hay apertura — profundizar:**
- *"¿Con qué frecuencia tienen problemas de stock, retrasos en entregas, o errores en pedidos?"*
- *"¿Cuánto tiempo consume ese proceso al equipo por semana?"*

**Señal de oportunidad:** Inventario gestionado en Excel, retrasos frecuentes, errores manuales en pedidos o despachos.

---

### 4.6 Herramientas y licencias activas

**¿Por qué explorar esto?** Entender el ecosistema tecnológico real es fundamental para identificar dónde hay redundancias, dónde hay gaps, y qué podría automatizarse sin reemplazar sistemas que ya funcionan y ya se están pagando.

**Preguntas de apertura:**
- *"¿Qué software o herramientas usan actualmente? Por ejemplo: Microsoft 365, Google Workspace, algún ERP, CRM, Notion..."*
- *"¿Tienen herramientas que paguen pero que el equipo no usa bien o que estén subutilizadas?"*

**Si hay apertura — profundizar:**
- *"¿Cuánto pagan aproximadamente en licencias de software por mes?"*
- *"¿Hay alguna herramienta que les gustaría tener pero no han podido implementar?"*

**Lista de seguimiento — preguntar si no mencionaron espontáneamente:**
- Microsoft 365 / Google Workspace
- ERP: SAP, Siesa, World Office, Contpaq, Odoo, CONTPAQi...
- CRM: Salesforce, HubSpot, Zoho, Bitrix24...
- Comunicación: Slack, Teams, WhatsApp Business...
- IA: ChatGPT, Copilot, Gemini...

**Señal de oportunidad:** Microsoft 365 o Google Workspace subutilizados → hay automatizaciones posibles con herramientas que ya tienen y ya pagan.

---

### 4.7 Seguridad de información

**¿Por qué explorar esto?** En empresas con baja madurez digital, la seguridad suele ser el eslabón más débil — y a la vez un punto de entrada natural para hablar de buenas prácticas y sistematización.

**Preguntas de apertura:**
- *"¿Tienen alguna política de respaldo de información? ¿Dónde guardan los backups?"*
- *"¿Han tenido alguna vez un incidente de seguridad — pérdida de datos, acceso no autorizado, algo así?"*

**Si hay apertura — profundizar:**
- *"¿Cómo manejan el acceso a la información cuando alguien sale de la empresa?"*
- *"¿Usan contraseñas compartidas entre el equipo?"*

**Señal de oportunidad:** Sin política de backups, contraseñas compartidas, sin control de accesos → vulnerabilidad y oportunidad de sistematización.

---

## 5. PREGUNTAS DE GAME-CHANGER

Estas preguntas van después de explorar las áreas operativas. Su objetivo es entender la visión del cliente y encontrar el dolor más profundo — el que no aparece en ningún reporte.

*"Si pudiera resolver UN problema en su empresa con un chasquido de dedos, ¿cuál sería?"*

*"¿Qué proceso le quita más tiempo al equipo, el que más les duele en el día a día?"*

*"¿Hay algo que hoy hacen manualmente que saben que se podría hacer de otra manera, pero no han tenido tiempo de resolver?"*

*"¿Qué tiene que pasar en los próximos 12 meses para que consideren que este año fue exitoso?"*

*"Si su competidor más fuerte estuviera adoptando tecnología que ustedes no tienen todavía, ¿cómo lo sabrían?"*

---

## 6. OBJETIVOS DE LA LLAMADA

Ricardo debe colgar la llamada sabiendo:

- [ ] ¿Qué herramientas tecnológicas usan hoy? (ERP, CRM, productividad)
- [ ] ¿Cuál es el proceso más manual y costoso en tiempo o dinero?
- [ ] ¿Quién toma las decisiones de tecnología e inversión?
- [ ] ¿Hay urgencia real? ¿Algo los está quemando ahora mismo?
- [ ] ¿Cuál es su actitud frente a la IA? (curiosidad, escepticismo, entusiasmo, miedo)
- [ ] ¿Cuál es el rango de inversión que tendría sentido para ellos?
- [ ] ¿Qué áreas generaron más energía durante la conversación?

**Señal de éxito de la llamada:** El cliente pregunta cuándo va a recibir el análisis. No empujamos — están jalando.

---

## 7. RED FLAGS A MONITOREAR

[Para cada señal de alerta del company-analyst — incluir una versión adaptada para detectarla en conversación]

**Señales generales a tener en radar:**

- **"Ya intentamos tecnología y no funcionó"** → No rebatir. Preguntar qué pasó. Entender qué salió mal — ahí está la clave de lo que hay que hacer diferente.
- **"Nuestro negocio es muy particular, no creo que la IA aplique aquí"** → No contradecir. Pedir que describan la particularidad — en esa descripción suele estar la oportunidad.
- **"No tenemos presupuesto"** (antes de entender el valor) → No es objeción de dinero, es objeción de ROI no visible todavía.
- **"Eso lo maneja sistemas / TI"** → Identificar quién es el decisor real: *"¿Podríamos incluirlos en el siguiente paso?"*
- **El interlocutor no es el decisor** → Confirmarlo amablemente: *"¿Quién más estaría involucrado en tomar una decisión de este tipo?"*

**Señales específicas de esta empresa:**
[2-3 señales basadas en las alertas del company-analyst — si hay deuda alta, reseñas muy negativas, sector en declive, etc. Si no hay → "Sin señales de alerta específicas identificadas."]
```

---

## PASO 3 — Generar el DOCX

Con el markdown completo, ejecuta:

```bash
pip install python-docx --break-system-packages -q
python scripts/generate_docx.py [Empresa]_PrepLlamada_YYYYMMDD.md [Empresa]_PrepLlamada_YYYYMMDD.docx
```

---

## NOTAS OPERATIVAS

**El objetivo no es vender — es entender.** La primera llamada es de diagnóstico, no de propuesta. Cuanto más habla el cliente, mejor. Ricardo escucha, toma notas, y hace preguntas que lo llevan a revelar dolores reales.

**Sigue el hilo.** Este documento es una guía, no un script rígido. Si el cliente abre una puerta interesante, entra por ahí aunque no esté en la guía.

**Las preguntas deben sonar naturales.** Di cada pregunta en voz alta mientras la generas. Si suena a cuestionario, reescríbela hasta que suene como conversación.

**Un dolor cuantificado vale más que diez hipótesis.** Si el cliente dice "nos toma tiempo", preguntar "¿cuánto tiempo? ¿cuántas personas?" convierte una hipótesis en un caso de negocio.
