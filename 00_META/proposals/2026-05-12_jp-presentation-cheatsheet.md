# Cheat Sheet — Presentación JP · Sistema Operativo M.I.A

> **HTML que vas a presentar:** `2026-05-12_jp-presentation-v3.html` ← **v3, recién armada**
> **HTML histórico (v2):** `2026-05-11_jp-presentation.html` — sin cambios, queda como archivo
> **Para:** Ricardo (presentador) · **Audiencia objetivo:** Juan Pablo
> **Fecha de presentación:** 2026-05-13
> **Estado:** Cheat sheet de respaldo — no se entrega a JP

---

## Cómo usar este documento

Este es tu guion de presentador. Cada sección del HTML tiene aquí cuatro líneas:

- **Qué es** — la cosa concreta que JP está viendo en pantalla. Habla simple.
- **Propósito** — por qué esta sección existe en la presentación; qué debe entender JP al final de ella.
- **Por qué lo usamos** — el razonamiento de fondo (la decisión técnica/de diseño que está debajo).
- **Cómo presentarlo (paso a paso)** — los puntos que tienes que decir, en orden, sin leer slide-por-slide.

**Secciones nuevas que aparecen solo en v3 del HTML** (no estaban en v2):
- **Cimientos · sub-bloque "Los 6 candados"** — al final de Cimientos, con la analogía de caja fuerte.
- **"Plan dual de herramientas"** — sección completa nueva, entre Stack y Odoo.
- **"Servicios"** — sección completa nueva, después de Odoo, antes de Install.

Estas tres están marcadas en el cheat sheet con el tag **[NUEVO EN V3]** para que sepas qué presentar con más cuidado.

Al final hay una sección con las **decisiones que JP debe tomar** y un bloque de **preguntas anticipadas + respuestas**.

Regla de oro: **JP no necesita entender cómo se construye nada. Necesita entender qué pasa, por qué pasa, y dónde firma. Habla como si le explicaras a un amigo inteligente que no es técnico — sin jerga.**

---

## 0 · Antes de empezar (30 segundos)

Antes de abrir el HTML, dile a JP en voz:

> "Esto es la propuesta del sistema operativo de la compañía — no es código, no es un producto. Es la base sobre la que vamos a construir todo. La idea es que al terminar tengas una decisión clara: firmas, editas, o vetas."

Eso lo ancla. Ahora abre el HTML.

---

## 1 · Hero — apertura

**Qué es:** la portada. Título, fecha, "preparado por Ricardo", estado "Propuesto".

**Propósito:** formalidad. Esto NO es una conversación informal — es un documento que va a ser firmado.

**Por qué lo usamos:** marca el tono. Si JP siente que esto es serio, lee con seriedad.

**Cómo presentarlo:**
1. Lee el título en voz alta: "Sistema operativo M.I.A — Mejía, IA & CIA."
2. "Lo que viene es la propuesta. Al final hay una sección para firmar, editar o vetar."
3. Click en "Empezar" o scroll.

---

## 2 · ¿Qué estás viendo? — contexto

**Qué es:** dos tarjetas — "Qué decide este documento" y "Propósito general".

**Propósito:** que JP entienda el alcance antes de entrar en detalle. No es un plan de negocios, es el sistema operativo.

**Por qué lo usamos:** sin este frame, JP puede llegar al detalle pensando "¿y la estrategia comercial?" Esto le dice: la estrategia comercial vive en el Plan Maestro; aquí vive el sistema.

**Cómo presentarlo:**
1. "Este documento decide cuatro cosas: dónde vive lo que producimos, cómo se respalda, cómo nos comunicamos con el sistema, y cómo los agentes de IA trabajan dentro."
2. "Tu trabajo al leerlo es: revisar, comentar o vetar."
3. Subraya la pregunta clave que tienen que resolver juntos: **"¿cómo nos comunicamos con el sistema?"** — esta es la decisión más visible (Heavy / Hosted / Light, sección 13).

---

## 3 · El sistema en 4 piezas — mapa mental

**Qué es:** cuatro tarjetas grandes numeradas — Cimientos, Arquitectura, Agentes, Bot.

**Propósito:** dar el mapa antes del recorrido. Las cuatro capas siguientes son cada una de estas piezas.

**Por qué lo usamos:** la presentación es larga. Si JP ve la silueta de las 4 piezas al inicio, no se pierde después.

**Cómo presentarlo:**
1. "El sistema tiene 4 capas. Cada una habilita a la siguiente."
2. Apunta cada una en orden:
   - **Cimientos** — dónde vive, seguridad, respaldos.
   - **Arquitectura** — la forma: carpetas, cadena de clientes, personas.
   - **Agentes** — el trabajo automatizado.
   - **Bot** — la ventana al sistema desde el teléfono.
3. "Todo empieza por Cimientos. Sin eso, nada arriba funciona."

---

## 4 · Cimientos — Capa 01

**Qué es:** 8 tarjetas expandibles con las decisiones de infraestructura base.

**Propósito:** que JP entienda que la base es sólida — no estamos improvisando. Encripción, respaldos, permisos, disciplina de git.

