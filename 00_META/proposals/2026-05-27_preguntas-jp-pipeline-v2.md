# Preguntas para JP — Reunión 2026-05-28 [PARCIALMENTE CERRADA]

> Pipeline v2 — Lo que falta por definir antes de implementar
>
> **Reunión ocurrida:** 2026-05-28 07:05 PT (49 min). Transcripción + summary en `/srv/meetings/nexostrat/2026-05-28/2026-05-28_07-05_buyer-persona-trixx-logistic-pipeline/`.

---

## Resultado de la reunión 2026-05-28

**4 preguntas cerradas + 1 parcial + 9 quedan abiertas.**

| # | Pregunta | Estado | Respuesta JP |
|---|---|---|---|
| 1 | CRM herramienta | PARCIAL | Notion vs Odoo — Ricardo investiga Odoo (self-hosting + extensiones comunidad) antes de decidir. |
| 2 | Estructura del Word | CERRADA | DOCX/HTML de **10-15 páginas** + PPTX/HTML de **máximo 10 slides**. Balance exhaustividad vs lectura digerible. |
| 3 | Cifras concretas o rangos | CERRADA | Baseline mínimo **$3,000 USD** por proyecto. Sin cobro por horas. Margen de maniobra sano frente a solicitudes adicionales. |
| 4 | Catálogo de capacidades antes 1er cliente | ABIERTA | No se discutió. Sigue pendiente. |
| 5 | 6 fases Ciclo 2 — skills/humano/mezcla | ABIERTA | No se discutió. Sigue pendiente. |
| 6 | Qué cubre la garantía 1 mes | CERRADA | Opción A — solo bugs + ajustes menores. Features nuevos = proyecto independiente. |
| 7 | Garantía incluida o aparte | CERRADA | Opción A — incluida en el precio estándar. |
| 8 | Canales de captación | ABIERTA | Mención lateral a estrategia de contenido (podcast → IA → newsletter/LinkedIn/Twitter) pero canales de prospect-to-discovery no se decidieron. |
| 9 | Funnel CRM etapas | ABIERTA | Espera decisión Odoo vs Notion. |
| 10 | Plantillas seguimiento D+7/15/30/60/90 | ABIERTA | No se discutió. |
| 11 | Canal mensajes D+7..D+90 | ABIERTA | No se discutió. |
| 12 | Qué detiene la cadena de seguimiento | ABIERTA | No se discutió. |
| 13 | JP en el flujo (opcional/obligatorio) | ABIERTA-AJUSTE | Surge modelo nuevo: **tercerización con Neo** para proyectos que excedan el modelo ágil con IA — Nexostrat retiene rol comercial/estratégico, Neo ejecuta técnico, comisión. |
| 14 | "Cowork" nombre comercial | ABIERTA | No se discutió. Pero locked decisión transversal: evitar "bot"/"robot"; usar **"sistemas de consolidación de información"** o **"secretarios digitales"**. |

### Decisiones nuevas que no estaban en las 14 preguntas

- **Posicionamiento**: Nexostrat no vende "bots" ni "programación" — vende **consultoría completa** con fases de entendimiento, diseño, validación, construcción y pruebas. El baseline $3,000 USD refleja esa profundidad.
- **Tercerización con Neo** para proyectos fuera del scope ágil-con-IA (plataformas custom desde cero).
- **Facturación internacional**: USD legalmente vía la empresa de JP registrada en Panamá — **Consultores Butacos**.
- **Marketing de contenido**: grabar reuniones/podcast → IA extrae → newsletter + LinkedIn + Twitter (estrategia de única fuente, múltiples salidas).
- **Redes sociales**: reservar handles `nexostrat_` (guion bajo) en Instagram, Twitter, TikTok.
- **Buyer Persona Don Carlos**: JP ya consolidó las versiones de Ricardo + JP usando IA + generó video explicativo (`Cerrar_a_Don_Carlos.mp4`) — entregables consolidados disponibles.

### Tasks abiertas en tasks.json desde la reunión

