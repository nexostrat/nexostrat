# Respuestas a tus preguntas + FAQ — Sistema operativo M.I.A

> **Para:** Juan Pablo
> **De:** Ricardo
> **Fecha:** 2026-05-12
> **Documento de referencia activo:** `2026-05-12_jp-presentation-v3.html` ← **v3, recién armada con todos los cambios**
> **Documento histórico (v2):** `2026-05-11_jp-presentation.html` (sin cambios, queda como archivo)
> **Estado:** Ronda 1 de respuestas. v3 ya incorpora las enmiendas. Edits/vetos siguen abiertos.

---

## Cómo leer este documento

Tiene tres partes:

1. **Respuestas directas** — a las 5 preguntas y comentarios que dejaste sobre la propuesta.
2. **FAQ** — preguntas anticipadas organizadas por tus 5 preocupaciones principales: **privacidad, seguridad, escalabilidad, despliegue en otras máquinas, costo**.
3. **Plan dual de herramientas** — propuesta nueva que reemplaza y amplía la sección Stack del documento original: usar las herramientas pagadas hoy en producción **y en paralelo** instalar versiones libres en nuestro servidor, para aprender a operarlas y eventualmente ofrecerlas a clientes como línea de servicio.

Cuando algo aquí cambia una decisión de la propuesta v2, lo marco como **[ENMIENDA v2 → v3]**. **Esos items ya están aplicados en v3** del HTML — este documento te explica el porqué.

> **Estado del HTML:** la **v3 está lista** en `2026-05-12_jp-presentation-v3.html`. Incorpora todas las enmiendas listadas en la última parte de este documento: nuevo bloque "Los 6 candados" en Cimientos, nueva sección "Plan dual", nueva sección "Servicios", decisión de grabaciones cerrada con tu respuesta, lenguaje más amigable con analogías (caja fuerte, cuaderno de bitácora). La v2 queda intacta como histórico.

---

# Parte 1 · Respuestas directas

## 1. ¿Quién puede revocar una llave privada?

**Respuesta corta:** cualquiera de los dos, con dos modalidades distintas.

**Cómo funciona `age` en nuestro setup:**
- Tú generas tu par de llaves (`age-keygen`). Tu llave privada vive solo en tu laptop. Tu llave pública vive en el repo en `infra/age-recipients.txt`.
- Yo hago lo mismo. Resultado: `recipients.txt` tiene dos líneas — tu pública y la mía.
- Cuando algo se encripta, se encripta a **las dos llaves**. Cualquiera de las dos puede desencriptar.

**Revocación — dos escenarios:**

| Escenario | Quién revoca | Cómo |
|-----------|--------------|------|
| **Emergencia** (laptop robada/comprometida) | El dueño de la llave, de forma unilateral | Borra su línea de `recipients.txt`, re-encripta todo el vault hacia adelante con las llaves restantes, commit + push. Notifica al otro inmediatamente. |
| **Rotación rutinaria** (cambio de equipo, refresh anual) | Ambos, vía PR + aprobación | El que rota genera nueva llave, abre PR con `recipients.txt` actualizado y vault re-encriptado, el otro aprueba. |

**Punto importante — qué NO revoca la revocación:**
Los archivos encriptados que ya estaban en commits viejos del repo siguen siendo desencriptables con la llave revocada (porque alguien con esa llave podría tener un clone viejo). Por eso, en emergencia, también hay que asumir que **datos sensibles pre-revocación deben tratarse como expuestos** y, si es crítico, regenerarse (ej. rotar API keys, no solo re-encriptar el `.env`).

**[ENMIENDA v2 → v3]:** Agregar `00_GOVERNANCE/key-rotation-protocol.md` con este procedimiento por escrito.

---

## 2. ¿Claude tiene acceso a nuestros secretos, API keys y demás? ¿Puede ver el `.env`?

**Respuesta corta y honesta:** Claude no es una caja mágica que ve todo. Es un programa que corre en mi laptop. **Lo que mi laptop puede ver, Claude puede ver si lo pide.** Pero hay 6 candados que le hacen muy difícil llegar a los secretos. Te los explico uno por uno.

### La analogía para entender la situación

Imagina que Claude es un asistente humano que trabaja en mi oficina. **Puede ver lo que tengo encima del escritorio.** Pero los documentos sensibles no viven en el escritorio — viven en una caja fuerte. La caja se abre con una llave que tengo yo (no Claude). Cuando saco un documento para usarlo, queda 10 segundos encima del escritorio, lo uso, y lo guardo. Si en ese momento Claude está mirando, podría verlo — por eso hay reglas que se lo prohíben. Y un guardia en la puerta lo revisa cada vez que intenta entrar a la caja directamente, y lo bloquea.

Eso es lo que pasa, traducido a los 6 candados:

### Los 6 candados, en orden

1. **Candado 1 — La caja fuerte (encriptación en reposo).** El archivo de secretos (`secrets.env.age`) vive cifrado en el disco. Claude ve bytes incomprensibles. Para descifrarlo necesita una llave privada que vive solo en mi laptop, NO en el repo.

2. **Candado 2 — Espacio temporal en RAM.** Cuando un secreto se necesita (ej. llamar a la API de Anthropic), se descifra a una "pizarra de memoria" — un área de RAM que se borra al apagar el computador y nunca toca el disco duro. El secreto vive ahí 1-2 segundos, se usa, se borra.

3. **Candado 3 — Guardia en la puerta (hooks).** Claude Code tiene un mecanismo donde le decimos: *"si Claude intenta abrir cualquier archivo cuyo nombre contenga `secrets` o termine en `.age`, abortar y avisarme."* **Esto no depende de la buena voluntad de Claude — es un muro a nivel del programa.**