**Por qué lo usamos:** sin cimientos sólidos, todo lo demás es frágil. Esta sección es la que más reduce riesgo percibido para JP (que es asesor estratégico — le importa el riesgo).

**Cómo presentarlo (no leas las 8, agrúpalas en 3 bloques):**

**Bloque A — Dónde vive (3 tarjetas):**
1. **Casa del repositorio** — "Todo el cerebro de la compañía vive en mi servidor, en una carpeta única. Gitea es como un GitHub privado nuestro — la página web para verlo."
2. **Vault de documentos** — "Piensa en una caja fuerte digital. Documentos sensibles (contratos, IDs) están cifrados. Tú tienes una llave, yo tengo otra. Cualquiera de los dos puede abrirla. Si pierdes la tuya, te quito tu llave del candado y le pongo una nueva." **[Tarjeta ya extendida en v3 con protocolo de revocación: emergencia unilateral vs rotación con PR. Click en la tarjeta para mostrar el detalle si JP quiere ver.]**
3. **Secretos del sistema** — "API keys (las contraseñas que el sistema usa para hablar con servicios externos) viven en otro archivo cifrado. Se descifran solo el segundo que se usan y se borran." **[Tarjeta ya extendida en v3 con el paso a paso: descifra → usa → borra.]**

**Bloque B — Cómo se protege (3 tarjetas):**
4. **Disciplina de git** — "Cambios chiquitos pasan directo. Cualquier cosa que termine en manos del cliente tiene que pasar por revisión — como un segundo par de ojos obligatorio. Esto evita que un error mío llegue al cliente sin que tú lo veas."
5. **Respaldos múltiples** — "Imagínate que todo nuestro trabajo vive en 5 lugares al mismo tiempo: nuestro servidor, GitHub, Codeberg, un disco local, y Google Drive. Si se queman 2 al mismo tiempo, los otros 3 nos salvan."
6. **Permisos: humano vs IA** — "Los agentes pueden escribir notas y status sin pedir permiso. Pero borrar archivos, mover cosas, o tocar la configuración crítica requiere que uno de nosotros lo apruebe. La misma regla aplica también a nosotros — nadie borra sin que el otro vea."

**Anuncio del sub-bloque "6 candados" abajo:** "Sobre si Claude puede ver el `.env`, hice una sub-sección dedicada al final de Cimientos — con analogía de caja fuerte y los 6 candados explicados uno por uno. La vemos en un minuto cuando bajemos." → presentar ahí con detalle.

**Bloque C — Cómo escala (2 tarjetas):**
7. **Activos pesados** — "Audios y PDFs grandes a Drive 2TB + mirror al NAS. Audio-only para grabaciones — 20× más eficiente que video."
8. **Niveles de acceso** — "Tres maneras de conectarse al sistema. Cada uno elige. Lo vemos en la sección 13." (Esto es teaser — no lo explores aquí.)

**Tip:** si JP se queda mirando una tarjeta, dile "haz click para ver el detalle." Si no, sigue.

### Sub-bloque "Los 6 candados" [NUEVO EN V3]

**Qué es:** sección al final de Cimientos, en pantalla aparece justo después de las 8 tarjetas.

**Propósito:** responder de frente a tu Q2 ("¿Claude puede ver el `.env`?"). Lo armé como sección dedicada con la analogía del asistente humano + 6 sub-cards (uno por candado).

**Cómo presentarlo:**
1. **Frame inicial:** "Esta sub-sección es respuesta directa a una de tus preguntas. Te la pongo aquí porque la respuesta tiene capas y no quería inventarme un sí o un no."
2. **Lee la analogía en voz alta** (callout azul al inicio): Claude = asistente humano en mi oficina. Ve el escritorio, no la caja fuerte. Tengo yo la llave. Cuando saco algo lo dejo 10 segundos en el escritorio. Hay reglas + guardia + permisos para que no mire en ese instante.
3. **Recorre los 6 candados rápido** — no leas las descripciones completas; nombra el candado y di una frase:
   - 1 · Caja fuerte (cifrado en disco)
   - 2 · Pizarra de memoria (uso temporal en RAM)
   - 3 · Guardia en la puerta (hook automático que bloquea)
   - 4 · Reglas escritas (CLAUDE.md le dice qué no leer)
   - 5 · Permisos del sistema (Linux no le da acceso)
   - 6 · Rotación trivial (cambiar la llave toma 30 seg)
4. **Lee el callout final** ("¿Y los prompts que sí van a Anthropic?"): no entrenan, retención 30 días, Zero Data Retention disponible cuando lo pidamos.
5. **Resumen verbal:** "No es seguridad hermética, pero sí seriamente defendida. Si quieres todavía más detalle, lo tienes escrito en el FAQ."

---

## 5 · Arquitectura — La forma del sistema

**Qué es:** árbol de carpetas del repo + dos explicaciones laterales (organizado por función / split infra vs operations).

**Propósito:** que JP entienda **dónde vive cada cosa**. Si mañana abre el repo, sabe a qué carpeta ir.