`t-010` a `t-015` (auto-extraídas vía meetings pipeline): ajustar Skill 6 (JP), compartir versión nueva (JP), investigar Odoo (Ricardo), contactar Andrea (Ricardo), correr Skill 6 final Trixx (Ricardo), crear cuentas de redes con `nexostrat_` (Ricardo).

---

## Lo que ya cerramos (Ricardo + Claude, esta semana)

Tu HTML `pipeline-nexostrat-v2.html` está aprobado en la columna vertebral. Cinco decisiones quedaron tomadas con base en lo que dibujaste:

1. El Skill 6 produce dos documentos: un Word editable (`.docx`) y una presentación (`.pptx`).
2. El Word contiene el diagnóstico, la hoja de ruta y la propuesta, todo en un solo documento.
3. La presentación se proyecta en la reunión primero. El Word se envía al cierre de la reunión. No es regla rígida — habrá casos donde se entregue antes o durante.
4. El Skill 7 desaparece como entidad separada. Todo el contenido vive en el Word del Skill 6.
5. No hay artefacto intermedio entre Skill 5 (reporte interno) y Skill 6 (documentos cliente). La revisión es libre, iterativa entre Ricardo y la IA hasta llegar al documento final.

---

## Lo que falta por definir (14 preguntas)

Las 7 primeras son bloqueantes — sin tu respuesta no puedo arrancar la implementación del Skill 6. Las 7 restantes son importantes pero no bloquean el arranque técnico.

---

## Bloqueantes para arrancar implementación

### 1. ¿Qué CRM usamos?

En tu diagrama, el paso 2 dice "actualizar CRM" cuando llega un prospecto. No especificaste qué herramienta.

**Por qué te pregunto:** "CRM" puede ser muchas cosas con costos y complejidades muy distintas. La decisión define qué construimos y cuánto tiempo toma.

- [ ] Opción A — Baserow self-hosted (ya está planeado en otro doc nuestro; gratis; corremos el servidor nosotros; alineado con la decisión de no depender de SaaS de terceros)
- [ ] Opción B — Una herramienta externa que tú prefieras (HubSpot Free, Pipedrive, Folk, Attio) — cuéntame cuál y por qué
- [ ] Opción C — Empezamos sin CRM herramienta; usamos carpetas y un archivo de estado por cliente; cuando tengamos volumen migramos
- [ ] Opción D — Decide tú Ricardo

---

### 2. Estructura del Word del Skill 6

Tu diagrama dice que el Word tiene "diagnóstico, hoja de ruta y propuesta" pero no especifica cómo se organizan en secciones.

**Por qué te pregunto:** Sin estructura definida no puedo escribir el template del Skill 6.

En el spec original teníamos 4 secciones espejo:
1. Diagnóstico Operacional (lo que vimos del cliente)
2. Movimientos del Sector (qué está pasando en su industria)
3. Frentes de Oportunidad (qué se puede mejorar)
4. Próximos Pasos (mini-roadmap + invitación a la siguiente fase)

- [ ] Opción A — Mantenemos las 4 secciones originales y agregamos una sección 5 de Propuesta (con costos, tiempos, alcance)
- [ ] Opción B — Tú propones una estructura nueva (cuéntame cuál)
- [ ] Opción C — Dos documentos separados: un Word de Diagnóstico (4 secciones) y un Word de Propuesta + Hoja de Ruta aparte

---

### 3. ¿Las cifras en la propuesta son concretas o rangos?

Tu diagrama dice que el Word incluye la propuesta. La pregunta es si esa propuesta lleva números exactos o rangos cualitativos.

**Por qué te pregunto:** Cifras concretas requieren que sepamos exactamente qué podemos entregar y a qué precio. Rangos cualitativos ("inversión moderada · 4-6 semanas") son más fáciles de poner pero menos creíbles.

- [ ] Opción A — Cifras concretas siempre (USD X o COP X, con cronograma específico)
- [ ] Opción B — Rango cualitativo en el primer Word; cifras concretas cuando arranquemos Ciclo 2
- [ ] Opción C — Caso por caso según el cliente

---

### 4. ¿Necesitamos el catálogo de capacidades antes del primer cliente?