4. **Candado 4 — Reglas escritas (CLAUDE.md).** Al inicio de cada sesión, Claude lee instrucciones que dicen: *"nunca leas archivos de secretos, nunca pegues API keys en respuestas."* Es honor system, pero combinado con el candado 3 es robusto.

5. **Candado 5 — Permisos del sistema operativo.** El archivo de secretos pertenece a un usuario aparte del que usa Claude. A nivel de Linux, Claude literalmente no tiene permiso de leer ese archivo. Es como un empleado sin pase a un piso restringido — la puerta no abre, no importa si quiere entrar.

6. **Candado 6 — Rotación trivial.** Si algún día sospechamos que algo se filtró, cambiar la API key toma 30 segundos en el dashboard de Anthropic. Las llaves no son secretos eternos — son revocables. Limita el daño máximo a "lo que se gastó entre la filtración y la rotación."

### ¿Qué pasa con los prompts que sí van a Anthropic?

Cada cosa que escribimos en una sesión, y cada archivo que Claude lee, viaja cifrado por internet (HTTPS) a Anthropic para que el modelo lo procese. Tres cosas importantes:

- **Anthropic NO entrena modelos con tu tráfico** (compromiso comercial de la API).
- **Retención de ~30 días** para fines operacionales (debugging, detección de abuso).
- **Existe un plan "Zero Data Retention"** para clientes enterprise — no guarda nada. Lo pedimos cuando tengamos primer cliente con compliance estricto.

Punto clave: **los secretos nunca se mandan como parte de un prompt.** Solo el código que los usa, no los valores.

### Resumen para JP

> **¿Puede Claude "ver" el `.env`?** No — está cifrado, el guardia lo bloquea, los permisos del sistema lo impiden. **¿Podría verlo si rompiera todos los candados al mismo tiempo?** Habría que romper 4 de los 6 en simultáneo, y el intento quedaría registrado en el billing de Anthropic (audit trail). **No es seguridad hermética, pero sí seriamente defendida.**

**[ENMIENDA v2 → v3]:** Agregar sección **Modelo de amenazas + capas de defensa** al capítulo de Cimientos, con esto explicado (incluyendo la analogía).

---

## 3. Notion — ya lo estás pagando, lo podemos usar

**Aceptado.** Cambia la sección de Stack:

| Antes (v2) | Después (v3) |
|------------|--------------|
| Notion — Paid (línea propia del proyecto) | Notion — Paid (cuenta de JP, compartida con la compañía) |

**Implicaciones:**
- **Workspace ownership:** mientras tú pagas, tú eres dueño del workspace. Cuando la compañía tenga entity legal + tarjeta corporativa, transferimos billing a la compañía (no migración de datos, solo cambio de cobranza).
- **Acceso:** ambos como admins. Futuros contratistas o clientes externos entran como guests con permisos limitados.
- **Punto de auditoría:** una vez al trimestre revisamos quién tiene acceso a qué workspace y limpiamos.

**Beneficio inmediato:** elimina ~USD 10/mes de la cuenta de Stage 1.

**[ENMIENDA v2 → v3]:** Stack inventory actualizado. Costo mensual revisado abajo en sección de Costos.

---

## 4. Grabaciones — usemos los transcripts/resúmenes de Notion en vez de Whisper

**Aceptado con dos backstops.** Tu argumento es bueno: ya pagamos Notion, ya hay workflow probado, menos infra que mantener, y la disciplina de revisión inmediata es justo lo que el sistema necesita.

### Decisión actualizada

- **Default:** transcripts + resúmenes vía Notion AI Meeting Notes. Revisión obligatoria inmediatamente después de cada llamada (regla codificada).
- **Whisper.cpp:** baja de Stage 1 a **Stage 2 condicional** — se activa solo si: (a) un cliente exige procesamiento self-hosted por NDA, (b) Notion cambia precios o cierra la feature, (c) queremos transcribir audio que no pasó por Notion.

### Dos backstops importantes

1. **Exportar a nuestro repo después de revisar.**
   Después de que revisas el resumen en Notion, exportas a `clients/<cliente>/transcripts/YYYY-MM-DD_<topic>.md`. Esto:
   - Nos da copia propia (no dependemos de Notion para siempre)
   - Lo hace searchable vía `grep` en el repo
   - Permite que skills/agentes lo lean como contexto en pipelines posteriores
   - Crea audit trail en git con timestamp y autor de la revisión

2. **Política de audio.**
   Notion guarda el audio durante un tiempo (varía por plan). **Regla:** después de revisar el resumen, borrar el audio en Notion si no hay razón explícita para retenerlo. Justificaciones para retener: cliente lo requiere, evidencia legal, llamada de descubrimiento clave. Default: borrar.

### Curiosidad técnica — ¿por qué los transcripts salen en inglés?

Probablemente uno de tres motivos:
- **Setting del workspace:** "AI default language" está en English. Cambiar a Spanish en workspace settings.
- **Setting por página:** las plantillas de meeting notes pueden traer language sobreescrito. Revisar en la plantilla.
- **Detección automática fallida:** si la primera frase de la grabación no tiene acento claro, Notion detecta wrong language. Configurar manualmente en la página.

**Próximo paso pequeño:** cuando me muestres tu workflow, le revisamos el setting de idioma. Si lo arreglamos, el transcript también sale en español y el resumen no tiene que ser la única salida usable.

### Regla de protocolo