**Por qué lo usamos:** carpetas planas + nombres descriptivos. Discoverable. No hay sistema numérico que memorizar como en el Brain personal de Ricardo (`00_META`, `01_VENTURES`...). Aquí solo `skills/`, `clients/`, `operations/`, etc.

**Cómo presentarlo:**
1. "El repo es plano. Carpetas con prefijo `00_` son gobernanza — meta, governance, partnership. El resto son funciones del negocio."
2. Apunta `skills/` — "los 5 skills del diagnóstico viven aquí."
3. Apunta `clients/` — "una carpeta por cliente. Cada cliente es una línea de ensamblaje (siguiente sección)."
4. Apunta `operations/` — "funciones internas: marketing, sales, accounting, legal, IT."
5. **Punto importante — el split intencional:** "`infra/` es código que construimos. `operations/it/` son servicios a los que nos suscribimos (Notion, Drive, Cal.com). No los mezclamos."
6. Apunta `vault/` — "ahí va lo encriptado de alto valor: contratos firmados, IDs, NDAs."

---

## 6 · Cadena de producción — 13 estaciones

**Qué es:** una franja horizontal de 13 estaciones numeradas, agrupadas por color (Diagnóstico / Propuesta / Ejecución).

**Propósito:** que JP visualice **el flujo del cliente** de principio a fin. Cada estación es una carpeta dentro de `clients/<cliente>/`.

**Por qué lo usamos:** un cliente no es un blob caótico. Es un proceso secuencial donde cada paso deja un output en su carpeta y dispara el siguiente. Esto hace que el trabajo sea auditable y reproducible.

**Cómo presentarlo:**
1. "Cada cliente sigue exactamente esta línea de ensamblaje. 13 estaciones."
2. Recorre los 3 grupos de color:
   - **Diagnóstico** (azul · 00-05): Intake → Compañía → Industria → Competencia → Guión → Reporte. **Skills 1-5 viven aquí.**
   - **Propuesta** (dorado · 06-07): Propuesta + Contrato/Onboarding.
   - **Ejecución** (verde · 08-11): Diseño → Implementación → Seguimiento (30/60/90) → Retainer.
   - **Archive** al final cuando cierra.
3. Apunta abajo: "Dos cosas cruzan todas las fases — `transcripts/` (audio transcrito) y `communications/` (email, WhatsApp, Telegram con el cliente)."
4. **Punto clave:** "Las carpetas no se mueven jamás. Una vez que algo está en su estación, ahí se queda. La progresión es por eventos, no por mover archivos."

---

## 7 · Personas + comunicación — Capa 02

**Qué es:** 3 personas (Founder / Skills-Master / Client-Owner) + un bloque que muestra `events.jsonl` + 4 superficies para observar el sistema.

**Propósito:** explicar **cómo opera Claude dentro del sistema** y **cómo se observa lo que pasa**.

**Por qué lo usamos:** en el Brain personal de Ricardo, cada carpeta tiene su propia persona. Eso se vuelve frágil cuando son 20+ carpetas. Aquí simplificamos a 3 personas atadas a función, no a ubicación. Y `events.jsonl` es el mecanismo de comunicación entre piezas (en vez del sistema de memos del Brain personal, que es síncrono y manual).

**Cómo presentarlo:**

**Parte A — 3 personas:**
1. "Claude opera en 3 modos dependiendo de la carpeta donde esté."
2. **Founder** (en `/`) — "estrategia, gobernanza, marketing, ventas, prospectos. La persona por defecto."
3. **Skills-Master** (en `skills/`) — "diseña, versiona, prueba los 5 skills. Dueña de los casos de benchmark."
4. **Client-Owner** (en `clients/`) — "opera la cadena de producción. El cliente activo es un parámetro — la misma operadora atiende a Ascenso hoy y a Bodai mañana."

**Parte B — events.jsonl (el "sistema nervioso"):**
5. Apunta el JSON de la izquierda. "Esto es un solo archivo donde se anota cada cosa importante que pasa en el sistema, una línea por evento. Piénsalo como el cuaderno de bitácora de un barco — solo se agrega abajo, nunca se borra ni se reescribe."
6. "Los agentes 'escuchan' este cuaderno: 'cuando aparezca una línea que diga *Skill 1 terminó*, corre Skill 2 automáticamente.' Es como un sistema nervioso — un nervio dispara, otro reacciona."
7. "El bot también escucha — cuando pasa algo importante, te llega solo al chat. No tienes que preguntar '¿qué pasó hoy?'"

**Parte C — 4 superficies:**
8. "Hay 4 maneras de ver qué está pasando, todas leen los mismos datos:"
   - `events.jsonl` — stream crudo en vivo.
   - `STATUS.md` — agregado humano-legible por proyecto.
   - **Bot de Telegram** — `/status`, `/digest`, brief matinal al teléfono.
   - **Notion CRM** — vista kanban del pipeline.
9. "Cada usuario elige la que prefiera."

---

## 8 · Agentes — Capa 03

**Qué es:** un hub central (`dispatch.py`) rodeado de 4 maneras de invocarlo.

**Propósito:** que JP entienda que los agentes no son magia — son scripts con 4 puntos de entrada predecibles.