Para poner cifras en la propuesta necesitamos saber qué podemos entregar y a qué precio. Hay un catálogo de capacidades pendiente desde hace varias sesiones.

**Por qué te pregunto:** Si la respuesta de la pregunta 3 es "cifras concretas", el catálogo es bloqueante para el primer cliente real. Sin él no puedo generar la sección Propuesta del Word.

- [ ] Opción A — Sí, lo construimos juntos antes del primer cliente real. Tú me cuentas qué podemos entregar y a qué precio; yo lo armo en un documento de 1 página
- [ ] Opción B — El primer cliente va con rango cualitativo; el catálogo lo armamos después con la experiencia de la primera entrega
- [ ] Opción C — Tú ya lo tienes armado mentalmente; me lo cuentas en la reunión y armamos el documento ahí mismo

---

### 5. Las 6 fases del Ciclo 2 — ¿skills automatizados, trabajo humano, o mezcla?

Tu diagrama del Ciclo 2 tiene 6 fases (Diseño → Construcción → Pruebas → Ajustes → Implementación final → Mantenimiento). No queda claro si cada fase la ejecuta un skill o es trabajo humano custom.

**Por qué te pregunto:** Define qué documentamos en el spec sobre Ciclo 2 y si abrimos tasks técnicas para construir skills nuevos.

- [ ] Opción A — Cada fase eventualmente será un skill (Skills 08-13). Hoy no construimos nada; cuando llegue el primer Ciclo 2 real arrancamos
- [ ] Opción B — Ciclo 2 es trabajo humano custom por cliente. No skills automatizados. Cada proyecto se diseña a mano
- [ ] Opción C — Algunas fases serán skills (Diseño, Pruebas), otras siempre humanas (Construcción, Ajustes)

---

### 6. La garantía de 1 mes — ¿qué cubre exactamente?

Tu diagrama incluye "Mantenimiento — garantía 1 mes" como fase 6 del Ciclo 2. Es un compromiso comercial que tiene que aparecer claro en cada propuesta.

**Por qué te pregunto:** "Garantía" sin definir invita malentendidos con el cliente. Necesitamos un alcance claro.

- [ ] Opción A — Solo bugs en lo entregado. Cambios de alcance o features nuevas no entran
- [ ] Opción B — Bugs + ajustes menores razonables a nuestro juicio
- [ ] Opción C — Se define caso por caso en la propuesta de cada cliente, no hay regla fija

---

### 7. La garantía de 1 mes — ¿incluida en el precio o aparte?

**Por qué te pregunto:** Afecta cómo redactamos la sección Propuesta del Word.

- [ ] Opción A — Incluida en el precio del Ciclo 2
- [ ] Opción B — Aparte. Cobramos retainer mensual desde el día 1 post-entrega
- [ ] Opción C — Caso por caso según tamaño del proyecto

---

## Importantes pero no bloqueantes

### 8. Canales de entrada del paso 1 (Captación)

Tu diagrama menciona WhatsApp, email, página web y redes sociales como canales por donde puede llegar un prospecto.

**Por qué te pregunto:** Cada canal requiere infraestructura distinta. WhatsApp Business + automatización de email + un formulario web + integración con redes sociales son cuatro proyectos técnicos diferentes.

- [ ] Opción A — Todos automatizados desde día uno (proyecto técnico grande)
- [ ] Opción B — Solo WhatsApp + email automatizados; web y redes manuales
- [ ] Opción C — Solo manual al principio; tú o yo recibimos personalmente y metemos los datos al CRM. Automatización viene cuando tengamos 5-10 clientes/mes

---

### 9. ¿El funnel del CRM tiene etapas fijas o flexibles?

Tu diagrama dice "etapa Contactado" como ejemplo. La pregunta es si manejamos un set fijo de etapas con transiciones definidas, o cada cliente tiene su propio sub-flujo.

**Por qué te pregunto:** Etapas fijas permiten medir conversión y armar dashboards. Etapas flexibles son más realistas pero menos analíticas.

Te propongo unas etapas concretas:

1. Contactado
2. Pre-llamada agendada
3. Llamada realizada
4. Diagnóstico en producción
5. Diagnóstico entregado
6. Esperando decisión
7. Ciclo 2 firmado
8. Cerrado / Perdido / Pausado

- [ ] Opción A — Etapas fijas como las que te propuse arriba
- [ ] Opción B — Etapas fijas pero con un set distinto (cuéntame cuál)
- [ ] Opción C — Etapas flexibles por cliente

---

### 10. ¿Quién escribe las plantillas de seguimiento D+7/15/30/60/90?

Tu diagrama define 5 mensajes de seguimiento si el cliente no cierra: día 7 manual por Ricardo, días 15/30/60/90 automatizados con IA y mensaje personalizado según la etapa.

**Por qué te pregunto:** Las plantillas son contenido comercial sensible — son el último intento de cerrar después de no haber cerrado en la presentación. El tono y contenido importan mucho.

- [ ] Opción A — Las escribo yo (Ricardo) y te las paso para feedback antes de wrapearlas
- [ ] Opción B — Las escribes tú (JP) y me las pasas para conectarlas al script de envío
- [ ] Opción C — Las redactamos juntos en la próxima reunión

---

### 11. ¿Por qué canal se mandan los mensajes D+7 a D+90?

**Por qué te pregunto:** Afecta la integración técnica. Email es lo más fácil. WhatsApp requiere API verificada. Multi-canal requiere lógica de decisión.

- [ ] Opción A — WhatsApp (es donde el cliente está siempre)
- [ ] Opción B — Email (queda registro formal escrito)
- [ ] Opción C — El canal por donde nos contactó originalmente
- [ ] Opción D — Multi-canal según relevancia del mensaje (urgente = WhatsApp; documental = email)

---

### 12. ¿Qué detiene la cadena de seguimiento antes del D+90?

**Por qué te pregunto:** Si el cliente responde algo en D+15, hay que decidir si la cadena se pausa, se acelera o sigue como si nada.

- [ ] Opción A — Cualquier respuesta del cliente pausa la cadena automatizada (Ricardo retoma manual)
- [ ] Opción B — Solo un "no me interesa" explícito la pausa. Las respuestas tibias siguen el cronograma
- [ ] Opción C — Otra lógica que cuentes en la reunión

---

### 13. ¿En qué pasos participas tú (JP)?

Tu diagrama te marca como "opcional" en cuatro puntos: preparación de la llamada (paso 5), llamada de descubrimiento (paso 6), revisión de entregables (paso 10), presentación al cliente (paso 11).

**Por qué te pregunto:** Define cómo organizamos el trabajo entre los dos.

- [ ] Opción A — Opcional en todos esos pasos (tú decides caso por caso según disponibilidad)
- [ ] Opción B — Obligatoria en revisión de entregables (paso 10); opcional en los otros
- [ ] Opción C — Participas en todos pero como observador / segunda opinión; Ricardo conduce todas las interacciones con el cliente
- [ ] Opción D — Otra distribución que tú quieras proponer

---

### 14. "Cowork" como nombre de la IA — ¿comercial o sólo etiqueta del diagrama?

En tu HTML etiquetaste a la IA como "IA · Cowork".

**Por qué te pregunto:** Define cómo nos referimos a la IA en los documentos que ve el cliente.

- [ ] Opción A — "Cowork" es el nombre comercial; lo usamos siempre que hablemos de la IA en outputs cliente
- [ ] Opción B — Es sólo etiqueta interna del diagrama. En outputs cliente bajamos la frecuencia de "AI" o "IA" como decidimos antes (decir QUÉ se puede hacer, no QUÉ comprar)
- [ ] Opción C — Es nombre interno entre nosotros, pero cliente-facing usamos otra cosa (cuéntame cuál)

---

## Cierre

Cuando me respondas — en este documento, en Telegram, o en la reunión cara a cara — yo:

1. Escribo el spec oficial del Pipeline v2 con todas estas decisiones integradas
2. Identifico los cambios técnicos requeridos
3. Te confirmo el plan antes de tocar código

Las que prefieras dejar para la reunión, márcalas como "reunión" y las cerramos cara a cara mañana.