**[ENMIENDA v2 → v3]:** Agregar a `00_GOVERNANCE/meeting-protocol.md`:

> 1. Grabar reunión con Notion AI Meeting Notes.
> 2. **Inmediatamente al colgar** (≤15 min): revisar resumen, corregir errores, completar contexto que falta.
> 3. Exportar el resumen revisado a `clients/<cliente>/transcripts/` (o `00_META/transcripts/` si es interna).
> 4. Decidir destino del audio en Notion: retener (con razón anotada) o eliminar.

---

## 5. "Me gustaría revisar el documento juntos paso a paso"

**Confirmado.** Es la mejor manera de cerrar esta ronda.

### Propuesta de formato

- **Duración estimada:** 60-90 min.
- **Modalidad:** sesión guiada, yo conduciendo el HTML en pantalla compartida, sección por sección.
- **Tu rol:** interrumpir libremente. Cualquier "no entiendo X" es input válido.
- **Output esperado al final:**
  - Decisión sobre **interfaz** (Heavy / Hosted / Light)
  - Decisión sobre **aprobación general** (acepto / acepto con ediciones / declino)
  - Lista escrita de **ediciones específicas** para v3 (todo lo de este documento + lo que salga en la sesión)
- **Después de la sesión:** firmamos la v3 (no la v2). La v3 incorpora todas las enmiendas marcadas en este documento + las que salgan del walkthrough.

### Material de apoyo en el walkthrough

Tengo preparado un guion interno por sección. No es para ti — es mi guía de presentador para no leerte las slides. Tú vas a tener:
- El HTML en pantalla
- Este documento (respuestas + FAQ) abierto a un lado por si entras a una pregunta que ya está aquí
- Tu lista de notas/ediciones que vamos a ir escribiendo en vivo

**Próximo paso:** dime dos o tres ventanas de tiempo esta semana y te confirmo.

---

# Parte 2 · FAQ — Preguntas anticipadas

Organizadas por tus 5 preocupaciones principales. Tabla rápida arriba; detalle abajo.

## Privacidad

### ¿Qué datos salen de nuestra infraestructura?

Tres flujos hacia afuera:
1. **A Anthropic** (Claude API): prompts y archivos que el agente lee durante una sesión. Términos comerciales: no se usan para entrenar, retención ~30d.
2. **A Notion** (cuando guardas algo allí): notas, transcripts, resúmenes, contenido de páginas. Notion términos enterprise/business — datos del cliente no se usan para entrenar IA general.
3. **A GitHub/Codeberg** (mirrors de git): todo el contenido del repo cifrado en tránsito (HTTPS) pero **plaintext en reposo en GitHub**. **Esto es importante** — ver siguiente pregunta.

### Si GitHub guarda el repo en plaintext, ¿no se ve todo?

GitHub guarda lo que está **plaintext en el repo** — código, markdown, JSONs no sensibles. Lo sensible (`*.age`, `vault/.encrypted/`) está cifrado **antes** de llegar a git, así que GitHub solo ve los ciphertexts. Los empleados de GitHub no pueden leer nada sensible sin nuestras llaves age. Es el mismo principio que un email cifrado con PGP — pasa por servidores que no pueden leerlo.

### ¿Anthropic guarda nuestros prompts? ¿Por cuánto?

- **API estándar:** retención operacional típica ~30 días, sin entrenamiento de modelos.
- **Zero Data Retention (ZDR):** disponible en planes enterprise. No retiene nada. **Vale la pena pedirlo cuando tengamos primer cliente con compliance estricto.**
- **Para uso interno (sin datos de cliente):** retención estándar es aceptable.

### ¿Los clientes pueden ver lo que escribimos sobre ellos?

**No por default.** El folder `clients/<cliente>/` vive en nuestro repo privado. Solo tú y yo tenemos acceso.

Lo que el cliente **sí** ve: los entregables formales que le mandamos (DOCX, PDF) — están en `clients/<cliente>/05_reporte_oportunidades/`. Notas internas, guion de reunión (Skill 4 explícitamente marcado como **privado**), análisis crudos: el cliente nunca los recibe.