**Por qué lo usamos:** una sola lógica de runtime (`dispatch.py`) que carga el skill, valida inputs, ejecuta, escribe outputs, emite eventos. Cuatro caminos para llamarla — pero el agente en sí es uno solo.

**Cómo presentarlo:**
1. "Un agente toma inputs, ejecuta un skill, produce outputs, emite un evento. Eso es todo."
2. Apunta el hub central: "`dispatch.py` es el único punto de entrada. Garantiza que da igual cómo lo llames, hace lo mismo."
3. Las 4 maneras de invocar:
   - **Comando bot** — `/skill1 ascenso` desde Telegram.
   - **Eventos** — una línea en `events.jsonl` dispara el agente automáticamente.
   - **Cron programado** — systemd timer (ej. digest diario 8am).
   - **CLI directo** — `mejia agent run` desde la terminal.
4. "El mismo motor responde a las 4. No mantenemos 4 versiones del mismo skill."

---

## 9 · Bot — Capa 04

**Qué es:** mockup de un teléfono con un chat de Telegram + listas de comandos divididas en Capturas y Operaciones.

**Propósito:** que JP entienda **la interfaz humana del sistema**. Si elige el modo Light (sección 13), este es su único punto de contacto.

**Por qué lo usamos:** Telegram funciona en celular y desktop, allowlist estricto (solo Ricardo y JP), bot familiar de usar. No hace falta una app custom.

**Cómo presentarlo:**
1. "El bot es la ventana al sistema. Tres canales: grupo (los dos), tu DM, mi DM. Allowlist estricto — nadie más puede hablarle."
2. Muestra el flujo del chat en pantalla: capturar prospecto → disparar skill → ver status.
3. Explica las dos categorías:
   - **Capturas** — información que entra al sistema (`/note`, `/idea`, `/decision`, `/expense`, `/client`, `/meeting`, `/marketing`, `/prospect`).
   - **Operaciones** — cosas que el sistema ejecuta (`/status`, `/skill1..5`, `/pipeline run`, `/digest`, `/ask`, `/help`).
4. **Punto importante (escalamiento a IA):** "Por default el bot responde con plantillas — barato y rápido. Escala a Claude solo cuando lo pides con `/ask`, o cuando un mensaje largo no tiene comando. Rate-limit de 20 escalamientos por hora por usuario. Esto controla costo."

---

## 10 · Árbol de la compañía — Organización

**Qué es:** un diagrama de árbol con la compañía arriba y 3 ramas (Skills / Pipeline / Operations) con sus hojas.

**Propósito:** vista organizacional, no técnica. Lo mismo de antes pero como organigrama mental.

**Por qué lo usamos:** algunas personas piensan en árboles, otras en carpetas. Esto refuerza el modelo desde otro ángulo. JP puede preferir este formato.

**Cómo presentarlo (rápido — es refuerzo, no contenido nuevo):**
1. "Visto como organigrama: tres ramas."
2. **Skills** (capa metodológica) — los 5 skills, lo que la compañía sabe hacer.
3. **Pipeline** (capa comercial) — prospects, clients, templates, knowledge.
4. **Operations** (capa operativa) — marketing, sales, accounting, legal, IT.
5. "Si no recuerdas el árbol de carpetas, recuerda esto. Es la misma cosa."

---

## 11 · Stack tecnológico — Lo que vamos a usar

**Qué es:** dos grids de herramientas con precio — Stage 1 (ahora) y Stage 2 (cuando se justifique). En v3 ya está actualizado: Notion como `$0 · cuenta de JP`, Whisper.cpp removido (subió al plan dual).

**Propósito:** transparencia de costos. JP ve exactamente qué se paga y qué es gratis.

**Por qué lo usamos:** "Boring but Robust". Mayoría free / open source. Solo pagamos lo imprescindible (Claude, Drive 2TB).

**Cómo presentarlo:**
1. "Stage 1 es lo que se despliega desde día uno. Stage 2 espera un gatillo concreto."
2. Resume Stage 1 — "Casi todo gratis u open source. Lo pagado: Claude Code (Anthropic) y Drive 2TB. Notion lo aportas tú, gracias."
3. Resume Stage 2 — "Cosas que se activan cuando hace falta: Codeberg como tercer mirror, Backblaze cuando se llene Drive, DocuSign para primer contrato firmado, Stripe para primera factura, CRM upgrade si el pipeline pasa de 15 clientes activos."
4. **Punto clave:** "No compramos nada antes de necesitarlo."
5. **Apunta al callout dorado al final:** "Y aquí viene algo nuevo — el plan dual. Bajamos."

---

## 12 · Plan dual de herramientas [NUEVO EN V3]

> **Sección completa nueva en el HTML de v3** (entre Stack y Odoo). Si JP solo lee dos secciones nuevas, esta es la prioritaria — convierte la conversación de Stack en una conversación estratégica.

**Qué es:** sección dedicada en v3. Tiene un eyebrow "Nuevo en v3 · Filosofía de herramientas", título grande, dos tarjetas (¿Por qué? + ¿Cómo se opera?), una tabla de 9 pares producción↔shadow, un cronograma de 4 semanas, y un callout final con lo que NO promete.

