---
name: discovery-meeting
description: |
  Guión de Reunión de Descubrimiento — Nexostrat. Genera el guión completo para la reunión de exploración de 60 minutos: apertura con credibilidad instantánea, áreas de mayor potencial IA priorizadas, guión de preguntas por área con seguimiento (Operaciones, Ventas/CRM, Marketing, Finanzas, RRHH, Atención al Cliente, Logística), señales de oportunidad, manejo de objeciones, zonas sensibles, 10 ítems a documentar y cierre. Output: .docx confidencial para Ricardo.

  INPUT REQUERIDO: Los 3 reportes .md de company-analyst + industry-analyst + competitor-analyst. Si alguno falta, produce un mensaje claro indicando qué falta y por qué es necesario.

  Activar SIEMPRE ante: "guión de reunión", "prepárame para la reunión", "script de descubrimiento", "quiero ir preparado a la reunión", "guión para la llamada", "siguiente paso después del análisis", "prepara la llamada de exploración", o cuando el usuario comparte los .md de los skills anteriores y pide el guión. Ante la duda, activar.
---

# Discovery Meeting Script — Guión de Reunión de Descubrimiento

**Uso:** Interno — solo Ricardo
**Input:** Reportes .md de company-analyst + industry-analyst + competitor-analyst
**Output:** `[EmpresaCamelCase]_GuionReunion_YYYYMMDD.md` + `.docx`
**Propósito:** Que Ricardo llegue siendo el experto más preparado en la sala

---

## REGLA ANTI-ALUCINACIÓN

Todo dato específico en el guión (cifras, nombres, tecnologías, fechas) debe tener fuente en los 3 reportes de input. Si un dato no apareció en los reportes, márcalo como hipótesis: "Es probable que..." o "Vale la pena explorar si...". Nunca inventes datos de la empresa ni del sector.

---

## SETUP — Destino de outputs

**Convención canónica (per spec §7).** Cuando se ejecuta dentro del pipeline de un cliente, los outputs van a:

```
pipeline/clients/<slug>/04_meeting_script/runs/<YYYY-MM-DD_HHMM>_mode-a/
├── final_report.md      ← el guión completo (este skill)
├── final_report.docx    ← versión Word con cajas de color (generada por scripts/generate_docx.py)
└── notes.md             ← opcional: juicio cualitativo de Ricardo post-reunión (útil para iteración de prompts)
```

Para este skill, `<stage>` = `04_meeting_script` (corresponde a `pipeline/clients/_template/04_meeting_script/`).

**Inputs requeridos:** los 3 reportes .md de company-analyst + industry-analyst + competitor-analyst del mismo cliente. Típicamente ubicados en `pipeline/clients/<slug>/{01_company_analysis,02_industry_analysis,03_competitor_analysis}/runs/<RUN_ANTERIOR>/final_report.md`. El skill valida explícitamente la presencia de los 3 antes de generar el guión (ver PASO 0 abajo).

**Confidencialidad:** este guión es para uso interno exclusivo de Ricardo. NUNCA compartir con el prospecto. El renderer de DOCX agrega un marcador "CONFIDENCIAL" en la portada y el footer.

**Invocación standalone (fuera del pipeline):** guardar en el directorio de trabajo actual usando `[EmpresaCamelCase]_GuionReunion_YYYYMMDD.md/.docx` (ver PASO 4 abajo).

**Captura de versión:** el SHA del commit Git al momento del run identifica la versión exacta del prompt usado (per ADR-022).

---

## PASO 0 — VALIDAR LOS TRES INPUTS

Antes de hacer cualquier otra cosa, confirma que tienes exactamente estos 3 archivos .md:

- **company-analyst**: archivo tipo `*_AnalisisCompania_*.md` — perfil de la empresa prospecto
- **industry-analyst**: archivo tipo `*_CO_*.md` sobre el sector de la empresa
- **competitor-analyst**: archivo tipo `*_Competencia_CO_*.md` — análisis competitivo

Búscalos en el directorio de trabajo y en los paths proporcionados por el usuario.

Si falta alguno, NO generes el guión. Responde:

```
⚠️ Para generar el Guión de Reunión faltan los siguientes inputs:

❌ [Nombre del reporte faltante] — skill: [skill que lo genera]
   Por qué es necesario: [razón específica — no genérica]

✅ [Reporte disponible] — encontrado en [path]

Genera el(los) reporte(s) faltante(s) y vuelve a ejecutar este skill.
```

---

## PASO 1 — EXTRAER INTELIGENCIA

Lee los 3 reportes y extrae:

**Del company-analyst:**
- Nombre, NIT, ciudad, sector CIIU
- Ingresos 2024 (COP + USD), empleados, tendencia financiera
- Productos/servicios y clientes objetivo
- Madurez digital 1-5 con evidencias
- Debilidades y amenazas del FODA
- Quick Wins sugeridos, señales de alerta
- Sistemas tecnológicos mencionados (ERP, CRM, etc.)

**Del industry-analyst:**
- Tamaño de mercado y CAGR
- % adopción de IA en el sector y herramientas más usadas
- Disrupciones inminentes
- Ventana de oportunidad antes de que IA sea commodity
- Procesos del sector con mayor ROI documentado de IA

**Del competitor-analyst:**
- Top 3 competidores más peligrosos
- Nivel de adopción de IA de cada competidor vs. el prospecto
- Brechas que el prospecto tiene vs. la competencia
- Señales de punto ciego identificadas

---

## PASO 2 — PRIORIZAR ÁREAS DE IMPACTO IA

Clasifica cada área según evidencia real en los 3 reportes. No uses la misma priorización para todas las empresas.

**Áreas a evaluar:**
Operaciones · Ventas/CRM · Marketing · Finanzas · RRHH · Atención al Cliente · Logística

**Criterios:**
- ¿Hay evidencia en los reportes de que esta área es un cuello de botella?
- ¿La competencia usa IA aquí y el prospecto no?
- ¿Hay procesos manuales documentados en esta área?
- ¿El industry-analyst documenta ROI real de IA en esta área?

**Notación:** ●●● = Alta (5+ preguntas) · ●● = Media (3 preguntas) · ● = Baja (1 pregunta o excluir)

Incluye TODAS las áreas con ●● o superior. No hay límite.

---

## PASO 3 — GENERAR EL GUIÓN

Sigue el template de abajo exactamente. Rellena con contenido específico de la empresa: nombres reales, cifras reales, frases que suenen naturales en conversación. Cada pregunta debe poder decirse en voz alta sin sonar rara.

Usa las líneas `>` (blockquotes) exactamente como aparecen en el template — el generador de .docx las convierte en cajas de color especiales (verde para apertura, naranja para zonas sensibles, morado para timing, azul para notas).

---

## TEMPLATE DEL GUIÓN

El template completo está a continuación. Reemplaza TODOS los corchetes `[...]` con contenido específico de la empresa.