**Disciplina:** cualquier archivo destinado al cliente pasa por PR + aprobación (regla de Cimientos #4). Así evitamos accidentes tipo "compartí una nota interna por error".

### ¿Y NDAs de clientes? ¿Dónde viven?

- Original firmado (PDF/DOCX): en el vault encriptado → `/srv/brain-sensitive-mount/01_VENTURES/04_MejiaIACia/clients/<cliente>/nda/`.
- Índice plaintext (qué existe, cuándo se firmó, scope): `clients/<cliente>/legal/nda_index.md` en el repo.
- Acceso: solo nosotros dos. Si un futuro contratista necesita ver, decisión explícita caso por caso.

### ¿Implicaciones de compliance (LFPDPPP México, GDPR, LGPD)?

Resumen rápido:

| Régimen | Aplica si | Acción nuestra |
|---------|-----------|----------------|
| **LFPDPPP** (México) | Cliente o sus datos están en México | Aviso de privacidad estándar + ARCO rights documentados. Plantilla en `templates/legal/`. |
| **GDPR** (UE) | Cliente o sus datos están en UE | Más estricto. DPA (data processing agreement) con cada cliente + análisis de transferencias internacionales (Anthropic, Notion están en US — Standard Contractual Clauses aplica). |
| **LGPD** (Brasil) | Cliente brasileño | Similar a GDPR, menos estricto en transferencias. |
| **Habeas Data** (Colombia) | Cliente colombiano | Régimen propio, parecido a LFPDPPP. |

**Acción inmediata:** ninguna, hasta que tengamos primer cliente real. Cuando llegue, evaluamos el régimen aplicable y firmamos los DPAs necesarios. Tenemos `00_GOVERNANCE/compliance-checklist.md` como recordatorio para no olvidar.

---

## Seguridad

### ¿Qué pasa si me roban la laptop?

Tu laptop tiene: tu llave privada `age`, tu clone del repo, cookies de Notion/Gitea, sesión de Claude Code.

**Lo que se hace en el momento (orden de prioridad):**
1. **Te aviso o me avisas inmediatamente** (Telegram, llamada, lo que sea más rápido).
2. **Revoco tu llave age** (revocación de emergencia, sección 1).
3. **Re-encripto el vault hacia adelante** sin tu llave.
4. **Roto secretos críticos**: API key de Anthropic, tokens de GitHub, password de Gitea, etc.
5. **Invalido sesiones**: Notion logout de todos los devices, Telegram logout sessions.
6. **Generas nueva llave** desde un device limpio. Agregamos pública al repo. Re-encriptas tu acceso al vault.

**Mitigación previa para reducir daño:**
- **Full Disk Encryption (FDE)** habilitada en la laptop. Si la encienden, no entran sin password.
- **Auto-lock corto** (5 min). Pantalla bloqueada = laptop dura.
- **Llave age con passphrase** (no llave desnuda). Aunque tengan el archivo, sin passphrase no descifran nada.

### ¿Y si comprometen el servidor?

Servidor de Ricardo en Tijuana. Si lo comprometen totalmente:
- **Repo:** está mirroreado a GitHub + Codeberg. No se pierde código.
- **Vault encriptado:** copia en mi laptop, copia en tu laptop, copias en mirrors. No se pierde data.
- **Llaves age privadas:** **NO están en el servidor**. Viven solo en nuestras laptops. El atacante puede ver todo el ciphertext del vault pero no descifrar nada.
- **Secretos en plaintext en runtime:** posibles en RAM mientras procesos corren. Si el server cae, mitigación: rotar todos los secretos sospechosos.
- **Bot:** desde otro servidor cualquiera lo volvemos a levantar en horas con el repo restaurado.

**Tiempo de recuperación realista (RTO):** 24-48h para reconstruir el servidor en otro host. Cero pérdida de datos (RPO ~minutos, lo que tarde el último push).

### ¿Y si la API key de Anthropic se filtra?

- **Detección:** factura inesperada de Anthropic, o alertas si configuramos límite de gasto. Anthropic permite hard cap mensual.
- **Acción inmediata:** rotar la key (30 seg en el dashboard). Actualizar `secrets.env.age`. Push.
- **Daño máximo:** lo que se haya gastado entre filtración y rotación, hasta el hard cap.

**Mitigación previa:** hard cap configurado en Anthropic dashboard (ej. USD 500/mes). Ningún atacante quema más que eso antes de que lo notemos.

### ¿Quién puede leer nuestro repo en GitHub?

- **Repo privado** en GitHub bajo la org `mejia-ia-cia`. Solo miembros de la org pueden leer.
- **Miembros iniciales:** tú y yo, como owners.
- **Empleados de GitHub:** legalmente no leen contenido de repos privados sin orden judicial. Técnicamente pueden si tienen acceso interno; por eso, todo lo sensible está cifrado **antes** de llegar al repo.
- **Mirror automático:** mismo nivel de privacidad (repo destino también privado).

### ¿2FA en todas las cuentas?

Sí, obligatorio. Lista de cuentas con 2FA desde día uno:
- GitHub (org + personal)
- Codeberg
- Notion
- Anthropic console
- Google (Drive, Meet, Gmail asociado)
- Cal.com
- Gitea (selfhosted — 2FA habilitado para usuarios)

**Recovery codes:** guardados en el vault encriptado, no en el celular ni en notas. Si pierdo el celular, los recovery codes me sacan.

### ¿Los respaldos en GitHub/Codeberg están encriptados?

- **En tránsito:** sí, HTTPS.
- **En reposo:** GitHub/Codeberg guardan los bytes que les mandas. Si mandas `vault.age` (cifrado), guardan ciphertext. Si mandas `report.md` (plaintext), guardan plaintext.
- **Regla:** nada sensible llega plaintext al repo. Cifrado antes de commit. **Esa es la arquitectura entera.**

---

## Escalabilidad

### ¿Qué pasa cuando tengamos 10 clientes? ¿50?

| Volumen | Qué pasa | Acción |
|---------|----------|--------|
| 1-5 clientes | Estado actual diseñado. Cero fricción. | Nada. |
| 5-15 clientes | El bot empieza a tener traffic. `events.jsonl` crece, sigue siendo manejable (~MB). | Empezar a archivar `events.jsonl` mensualmente (rotación a `events-YYYY-MM.jsonl.gz`). |
| 15-50 clientes | Notion CRM se llena. Bot puede saturarse si todos los clientes interactúan a la vez. | Stage 2 trigger: CRM upgrade evaluado (HubSpot/Pipedrive). Considerar un worker queue para el bot. |
| 50+ clientes | Estamos en otro régimen: tenemos equipo, no somos dos. | Refactor mayor — multi-operador, roles, permisos granulares. |

**El sistema está diseñado para llegar fluidamente hasta ~15-20 clientes activos. Más allá, hay refactors específicos pero conocidos.**

### ¿`events.jsonl` se vuelve lento?

Cálculo: ~100 eventos por cliente por mes × 20 clientes activos = 2000 líneas/mes = ~500KB/mes. Después de 1 año = ~6MB. `tail -f`, `grep`, helpers en Python — todos manejan ese tamaño sin sudar.

**Cuando justifique:** rotación mensual a archivos comprimidos. Helpers leen del archivo activo + archivo del mes anterior por default. Más antiguo solo si se pide explícito.

### ¿2TB de Drive es suficiente?

Cálculo rough: cada cliente genera ~1-5GB de audio + PDFs durante un ciclo de Diagnóstico. 20 clientes ≈ 40-100GB. **2TB nos da margen para 200-400 clientes históricos.**

Cuando lleguemos a 1.5TB usado, Stage 2 trigger: Backblaze B2 o Cloudflare R2 para offload del archivo histórico (~USD 6/TB/mes, mucho más barato que escalar Drive).

### ¿Y si entra un tercer socio o empleado?

- **Llave age** propia (agregada a `recipients.txt` vía PR aprobado por ambos).
- **Acceso al repo** (invitación a la org en GitHub/Gitea).
- **Persona en Notion** como member o guest según rol.
- **Permisos del bot:** se agrega a allowlist con su chat_id.
- **Permisos en el repo:** ramas protegidas, PR requerido para tocar carpetas críticas. El nuevo no toca `00_GOVERNANCE/` ni `secrets.*` sin aprobación.

**Tiempo de onboarding:** medio día para Heavy, 30 min para Light. Documentado en `00_GOVERNANCE/onboarding.md`.

### ¿Cuándo se justifica saltar a Stage 2?

Tabla:

| Trigger | Stage 2 que se activa |
|---------|----------------------|
| Primer cliente firma contrato escrito | DocuSign |
| Primera factura enviada | Stripe |
| Drive 2TB pasa 80% | Backblaze B2 o R2 |
| Un usuario elige modo Hosted | code-server |
| Pipeline > 15 clientes activos | CRM upgrade evaluado |
| Web pública prioritaria | Sitio en producción |

**Cada uno se evalúa cuando llega su trigger, no antes.**

---

## Despliegue en otras máquinas

### ¿Puedo trabajar desde mi computador de casa Y oficina?

**Sí, sin importar el modo (A/B/C).**

- **Modo C (Light):** literalmente cualquier navegador + Telegram. Funciona en cualquier device sin instalar nada.
- **Modo B (Hosted):** instala Tailscale en cada device (5 min). Login en navegador. Listo.
- **Modo A (Heavy):** instala Claude Code, Gemini CLI, clone del repo, importa tu llave age. Toma ~1h por máquina, pero después funciona igual en todas. Tu llave age tiene que estar en cada device — la copias vía vault o vía canal seguro.

### ¿Y desde el celular?

- **Modo C (Light):** la propuesta está diseñada para esto. Telegram en el celular + Gitea web en el navegador del celular. Funciona.
- **Modo B (Hosted):** posible (Tailscale + navegador móvil) pero la UX no es buena. Editar archivos largos en celular es doloroso.
- **Modo A (Heavy):** no aplica — Claude Code no corre en iOS/Android.

**Resumen práctico:** desde el celular, todos terminamos usando Telegram como interfaz. Modo C lo hace explícito.

### ¿Y si viajo?

Sin problema:
- Modo C: Telegram + Gitea web funcionan en cualquier conexión.
- Modo B: Tailscale funciona desde cualquier red (es VPN, no requiere puerto abierto en el servidor).
- Modo A: solo necesitas tu llave age con passphrase. Si pierdes la laptop en el viaje, ver "qué pasa si me roban la laptop".

### Editamos los dos al mismo tiempo, ¿qué pasa?

**Cuando ambos usamos modo Heavy:** git maneja merges. Si editas un archivo distinto al mío, ambos commiteamos y un `git pull --rebase` integra sin conflicto. Si editamos el mismo archivo en la misma línea, hay conflicto explícito y lo resolvemos.

**Si uno usa Heavy y otro Light:** vía Gitea web editas archivos directamente (con commits inline). El otro hace `git pull` y ve tu cambio. Cero conflicto si no chocamos en el mismo archivo.

**Disciplina sugerida:** "edit shouting" — si vas a tocar `00_GOVERNANCE/` o un archivo crítico, anuncias en el grupo de Telegram. 5 segundos de aviso evitan 30 min de merge conflict.

### ¿Los clientes acceden a algo nuestro?

**No directamente.** Su contacto con nuestro sistema es vía entregables formales (DOCX, PDF que les mandamos por email/Drive link). Ninguno tiene acceso al repo, al bot, a Gitea, a Notion.

**Excepción futura — portal de cliente:** si en algún momento queremos que el cliente vea su estado en tiempo real, construimos un portal aparte que lea de nuestro sistema pero exponga solo lo público. **No es prioridad ahora.**

---

## Costo

### ¿Cuánto cuesta operar Stage 1 al mes?

Con la enmienda de Notion (tu cuenta, no nueva):

| Item | Costo USD/mes | Comentario |
|------|---------------|------------|
| Claude Code (Anthropic) | ~$20-60 | Escala con uso; hard cap configurable |
| Notion | $0 | Cuenta de JP, compartida |
| Google Drive 2TB | ~$10 | Activos pesados |
| Dominio (cuando se compre) | ~$1 | Amortizado mensual |
| GitHub, Codeberg, Gitea, Cal.com, Whisper, age, Pandoc, OBS | $0 | Free / open source / selfhosted |
| Bot Telegram | $0 | API gratuita |
| **Total Stage 1** | **~$31-71/mes** | |

**Hasta que haya revenue, esto sale de bolsillo de Ricardo (operador principal) o se prorratea entre los dos según acuerdo de partnership.**

### ¿Costo marginal por cliente?

Por cliente activo en pipeline:
- **Claude tokens:** ~USD 5-15 por cada Diagnóstico completo (5 skills × ~$1-3 cada uno).
- **Drive storage:** ~0.5GB de audio/PDFs × ~USD 0.005/GB-mes = despreciable.
- **Notion AI:** incluido en el plan plano (no es per-user de pago variable).

**Costo total marginal por cliente Diagnóstico:** ~USD 5-15.

A Diagnóstico de venta proyectado USD 1500-3000 (sujeto a confirmar precio con mercado), margen bruto por skill es altísimo. **El cuello de botella es nuestro tiempo, no el costo.**

### ¿Cuándo activamos Stage 2 y cuánto suma?

Por trigger (estimaciones cuando se activen):

| Stage 2 item | Costo USD/mes | Trigger |
|--------------|---------------|---------|
| Codeberg | $0 | "Cuando me cuadre la tarde para configurar" |
| Backblaze B2 | ~$6/TB | Drive > 1.5TB |
| Bitwarden | $0 (Free) o $3 (Premium) | Logins compartidos rutinarios |
| code-server | $0 (selfhosted) | Si JP elige modo Hosted |
| DocuSign | ~$10-25 | Primer contrato |
| Stripe | 2.9% + $0.30 por transacción | Primera factura |
| CRM upgrade | $30-100 | Pipeline > 15 clientes |
| Sitio público | $0 (selfhosted) | Cuando sea prioritario |

**Patrón:** Stage 2 sube el costo de forma proporcional al revenue. Si pagamos USD 25 de DocuSign es porque ya tenemos contrato firmado. Si pagamos USD 100 de CRM upgrade es porque tenemos 15+ clientes activos.

### ¿Hay costos escondidos?

Voy a ser explícito con todo lo que NO está en la tabla pero podría aparecer:

- **Hardware del servidor:** ya existe (de Ricardo), pero si falla en 5 años, reemplazo ~USD 800-2000.
- **NAS local:** ya existe (de Ricardo), reemplazo ~USD 500-1500.
- **Electricidad servidor + NAS:** ~USD 10-20/mes en factura de luz (asorbido por Ricardo como infra personal).
- **Internet residencial:** ya pagado por Ricardo. Si se vuelve cuello de botella, fibra dedicada ~USD 100/mes adicional.
- **Tiempo no remunerado de Ricardo:** durante pre-revenue, todo el trabajo de operador es free. Capturado en el partnership como equity, no como gasto.
- **Llamadas internacionales / móviles:** si trabajamos con clientes en LatAm/España, número virtual ~USD 5-10/mes.
- **Contador / legal cuando se constituya la entity:** ~USD 200-500 setup one-time + ~USD 50-100/mes ongoing. **Esto sí es item real, no infra.**

**Costo realista pre-revenue:** ~USD 40-80/mes operativo + ~USD 200-500 one-time si formalizamos entity este año.

### ¿Cuándo break-even?

Si Diagnóstico se vende a USD 2000 (precio referencial conservador):
- **Costos fijos mensuales** ~USD 60.
- **Un Diagnóstico cubre 33 meses de costos fijos.**

**Break-even práctico = primer Diagnóstico pagado.** A partir de ahí, cada Diagnóstico adicional es ~95% margen contributivo (descontando solo nuestro tiempo + ~USD 15 de tokens).

**El número que importa no es break-even — es velocidad para llegar al primer pagado.** La roadmap dice: Aprobación (hoy) → Scaffold + Skills 2-5 paralelo (2-3 semanas) → piloto sin cobro (4-6 semanas) → primer pagado cuando calidad sea 8/10 estable. **Realista: 2-3 meses al primer ingreso.**

### ¿Quién paga qué hasta que haya revenue?

**Propuesta para discutir (entra como tema en el walkthrough):**

| Item | Quién paga ahora | Por qué |
|------|------------------|---------|
| Claude Code, Drive 2TB | Ricardo | Operador principal, ya tiene cuenta |
| Notion | JP | Ya lo pagas |
| Dominio cuando se compre | Compartido 50/50 o Ricardo (decidimos) | Activo de la compañía |
| Hardware servidor/NAS | Ricardo | Es infra personal preexistente |

**Cuando haya revenue:** todo migra a billing corporativo. Quien adelantó costos se reembolsa con primer ingreso o se incorpora al cálculo de equity.

**[ITEM PARA WALKTHROUGH]:** formalizar este split de costos pre-revenue en el `00_PARTNERSHIP/cost-sharing-agreement.md`.

---

# Parte 3 · Plan dual de herramientas — pagadas hoy + libres en paralelo

> **Lo nuevo desde la propuesta v2.** Esto reemplaza la sección de Stack actual con un enfoque ampliado.

## La idea en una línea

Usamos las herramientas pagadas que ya conocemos para trabajar bien hoy. **En paralelo**, instalamos las versiones libres en nuestro servidor — sin tráfico crítico — para aprender a operarlas. **Cuando estén maduras, las ofrecemos a clientes** como alternativa más barata y soberana.

Es la misma lógica de "eat your own dogfood" que ya estaba con Odoo, pero extendida a todas las categorías de software que usamos.

## Por qué hacerlo así (4 razones)

1. **Vendemos lo que sabemos operar.** Las PyME en LatAm no quieren pagar suscripciones SaaS gringas para siempre. Si nosotros sabemos instalar Nextcloud o Anytype en su servidor, vendemos esa instalación + capacitación + soporte como un servicio nuestro. Y como ya lo operamos internamente, lo sabemos hacer bien.

2. **Probamos antes de prometer.** No le decimos a un cliente "Jitsi es como Meet pero gratis" sin haberlo usado nosotros mismos por meses. Sin uso interno, la promesa suena a venta — pierde credibilidad.

3. **Reducimos vendor lock-in.** Si Notion sube precio 5× el próximo año, nosotros migramos en una semana porque ya tenemos Anytype o AppFlowy operando en paralelo con nuestros datos.

4. **Credibilidad real frente al cliente.** Cuando un cliente pregunta "¿tú usas lo que me estás vendiendo?", la respuesta es **"sí, hace meses"**, no "lo probé un fin de semana".

## Cómo se opera el plan dual (paso a paso)

- **Producción (primary):** la herramienta pagada o conocida. Lo que usamos para trabajo real con clientes, sin riesgo. **Notion, Drive, Meet, Claude Code.**
- **Shadow (secondary):** la herramienta libre, desplegada en paralelo en nuestro servidor. Sin tráfico crítico. La usamos para:
  - Notas internas no críticas
  - Experimentos
  - Transcripciones de prueba (comparar contra Notion AI)
  - Subir habilidades operativas reales
- **Decisión de migración:** cuando la herramienta libre llega a **≥80% de paridad funcional** en nuestros flujos críticos (medido honestamente, no a ojo), evaluamos cambio. Si migramos, lo hacemos lentamente, no de golpe.
- **Oferta al cliente:** cuando un cliente pregunta por alternativa más barata a un SaaS, le ofrecemos:
  - El software libre (gratis para él)
  - **Deployment + capacitación + soporte (servicio nuestro, billable)**

## Pares de herramientas — qué entra a shadow

| Categoría | Hoy (producción) | Mañana (shadow libre) | Costo del shadow |
|-----------|------------------|----------------------|------------------|
| CRM + docs colaborativos | Notion | **Anytype** o **AppFlowy** | $0 |
| Transcripción + resumen | Notion AI | **Whisper.cpp** + **Ollama** local | $0 |
| Activos pesados | Google Drive 2TB | **Nextcloud** en NAS | $0 |
| Reuniones video | Google Meet | **Jitsi Meet** self-hosted | $0 |
| Agente IA primario | Claude Code (Anthropic) | **Ollama** (Llama 3, Qwen 2.5, etc.) | $0 |
| Firmas electrónicas | DocuSign (Stage 2) | **Documenso** self-hosted | $0 |
| Pagos | Stripe (Stage 2) | N/A — pagos necesita proveedor regulado | — |
| Calendario | Cal.com (ya self-hosted) | — | ya cubierto |
| Git origin | Gitea (ya self-hosted) | — | ya cubierto |

## Cronograma de deploy del shadow (Stage 1 ampliado)

Esfuerzo total: ~5-7 días repartidos en 4 semanas. Todo en nuestro servidor existente.

| Semana | Despliegue | Esfuerzo |
|--------|-----------|----------|
| Sem 1 | **Nextcloud + Jitsi Meet** | ~1 día (ambos vienen como docker compose) |
| Sem 2 | **Ollama + 2-3 modelos locales** (Llama 3, Qwen 2.5, Mistral) | ~1 día |
| Sem 3 | **Whisper.cpp** + pipeline reunión → transcript → resumen local | ~1-2 días |
| Sem 4 | **Anytype o AppFlowy** (elegimos uno después de probar ambos) | ~1 día |
| Sem 5-12 | Uso en shadow + documentación honesta de pros/cons por herramienta | difuso, ~2-4 h/semana |

**Costo monetario total del shadow: USD 0.** Hardware ya existe (servidor + NAS). Software todo libre. Solo cuesta tiempo.

## Service line — qué le ofreceríamos al cliente cuando madure

Después de ~6 meses de operación interna del shadow, estos servicios entran a nuestra oferta:

| Servicio al cliente | Qué incluye | Ticket aproximado |
|---------------------|-------------|-------------------|
| Migración **Notion → Anytype/AppFlowy** | Migración workspaces, capacitación, soporte 30d | USD 800-1500 |
| Migración **Google Drive → Nextcloud** | Deploy en su servidor o cloud + migración + capacitación + soporte 30d | USD 1200-2500 |
| Reuniones **Meet → Jitsi** | Deploy Jitsi self-hosted, capacitación, integración con calendario | USD 600-1200 |
| **Transcripción local** (Whisper + Ollama) | Deploy del pipeline + capacitación al equipo cliente | USD 800-1500 |
| **ERP Odoo Community** | (Ya en la propuesta como servicio) | USD 5K-25K |

**Implicación estratégica:** cada categoría de SaaS gringo se convierte en una posible línea de servicio nuestra. Lo que pagamos como suscripciones se transforma en lo que cobramos como servicios.

## Lo que este plan NO promete (por honestidad)

- **No todas las herramientas libres alcanzan paridad.** Notion AI Meeting Notes es muy pulido; Whisper + Ollama no va a estar igual desde el día uno. Documentamos el gap honestamente — si un cliente necesita el nivel de Notion AI, le decimos.
- **El tiempo de shadow compite con tiempo de cliente.** Cuando entren clientes pagos, el shadow se desacelera. Mantenemos cadencia mínima (~2 h/sem) para no perder el músculo.
- **Algunas categorías no aplican.** Pagos electrónicos no tienen alternativa self-hosted real — siempre habrá un Stripe o un Mercado Pago detrás. No prometemos lo que no se puede.
- **Hardware tiene límite.** Si los modelos de Ollama exigen GPU que no tenemos, ese item se queda en "experimento" hasta que el ROI justifique comprarla.
- **Pregunta esperada del cliente — "¿por qué tú usas Notion entonces?"** Respuesta honesta: porque ya teníamos el workflow montado y migrar tiene costo. **Lo que sí prometemos es saber cómo hacer la migración suya** — sabemos los puntos de dolor porque los enfrentamos en paralelo.

## Decisión que esto requiere de JP

Una sola, simple: **¿Aprobamos el plan dual desde Stage 1?**

- **Sí:** los shadows entran al cronograma de scaffold. ~5-7 días de mi tiempo en las primeras 4 semanas.
- **No / Después:** mantenemos solo lo pagado por ahora, y reabrimos esta conversación cuando se justifique.

**Mi recomendación: sí.** El costo es solo tiempo y el upside (línea de servicio + credibilidad + reducción de lock-in) es alto y temprano.

---

# Enmiendas aplicadas en v3 del HTML

Todos los cambios listados abajo **ya están aplicados** en `2026-05-12_jp-presentation-v3.html`. Esta lista existe para que puedas auditar — leyendo este documento de respuestas y luego la v3, deberías poder verificar que cada enmienda quedó reflejada.

1. **Cimientos · card Vault:** reescrito con analogía de **caja fuerte**. Documenta protocolo de revocación de emergencia (unilateral) vs rotación rutinaria (PR + aprobación). Nota explícita: commits viejos siguen desencriptables con llaves comprometidas — rotar secretos críticos también, no solo re-encriptar.
2. **Cimientos · NUEVO sub-bloque "Los 6 candados":** sub-sección completa al final de Cimientos. 6 cards explicando candado por candado (caja fuerte, pizarra de memoria, guardia, reglas, permisos, rotación) + 2 callouts (Anthropic ZDR + resumen). Con la analogía del asistente humano.
3. **Cimientos · card Secretos:** reescrito con paso a paso de "pizarra de memoria" (RAM) — 3 pasos: descifra → usa → borra.
4. **Personas · events.jsonl:** lenguaje suavizado con analogía de "cuaderno de bitácora de un barco" + "sistema nervioso".
5. **Stack — actualizaciones:** Notion ahora "$0 · cuenta de JP". Whisper.cpp removido de Stage 1 (se movió al plan dual como shadow). Callout final enlaza al nuevo "Plan dual".
6. **NUEVA sección · Plan dual de herramientas** (entre Stack y Odoo): por qué + cómo + tabla de 9 pares producción↔shadow + cronograma de 4 semanas + callout de honestidad sobre lo que NO promete.
7. **Odoo · reframe:** Odoo deja de ser caso aislado — primer ejemplo de la familia "Servicios". Quote final enlaza a la nueva sección.
8. **NUEVA sección · Servicios** (después de Odoo): catálogo de 5 líneas de servicio con tickets aproximados (Notion→Anytype USD 800-1500, Drive→Nextcloud USD 1.2-2.5K, Meet→Jitsi USD 600-1.2K, Whisper local USD 800-1.5K, Odoo USD 5-25K). Callout "¿Por qué tú usas Notion entonces?".
9. **Camino · paso 2 ampliado:** "Scaffold + Skills 2-5 + **shadows del plan dual** (paralelo)".
10. **Otras decisiones · #2 grabaciones:** marcada como **CERRADA por JP** con badge verde. Texto explica decisión: Notion AI + revisión inmediata + export a repo + política de audio.
11. **Otras decisiones · NUEVO #1 Plan dual:** aprobar Stage 1 / después / solo Odoo.
12. **Otras decisiones · NUEVO #6 Split de costos pre-revenue:** Ricardo paga Claude + Drive + hardware. JP aporta Notion. Dominio + legal por definir.
13. **Hero, navbar, footer:** actualizados a v3 · 2026-05-12. Navbar incluye "Plan dual" y "Servicios".
14. **Firma:** nuevo radio group `dual-choices` (aprobar / después / solo Odoo) registrado en el JS junto a interface-choices y approval-choices.
15. **¿Qué estás viendo?:** callout "Nuevo en v3" lista las novedades al inicio. Lenguaje más amigable con analogías.

**Items que el walkthrough todavía debe cerrar** (siguen abiertos en v3):
- Interfaz (Heavy / Hosted / Light)
- Aprobación general (acepto / amend / declino)
- **Plan dual** (Stage 1 / después / solo Odoo) — recomendación: Stage 1
- Posicionamiento de Odoo + línea de servicio en software libre
- Formalización del protocolo de sociedad
- Primer servicio pagado post-Diagnóstico
- Criterios del clasificador de prospectos
- Split de costos pre-revenue

**Pendientes documentales** (no entran al HTML, son archivos del repo a crear durante el scaffold):
- `00_GOVERNANCE/key-rotation-protocol.md` — protocolo de revocación
- `00_GOVERNANCE/meeting-protocol.md` — reunión → Notion AI → revisar → exportar a repo
- `00_PARTNERSHIP/cost-sharing-agreement.md` — split de costos pre-revenue
- `00_GOVERNANCE/compliance-checklist.md` — recordatorio LFPDPPP/GDPR/LGPD/Habeas Data cuando llegue primer cliente

---

*La v3 está lista para tu revisión. Cuando puedas, dame dos o tres ventanas esta semana para hacer el walkthrough en pantalla compartida.*