**Propósito:** convertir cada categoría de SaaS gringo en una posible línea de servicio nuestra. Es el cambio estratégico más importante de v3.

**Por qué lo usamos:** vendemos lo que sabemos operar. Eat your own dogfood ampliado de Odoo a todas las categorías. Reduce vendor lock-in y construye credibilidad real frente al cliente.

**Cómo presentarlo (paso a paso, ~5-7 min):**

1. **Frame inicial:** "Esto es la pieza nueva más grande de v3. Es una propuesta estratégica que cambia cómo pensamos el stack."

2. **La idea en una línea (lee el lede):** "Las herramientas pagadas las usamos para trabajar bien hoy. En paralelo, instalamos las versiones libres en nuestro servidor — sin riesgo, sin tráfico crítico — para aprender a operarlas. Cuando maduren, las ofrecemos a clientes."

3. **Las 4 razones (apunta a la tarjeta izquierda — no las leas todas, escoge 2-3):**
   - "Vendemos lo que sabemos operar."
   - "Probamos antes de prometer."
   - "Reducimos vendor lock-in."
   - "Credibilidad: cuando el cliente pregunta '¿tú lo usas?', la respuesta es 'sí, hace meses'."

4. **Cómo se opera (apunta a la tarjeta derecha):**
   - **Producción** = la pagada, trabajo real sin riesgo.
   - **Shadow** = la libre en paralelo, notas no críticas.
   - **Migración** = solo si la libre llega a ≥80% de paridad.
   - **Oferta al cliente** = software libre gratis + nuestro servicio billable.

5. **Tabla de pares (recórrela rápido):** "9 categorías. Notion ↔ Anytype, Drive ↔ Nextcloud, Meet ↔ Jitsi, Claude ↔ Ollama local, Notion AI ↔ Whisper, DocuSign ↔ Documenso. Calendario y git ya están self-hosted. Pagos no tiene alternativa real, ahí no aplica."

6. **Cronograma (los 4 dots):** "Semana 1 Nextcloud + Jitsi · Semana 2 Ollama · Semana 3 Whisper · Semana 4 Anytype o AppFlowy. Total 5-7 días de mi tiempo. **Costo: USD 0**."

7. **Lee el callout final** ("Lo que NO promete por honestidad") — esto es importante para que JP no piense que estoy vendiéndole humo:
   - No todas las libres alcanzan paridad de Notion AI.
   - El shadow se desacelera cuando entren clientes pagos.
   - Si Ollama exige GPU que no tenemos, queda como experimento.
   - Pagos siempre necesitan Stripe/Mercado Pago.

8. **La decisión que pides:** "Hay un radio button en la sección de Firma para esto. Tres opciones: Aprobar Stage 1 (mi recomendación), Después, o Solo Odoo. ¿Qué te parece?"

9. **Si JP quiere ver los servicios al cliente:** "La siguiente sección lista los 5 servicios que el plan habilita, con tickets aproximados." → bajamos a Sección 14.

---

## 13 · Odoo — Decisión pendiente (reframe en v3)

**Qué es:** sección destacada con dos ángulos (Uso interno / Línea de servicio) y una pregunta abierta. **En v3 la quote final fue extendida** para conectar con la nueva sección "Servicios" — Odoo deja de ser caso aislado y se convierte en el primer ejemplo de una familia de servicios.

**Propósito:** decisión explícita que JP tiene que tomar contigo, ahora ampliada al contexto del plan dual.

**Por qué lo usamos:** Odoo es ERP open-source dominante entre PyMEs LatAm. Es el caso de uso más maduro de "vendemos lo que operamos". Tickets grandes (USD 5K-25K).

**Cómo presentarlo:**
1. "Odoo es el ERP open-source dominante en LatAm para PyMEs. Edición Community gratis y selfhosted."
2. Ángulo 1 — **Uso interno:** "Lo usamos para nuestra contabilidad/CRM. Cuando le vendemos a un cliente, ya operamos así."
3. Ángulo 2 — **Línea de servicio:** "Customización + integración con IA. Mercado real y amplio en LatAm. Tickets típicos: configuración inicial, módulos custom, integraciones, automatización vía IA dentro de Odoo. Categoría billable real."
4. **La pregunta abierta + el bridge a Servicios:** "¿Abrazarlo como apuesta de línea de servicio? Y ojo — ya no es Odoo solo. En v3 lo amplié a una familia. La siguiente sección lo muestra."
5. **No fuerces respuesta aquí** — esto regresa en la sección "Otras decisiones por tomar". Si JP quiere opinar ya, escúchalo y toma nota mental. Si no, sigue a Servicios.

---

## 14 · Servicios [NUEVO EN V3]

> **Sección completa nueva en el HTML de v3** (después de Odoo, antes de Install). Cierra el círculo del plan dual: cada herramienta libre que operamos se convierte en una línea de servicio cobrable.

**Qué es:** sección con eyebrow "Nuevo en v3 · Línea de servicio", título grande ("Cada categoría de SaaS gringo es una posible línea de servicio"), lista de 5 servicios numerados con tickets, y un callout final anticipando la pregunta del cliente "¿Por qué tú usas Notion entonces?".