```
# Guión de Reunión de Descubrimiento: [Nombre Empresa]
**[Ciudad] · [Sector] · [Fecha]**
**CONFIDENCIAL — Solo para uso de Ricardo · Nexostrat**

---

## SECCIÓN 1: CONTEXTO RÁPIDO

### La empresa en 90 segundos
[3-4 oraciones en presente, lenguaje conversacional. Ricardo debe poder recitar esto sin leer el documento.]

### El sector en 30 segundos
[2-3 oraciones: tamaño, qué está pasando con IA en el sector, ventana de oportunidad.]

### Posición competitiva
[2-3 oraciones: cuál es la brecha más crítica entre esta empresa y sus competidores en IA/tecnología.]

### Indicadores clave
| Indicador | Dato | Fuente |
|-----------|------|--------|
| Ingresos 2024 | COP $XX (~USD $XX) | Supersociedades |
| Empleados | ~XX | [fuente] |
| Madurez digital | X/5 | company-analyst |
| Tendencia financiera | [creciendo/plana/cayendo X%] | Supersociedades |
| Sector — adopción IA | XX% de empresas | industry-analyst |
| Competidor con más IA | [nombre] — [herramienta específica] | competitor-analyst |

---

> 🟢 **APERTURA CON CREDIBILIDAD INSTANTÁNEA**
>
> Menciona uno de estos en los primeros 2 minutos. No los leas — di alguno naturalmente.
>
> **Credencial 1:** [Dato específico y concreto que demuestra que hiciste la tarea. No genérico: "vi que sus ingresos cayeron X% el año pasado — interesante dado que el sector creció X%."]
>
> **Credencial 2:** [Segundo dato sobre sector o competidor: "en su sector solo el X% de empresas tiene Y implementado — todavía hay una ventana."]
>
> **Pregunta gancho:** "[Pregunta específica que demuestra preparación. No retórica. No genérica. Algo que la empresa no espera que preguntes.]"
>
> *Por qué importa: Los primeros 2 minutos determinan si eres un vendedor o un par. Una credencial específica activa reciprocidad — quieren darte información a cambio.*

---

## SECCIÓN 2: OBJETIVO DE LA REUNIÓN

**Lo que queremos lograr:**
Entender cómo opera la empresa hoy, identificar los 3-5 procesos con mayor potencial de impacto con IA, y evaluar si hay voluntad de cambio. No ventas. Diagnóstico.

**Cómo sabemos que la reunión fue exitosa:**
- [ ] Identificamos al menos 3 áreas con procesos manuales costosos o dolorosos
- [ ] El interlocutor compartió al menos una cifra o frustración concreta
- [ ] Establecimos un próximo paso con fecha

**El estado ideal al minuto 55:**
El prospecto está preguntando cuándo puede ver el reporte. No empujamos — están jalando.

---

## SECCIÓN 3: ÁREAS DE MAYOR POTENCIAL IA

[Para cada área ●●● — repite este bloque]
### [●●●] [Nombre del Área]
**Por qué alta prioridad para ESTA empresa:** [1-2 oraciones basadas en evidencia de los reportes]
**Evidencia:** [Dato o señal específica de los 3 reportes]
**Benchmark del sector:** [ROI o caso documentado en industry-analyst, si existe]

[Para cada área ●● — repite este bloque más corto]
### [●●] [Nombre del Área]
**Por qué media prioridad:** [1 oración]
**Hipótesis a confirmar:** [Qué necesitan decirte para subir esta área a ●●●]

---

## SECCIÓN 4: GUIÓN DE PREGUNTAS

> ℹ️ **Cómo usar esta sección**
>
> Orden sugerido, no obligatorio. Si el prospecto abre una puerta, entra por ahí. El objetivo no es hacer todas las preguntas — es detectar dolor real y cuantificarlo.
>
> Checkpoint cada 7-8 minutos: ¿estás cubriendo suficientes áreas? Si llevas 20 min en un área sin dolor concreto, avanza.

---

[Para cada área ●●● — repite este bloque completo]
### ÁREA: [Nombre] (●●●)

**Contexto (no decir en voz alta):** [Por qué preguntar esto aquí — basado en los reportes]

**Apertura:** *"[Pregunta conversacional, sin sí/no, que invite a contar una historia]"*

**Si hay apertura — profundizar:** *"[Primera pregunta de seguimiento]"*

**Si hay dolor real — cuantificar:** *"[Pregunta para poner número: horas, personas, costos, errores]"*

**Si preguntan por soluciones:** *"[Solo si el prospecto lo pide: pregunta que los lleva a imaginar el futuro]"*

**Señal para avanzar:** [Qué escuchar para saber que tienes suficiente]

**Señal para quedarse más:** [Qué escuchar para saber que hay oportunidad real]

> ⚠️ **ZONA SENSIBLE: [Tema]**
>
> [1-2 oraciones sobre la sensibilidad basada en los reportes. Las zonas sensibles suelen ser donde hay más dolor y más oportunidad.]
>
> **Cómo acercarse:** [Estrategia concreta. Ej: "Enmarca en eficiencia, no en inversión. Si ellos sacan el tema, síguelos — es la señal de que quieren hablar de ello."]

[Para cada área ●● — repite este bloque corto]
### ÁREA: [Nombre] (●●)

**Contexto:** [Por qué preguntar esto — 1 oración]

**Apertura:** *"[Pregunta de apertura]"*

**Cuantificar:** *"[Si hay apertura: pregunta de cuantificación]"*

**Señal para avanzar:** [Cuándo moverse]

---

## SECCIÓN 5: SEÑALES DE OPORTUNIDAD

| Lo que dirán | Qué significa para IA | Cómo profundizar |
|-------------|----------------------|-----------------|
| "Hacemos eso manualmente / en Excel" | Automatización, RPA, OCR | "¿Cuántas personas? ¿Con qué frecuencia? ¿Qué pasa cuando alguien falla?" |
| "Nos toma mucho tiempo [proceso]" | Cuello de botella procesable | "¿Pueden cuantificar cuánto? ¿Qué pasa si se atrasa?" |
| "Siempre tenemos errores en [X]" | IA de validación y alertas | "¿Qué impacto tienen esos errores? ¿Se detectan rápido o tarde?" |
| "No tenemos cómo saber si [X]" | Analytics, BI, IA predictiva | "¿Qué decisión tomarían diferente si pudieran saber eso?" |
| "Mi equipo pasa tiempo buscando..." | Knowledge management, búsqueda IA | "¿Buscando qué — documentos, correos, historial de clientes?" |
| "El cliente siempre llama por lo mismo" | Chatbot, autoservicio, FAQ inteligente | "¿Con qué frecuencia? ¿Tienen métrica de satisfacción?" |
| "Nunca sabemos qué va a pasar con [X]" | Forecasting, IA predictiva | "¿Qué impacto tiene no poder anticiparse? ¿Tienen data histórica?" |
| "Nuestro [sistema] no habla con [otro]" | Integración, middleware, automatización | "¿Cuántos sistemas tienen sin integrar?" |
| [Señal específica del sector basada en industry-analyst] | [Significado sector-específico] | [Profundización contextual] |
| [Señal específica de esta empresa basada en company-analyst] | [Significado para su situación] | [Profundización específica] |

---

## SECCIÓN 6: SEÑALES DE ALERTA Y MANEJO DE OBJECIONES

| Objeción | Por qué la dicen | Cómo responder |
|----------|-----------------|----------------|
| "No estamos listos para IA" | Perciben IA como complejo y lejano | "No estamos hablando de ciencia ficción. Estamos hablando de automatizar [proceso concreto que mencionaron]. ¿Qué tan listo tiene que estar un proceso para merecer ser más eficiente?" |
| "No tenemos presupuesto" | No ven el ROI; el dolor no es suficiente | "Entendido. Por eso hacemos primero el diagnóstico — para que puedan ver exactamente qué ahorro se podría generar. ¿Tendría sentido verlo antes de hablar de inversión?" |
| "Ya lo intentamos y no funcionó" | Experiencia negativa con tecnología | "¿Pueden contarme qué pasó? Eso nos ayuda mucho a no repetir el mismo error." |
| "Nuestro negocio es muy particular" | Miedo a soluciones genéricas | "Es exactamente por eso que hacemos el diagnóstico antes de proponer nada. Cuéntenme qué hace que [proceso] sea particular." |
| "Eso lo maneja sistemas / TI" | No son el decisor | "Tiene sentido. ¿Podríamos incluirlos en el siguiente paso? El diagnóstico les dará argumentos técnicos y de negocio para presentar internamente." |
| [Objeción sector-específica del industry-analyst] | [Razón contextual] | [Respuesta adaptada] |
| [Objeción empresa-específica basada en perfil] | [Razón basada en señales de los reportes] | [Respuesta que toca su punto de dolor] |

---

## SECCIÓN 7: QUÉ DOCUMENTAR

Estos 10 ítems son obligatorios para escribir el Reporte Diagnóstico. Sin ellos, el reporte no puede ser concreto ni cuantificado.

1. **[Ítem más crítico para esta empresa]** — *[Por qué es prioritario — específico, no genérico]*
2. **[Ítem]** — *[Por qué]*
3. **[Ítem]** — *[Por qué]*
4. **[Ítem]** — *[Por qué]*
5. **[Ítem]** — *[Por qué]*
6. **[Ítem]** — *[Por qué]*
7. **[Ítem]** — *[Por qué]*
8. **[Ítem]** — *[Por qué]*
9. **[Ítem]** — *[Por qué]*
10. **Señal de disposición de inversión** — *"¿Si identificamos 3 áreas de impacto, qué rango de inversión anual tendría sentido para empezar?" Sin esto no podemos dimensionar la propuesta.*

---

## SECCIÓN 8: CIERRE Y PRÓXIMOS PASOS

### Guión de cierre (verbatim o adaptado)

*"Muchas gracias por el tiempo y la apertura — quedé con una imagen mucho más clara de cómo operan y dónde pueden estar las mayores oportunidades. Lo que haríamos ahora es consolidar esto en un Reporte Diagnóstico: un documento que identifica las [3-5] áreas de mayor impacto, el caso de ROI estimado para cada una, y los primeros pasos concretos. Lo típico es tenerlo listo en [X días]. ¿Queda bien si lo enviamos el [día específico]?"*

### Qué prometer
- El Reporte Diagnóstico en [X días — ser específico]
- Confidencialidad total
- Sin compromiso hasta que vean el reporte

### Qué NO prometer
- Precios específicos (van en la propuesta, después del diagnóstico)
- Timelines de implementación (dependen del diagnóstico)
- Casos de clientes específicos sin permiso explícito

### Si preguntan cuánto cuesta
*"Es exactamente lo que el diagnóstico nos va a ayudar a responder con datos. Trabajamos con empresas de tu tamaño con modelos desde proyectos puntuales hasta programas anuales. El diagnóstico nos dirá cuál tiene más sentido para ustedes."*

---

> ⏱️ **DISTRIBUCIÓN DE TIEMPO (60 min)**
>
> **0:00 – 0:05 | RAPPORT (5 min)**
> Preséntate brevemente. Menciona una credencial específica (ver Sección 1). Deja hablar. Objetivo: bajar la guardia.
>
> **0:05 – 0:15 | CONTEXTO DE ELLOS (10 min)**
> Apertura general: *"Antes de entrar en temas específicos, ¿me pueden contar cómo ven el momento actual de la empresa — qué están priorizando este año?"* Escucha. Toma notas. No interrumpas.
>
> **0:15 – 0:50 | PREGUNTAS POR ÁREA (35 min)**
> Prioriza las áreas ●●●. Sigue el hilo. Checkpoint cada 7-8 min: ¿estás cubriendo suficientes áreas?
> Minuto 30 — si no has cubierto la 2ª área más crítica, redirige: *"Cambiando de tema, ¿cómo manejan [área]?"*
>
> **0:50 – 0:55 | DEMO / PROPUESTA (5 min)**
> Solo si el prospecto pregunta. Muestra resultado, no proceso. *"En una empresa similar esto representó [resultado concreto]. ¿Algo así tendría sentido para ustedes?"*
>
> **0:55 – 1:00 | CIERRE (5 min)**
> Usa el guión de la Sección 8. Confirma fecha y formato del próximo paso.
```