**Propósito:** mostrarle a JP que el plan dual no es ejercicio académico — es la fundación de líneas de servicio billables.

**Por qué lo usamos:** convertir suscripciones en revenue. Cada SaaS gringo es una migración cobrable + soporte cobrable.

**Cómo presentarlo (rápido, ~3 min):**

1. **Frame:** "Esto cierra el plan dual. Cuando las herramientas libres maduren internamente (~6 meses de uso shadow), cada una se vuelve una oferta."

2. **Recorre los 5 servicios — di el nombre, el ticket, y una frase de contexto:**
   - **01 · Notion → Anytype/AppFlowy** — USD 800-1500. "PyMEs que quieren reducir gasto recurrente en SaaS."
   - **02 · Drive → Nextcloud** — USD 1200-2500. "Soberanía de datos + control de costos a escala de TB."
   - **03 · Meet → Jitsi self-hosted** — USD 600-1200. "Empresas sensibles a privacidad o con gasto Meet/Zoom alto."
   - **04 · Whisper local** — USD 800-1500. "Transcripción sin enviar audio a terceros. Sectores regulados."
   - **05 · ERP Odoo Community** — USD 5K-25K. "Categoría aparte, tickets grandes."

3. **Lee el callout final** — es la pregunta esperada del cliente:
   > "'¿Por qué tú usas Notion entonces?' — Respuesta honesta: porque ya teníamos el workflow montado y migrar tiene costo. Pero sabemos cómo hacer la migración tuya — conocemos los puntos de dolor porque los estamos enfrentando en paralelo."

4. **Punto clave:** "No promete que vamos a vender todo desde día uno. Promete que cuando un cliente pregunte, tendremos la respuesta y la habilidad."

5. **Bridge a Install:** "Bajamos a la decisión más importante para ti — cómo te conectas tú al sistema."

---

## 15 · ¿Cómo se conecta cada usuario? — DECISIÓN PRINCIPAL

**Qué es:** tres tarjetas — A (Heavy) / B (Hosted) / C (Light, recomendado).

**Propósito:** **la decisión más importante del documento para JP**. Tiene que elegir cómo va a interactuar con el sistema.

**Por qué lo usamos:** el sistema funciona para los 3 modos. JP puede elegir el que más se ajuste a su tiempo y apetito de tooling. Ricardo va a operar Heavy. JP puede elegir distinto.

**Cómo presentarlo (con calma — esta es la sección más importante):**

1. "Tres maneras de conectarse. Cada uno elige por separado."

2. **A · Heavy — operador par:**
   - En la laptop: Claude Code, Gemini CLI, clone de git, llave de encriptación.
   - Poder: igual que el operador principal. Trabajas directamente en cualquier carpeta.
   - Setup: unas horas + mantenimiento de tooling.
   - Secretos: en tu laptop también.
   - "Es lo que yo voy a operar."

3. **B · Hosted — navegador remoto:**
   - En la laptop: solo un navegador web + Tailscale.
   - Poder: igual que Heavy, pero las herramientas corren remoto en el servidor.
   - Setup: ~15 minutos (login en navegador).
   - Secretos: solo en el servidor.
   - "Para usuarios que no quieren mantener tooling local."

4. **C · Light — Telegram + Gitea web (recomendado por default):**
   - En la laptop: navegador + Telegram. Ya está.
   - Poder: bot para operar, Gitea web para leer documentos.
   - Setup: cero — ambas apps ya existen.
   - "Cero fricción. La sugerencia por default para ti, pero la decisión es tuya."

5. **Pregunta directa a JP:** "¿Cuál te ves usando?"
   - Anota la respuesta. Es la primera pregunta del bloque de Firma.

---

## 16 · Otras decisiones por tomar (v3 — reorganizada)

**Qué es:** lista de decisiones pendientes. **En v3 cambió la composición** — privacidad de grabaciones está cerrada (badge verde con ✓), entran dos items nuevos (Plan dual + Split de costos), Odoo se reformuló como "Odoo + línea de servicio en software libre".

**Propósito:** dejar explícitas las decisiones que no se cierran solas. Cada una admite acepto, edito, veto.

**Por qué lo usamos:** mejor listar las decisiones abiertas que pretender que todo está resuelto. Honesto, profesional.

**Cómo presentarlo (orden actual en HTML v3):**

0. **Privacidad de grabaciones — CERRADA** (badge verde con ✓). "Esto ya lo cerramos con tu respuesta — Notion AI + revisión inmediata + export al repo. Lo dejo aquí para registro."

1. **Plan dual de herramientas** [NUEVO]. "¿Aprobamos Stage 1? Recomendación: sí. Hay radio en Firma."

2. **Posicionamiento de Odoo + línea de servicio en software libre.** "Ampliado de Odoo solo a la familia completa de 5 servicios que vimos arriba."

3. **Formalización del protocolo de sociedad.** "El mecanismo de '15 min mano levantada + respuesta escrita en 12-24h' que ya practicamos. ¿Lo codificamos por escrito y lo firmamos?"

4. **Primer servicio pagado después del Diagnóstico.** "Diseño → Implementación → Seguimiento → Retainer. ¿Qué cobramos primero — Diseño? ¿O salto directo a Implementación para los pilotos satisfechos?"

5. **Criterios del clasificador de prospectos.** "Tenemos un formulario de 5 preguntas. ¿Qué significa 'calificado'? — mínimo de facturación, sector, disposición al cambio."

6. **Split de costos pre-revenue** [NUEVO]. "Yo pago Claude + Drive + hardware. Tú aportas Notion. Dominio + legal cuando se constituya entity — definir. Quien adelanta se reembolsa con primer ingreso o entra a equity."

**Para cada una:** "Puedes decirme ahora o anotarlo en la sección de firma para discutirlo después."

---

## 17 · Camino — Del documento al primer piloto (v3 — paso 2 ampliado)

**Qué es:** 4 hitos numerados. **En v3 el paso 2 fue ampliado** para incluir el deploy de shadows del plan dual en paralelo al scaffold.

**Propósito:** que JP vea **qué pasa después de firmar**. No es "firma y ya veremos" — hay un camino concreto.

**Por qué lo usamos:** la aprobación tiene consecuencias inmediatas. Mostrar el roadmap reduce la sensación de "estoy firmando un cheque en blanco".

**Cómo presentarlo:**
1. "Después de firmar, esto es lo que pasa:"
2. **01 — Aprobación** — "Lo que estás haciendo hoy."
3. **02 — Scaffold + Skills 2-5 + shadows en paralelo** [ampliado en v3] — "Construyo la estructura (vault, secretos, respaldos, bot v0). En paralelo construyo Skills 2-5 — Skill 1 ya existe. **Y en paralelo despliego los shadows del plan dual** en las primeras 4 semanas: Nextcloud, Jitsi, Ollama, Whisper, Anytype/AppFlowy."
4. **03 — Primer diagnóstico piloto** — "Corremos la cadena completa con un cliente piloto. Refinamos prompts. Validamos entregables. Sin cobro."
5. **04 — Primer Diagnóstico pagado** — "Cuando la calidad sea 8/10 estable y haya al menos un caso de éxito documentado. Activamos modelo de cobro."

---

## 18 · Firma — Cierre (v3 — radio nuevo del plan dual)

**Qué es:** dos columnas — radios para elegir interfaz (A/B/C), **radios para el plan dual** [NUEVO en v3] (Aprobar Stage 1 / Después / Solo Odoo), radios para aprobación general (acepto / con ediciones / declino), área de notas, dos líneas de firma.

**Propósito:** **cerrar la conversación con decisiones registradas por escrito**.

**Por qué lo usamos:** "propuesto" vs "aprobado" no es ambiguo. Una firma lo transforma.

**Cómo presentarlo:**
1. "Esta es la parte de firma. **Cuatro** decisiones a tomar (era tres en v2, agregamos plan dual)."
2. **Interfaz elegida** — A / B / C. (Ya la respondió en sección 15.)
3. **Plan dual** [NUEVO] — Aprobar Stage 1 (recomendado) / Después / Solo Odoo. (Ya hablado en sección 12.)
4. **Aprobación general** — acepto / acepto con ediciones / declino.
5. **Notas, ediciones, vetos** — "Si hay items que quieras editar o discutir, anótalos aquí. Cada uno se trata por separado."
6. Firmas — los dos. JP como Asesor Estratégico, Ricardo como Fundador.
7. **Cierre verbal:** "Si firmas hoy, mañana empiezo Scaffold + Skills 2-5 + shadows en paralelo. Si quieres anotar ediciones, las trabajamos juntos antes de firmar la versión final."

---

## Decisiones que JP debe tomar (resumen ejecutivo)

| # | Decisión | Sección HTML | Opciones |
|---|----------|--------------|----------|
| 1 | **Interfaz** | 15 Install + 18 Firma | A · Heavy · B · Hosted · C · Light (default sugerido) |
| 2 | **Plan dual de herramientas** | 12 Plan dual + 18 Firma | Aprobar Stage 1 (recomendado) · Después · Solo Odoo |
| 3 | **Aprobación general** | 18 Firma | Acepto · Acepto con ediciones · Declino |
| 4 | Posicionamiento Odoo + línea de servicio | 13 Odoo + 14 Servicios + 16 Otras | Apostar línea · Foco 5 skills · Solo uso interno |
| 5 | Privacidad de grabaciones | 16 Otras | ✓ **CERRADA por JP** — Notion AI + revisión inmediata + export |
| 6 | Formalización protocolo sociedad | 16 Otras | Sí, lo firmamos · No, queda informal |
| 7 | Primer servicio pagado post-Diagnóstico | 16 Otras | Diseño · Salto a Implementación · Otro |
| 8 | Criterios "calificado" para clasificador | 16 Otras | Por definir juntos |
| 9 | Split de costos pre-revenue | 16 Otras | Por definir (propuesta inicial: Ricardo Claude+Drive, JP Notion) |