---

## PASO 4 — GENERAR EL DOCX

Con el .md completo, ejecuta el renderer local (desde la raíz del repo `/srv/Nexostrat/`):

```bash
pip install python-docx --break-system-packages -q
python3 skills/06_discovery_meeting/scripts/generate_docx.py <ruta_al_md> <ruta_output_docx>
```

El renderer aplica colores de caja específicos al guión (verde para apertura, naranja para zonas sensibles, morado para timing, azul para notas). Convenciones de nombre (ver § PASO 0 — Setup arriba):
- **Dentro del pipeline:** `final_report.md` + `final_report.docx` (canónico per spec §7)
- **Standalone:** `[EmpresaCamelCase]_GuionReunion_YYYYMMDD.md/.docx`

---

## NOTAS OPERATIVAS

**Las zonas sensibles son oportunidades.** Una empresa con pérdidas tiene más presión para cambiar. Un cambio de ownership abre ventanas de transformación. El guión acerca a Ricardo a estos temas con cuidado — no los evita.

**El guión no es un script rígido.** Es navegación. La reunión la conduce el prospecto. Ricardo necesita saber a dónde quiere llegar.

**Las preguntas deben sonar naturales.** Di cada pregunta en voz alta mientras la generas. Si suena invasiva, reescríbela.

**El objetivo no es cubrir todo.** Es identificar 2-3 áreas de dolor real con datos cuantificables.