**Decisiones obligatorias hoy: 1, 2, 3 (los tres tienen radio button en Firma). Las otras pueden cerrarse hoy o quedar en "ediciones anotadas".**

---

## Preguntas anticipadas y respuestas

> **Nota:** el bloque más completo de Q&A vive en `2026-05-12_jp-respuestas-ronda-1.md` (FAQ por privacidad / seguridad / escalabilidad / despliegue / costo). Lo de abajo son respuestas rápidas para el momento de la presentación. Si JP entra en profundidad en algo, abre el FAQ.


**P: ¿Por qué Telegram y no WhatsApp?**
R: Allowlist nativo, bot API estable y gratuita, multi-dispositivo desde día uno. WhatsApp Business API es más cara y restrictiva. Si en el futuro queremos canal cliente, lo evaluamos aparte.

**P: ¿Por qué Gitea selfhosted y no GitHub directo?**
R: Control total, gratis, en mi servidor. GitHub queda como mirror automático — backup off-site sin pagar plan organizacional.

**P: ¿Qué pasa si te atropella un camión?**
R: Repo en 3 lugares (servidor + GitHub + Codeberg). Llaves age duplicadas. NAS local. Documentación de recuperación en el repo. JP tiene acceso a todo desde día uno si elige Heavy o Hosted; desde Light puede leer vía Gitea web.

**P: ¿Por qué encriptar con `age` y no GPG?**
R: `age` es moderno, simple, una llave por usuario. GPG es más complejo, web-of-trust, herramientas viejas. Para nuestro tamaño, `age` es la elección obvia. Si después se necesita GPG por compliance, se agrega.

**P: ¿Esto no es overkill para una compañía sin clientes?**
R: La base se construye una sola vez. Si la dejamos floja ahora, retrofittear seguridad/respaldos/disciplina cuando ya hay clientes es 10× más costoso. El scaffold sólido permite acelerar después.

**P: ¿Quién mantiene esto?**
R: Ricardo, operacionalmente. JP tiene visibilidad total y derecho de veto en cualquier momento. El bot reporta automáticamente — no hace falta preguntar "¿qué hiciste hoy?"

**P: ¿Y si quiero cambiar algo más adelante?**
R: Todo es texto plano en git. Cualquier cambio es un PR + aprobación. El sistema está diseñado para evolucionar — no para quedarse fijo.

**P: ¿Cuánto cuesta operar esto al mes?**
R: Stage 1 ≈ Claude Code (~USD 20/mes para empezar, escalable) + Notion (~USD 10/mes) + Drive 2TB (~USD 10/mes) + dominios cuando los tengamos. Total mensual operativo ~USD 40-60 hasta que haya clientes pagos. Stage 2 se activa solo cuando justifica el costo.

**P: ¿Qué pasa con Odoo si decidimos hoy "solo uso interno"?**
R: Lo instalamos en el servidor, lo usamos nosotros, y no lo vendemos como línea de servicio formal. Si después aparece un cliente que lo pide, evaluamos.

---

## Recordatorios para Ricardo durante la presentación

- **No leas las slides.** Tu trabajo es interpretarlas; el slide es el respaldo visual.
- **Habla simple, sin jerga.** Cada vez que uses una palabra técnica (encriptado, agente, hook, repo, vault, shadow), traduce: "cifrado = como una caja fuerte digital", "agente = un programa pequeño que hace una tarea específica", "shadow = la versión libre corriendo en paralelo sin riesgo". Si JP no preguntó, asume que entendió a medias.
- **Usa analogías sobre términos.** "Es como X" es más memorable que el término técnico solo. Las que ya están integradas en v3: **caja fuerte** (encriptación), **cuaderno de bitácora** (events.jsonl), **sistema nervioso** (event-driven), **guardia en la puerta** (hooks), **pizarra de memoria** (RAM), **segundo par de ojos** (PR review), **línea de ensamblaje** (cadena de producción), **asistente humano** (Claude + secretos), **shadow** (herramienta libre paralela).
- **Si JP se queda callado mirando algo, déjalo.** Está procesando, no esperando.
- **Si JP hace una pregunta que no sabes responder, di "no sé, lo investigo y te respondo escrito".** No improvises.
- **Los objetivos de hoy son las decisiones 1, 2 y 3 — todas tienen radio button en Firma.** Las otras pueden quedar como "ediciones anotadas".
- **Las tres novedades visuales grandes de v3:**
  1. **"Los 6 candados"** al final de Cimientos — sub-bloque con analogía + 6 sub-cards.
  2. **"Plan dual"** entre Stack y Odoo — sección completa nueva, la pieza estratégica del día.
  3. **"Servicios"** después de Odoo — catálogo de líneas billables que el plan dual habilita.
- **Si JP declina cualquier decisión:** no defiendas el documento. Pregunta qué falta. Cualquier "decline" abre conversación, no la cierra.
- **Si JP propone enmiendas:** anótalas en la `<textarea>` de Firma o en notas separadas. La siguiente versión (v4 si hace falta) las incorpora.
- **Después de la firma (cuando llegue):** exporta el HTML a PDF firmado, archiva una copia en el vault.

---

*Fin del cheat sheet. Suerte.*
