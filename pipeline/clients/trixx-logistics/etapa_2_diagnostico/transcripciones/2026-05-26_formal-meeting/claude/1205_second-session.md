# Reunión Trixx 12:05 PM — Sesión 2 (deep-dive operativo + cierre comercial)

> **Tipo:** segunda sesión, ~31 min, deep-dive demo + cierre con propuesta comercial.
> **Fuente primaria:** `../whisperx/1205_second-session.txt` (WhisperX large-v3 + diarización, 4 voces detectadas).
> **Síntesis:** Claude (auto), basada en WhisperX + contexto de `04_prep_llamada/runs/2026-05-26_mode-a/` + `01_company_analysis/runs/2026-05-26_mode-a/`.

## Mapeo de hablantes

WhisperX detectó 4 voces. Mapeo según contenido y rol:

| WhisperX | Persona real | Evidencia |
|---|---|---|
| `SPEAKER_00` | **Ricardo Mejía** (Nexostrat) | Voz conductora consultora. Pregunta abierta sobre impedimentos. Cierre: *"A ver, si te doy 100% sincero, la compañía está empezando. Ustedes son nuestro primer cliente"*. María Helena le agradece nombrándolo: *"Muchas gracias Ricardo"*. |
| `SPEAKER_01` | **Héctor Leyva** (fundador) | Voz operativa-explicativa que recorre el sistema mostrando contenedores, fechas, bodegas, Vernon, tarifas. Detalle de 24 años de oficio. |
| `SPEAKER_02` | **María Helena** (decisora) | Voz cuantitativa de presión: *"yo le digo mucho arriba: la información tiene que estar en tres minutos"*, *"yo no sé si todos esos contenedores se arribaron"*, *"¿Cómo son tus honorarios?"*. Confirmado cuando Ricardo cierra dirigiéndose a *"María Helena"*. |
| `SPEAKER_03` | **Andrea Chávez** (hija, voz digital) | Pelea con el proveedor del hosting/web (Carlos). *"Tuvimos un Zoom y te lo cotizo y ya te pasé a ti el número"*. Acepta cruzar la frontera con Ricardo para visitar bodega. |

Luis **no aparece** en esta sesión (participó solo brevemente en la sesión 10:10).

## Contexto

Después del 10:10 (deep-dive relacional + visión panorámica), María Helena/Hector llevan a Ricardo a un segundo segmento operativo. Le muestran el sistema concreto que ya usan (**Tracking Premium**) para un cliente — un **cliente chino** que mueve contenedores Asia → puertos USA → cruce terrestre o tren → bodegas mexicanas. Sale al aire la pregunta clave: *"¿cuál es el impedimento más grande para que repliquen este sistema a todos los clientes?"*

## Bloque 1 — Demo del sistema Tracking Premium (~0-5 min)

**Hector recorre la plataforma con Ricardo.** Tracking Premium es un sistema externo de pago (plataforma SaaS) que actualmente usan **solo para el cliente chino**. Contiene:

- Por contenedor: número, kilos, número de cajas, total de mercancía, producto, cita del puerto, bodega de destino (Vernon o bodega externa contratada), origen.
- Status por contenedor: en mar, en puerto, en cruce, en bodega, retorno de vacío.
- Tarifas por cliente: fórmula `alto × largo × ancho ÷ {12, 14 o 6} × tarifa` (varía por cliente).
- Alimentación de datos: manual, vía correos que Luis (broker/US contact) envía con números de contenedor y tiempos de llegada.

**María Helena (SPEAKER_02):** *"el cliente al momento de hacer su contratación de la terminal, porque son varias terminales, pone los días [de retorno de vacío sin costo]. Entonces aquí se hace eso con el fin de estar pendiente."*

**Datos cuantitativos surgidos:**
- Cruces: Mexicali, San Luis Río Colorado–Sonora (en tren a CDMX), o terrestre Los Angeles → cruce.
- Andrea (SPEAKER_03): *"Yo estoy en ese [sistema], y nada más que saco información de ahí, más no, yo no entiendo"* → confirmación de la hipótesis session 19 de que Andrea NO domina la herramienta interna.

## Bloque 2 — El "impedimento" central: María Helena confiesa el bloqueo (~5-8 min)

**Ricardo (SPEAKER_00):** *"¿Y cuál es el impedimento más grande para ustedes poder empezar a implementar esta misma plataforma o un sistema similar con lo que tienen actualmente?"*

**María Helena:** *"He entrado como 10 veces a quererlo generar y me distraigo, no lo he hecho."*

→ **Anchor anchor anchor.** El bloqueo no es tecnológico, es de bandwidth ejecutivo. La decisora tiene la intención + el sistema disponible, y aún así no logra ejecutar. Esto es exactamente el tipo de pain que un acompañamiento Nexostrat resuelve. **Calza con el §4.2 del PrepLlamada (Excel→PDF CBP) elevado a un nivel: el bloqueo ejecutivo es transversal a múltiples procesos.**

Hector ofrece alternativa: trasladar todo a **Amundi** (mencionada como otra plataforma global de pago). María Helena: *"No, lo que había pensado es en transferirnos para Amundi porque lo fácil era copiar siempre esta información"*. Después se autocorrige: *"esta es una plataforma externa a la que se le tiene que pagar"*.

**Ricardo redirige:** *"hay muchas formas, ustedes podrían, se podría desarrollar, o pues nosotros podríamos desarrollar una plataforma que sea exclusiva de ustedes"* — primera mención clara de Nexostrat como proveedor potencial.

**María Helena pivotea (key turning point):** *"Sí, si hubiera una buena propuesta y pudiéramos hacerlo todo gradual, donde pudiéramos comunificar con la información, sería lo ideal, sería como una plataforma propia. Porque al final, por ejemplo, si yo no pago mañana el mes de Tracking Premium, te lo cortan. Y toda la información que se quedó ahí..."*

→ **Pain point #2 confirmado:** dependencia de plataforma SaaS de pago con riesgo de pérdida de datos si se cancela. Anchor para una propuesta in-house.

## Bloque 3 — Sprawl de información + cultura "todo en papel" (~8-15 min)

María Helena enumera el caos operativo, en cascada:

1. **Excel sprawl por persona.** *"Cada uno tiene su pedazo de la información... uno tiene tres camiones en una lista, otro tiene dos camiones en otra"*.
2. **Información no-buscable.** *"yo, la información tiene que estar en tres minutos. O sea, si se pide algo, en tres minutos me la tienes que dar. Si ahorita yo pido la relación de cajas y camiones, y se la pido a Miguel que la tiene, o si no estaba, nadie la tiene"*.
3. **Damián (broker US) — riesgo de fraude/error no detectable.** *"a Damián, la persona que saca las fianzas... me mandó una relación de todos los contenedores para que yo se los pague. Entonces él me dice al final fueron... 135 contenedores. Entonces yo no tengo manera de saber si realmente todos los contenedores que me están poniendo... pues de quién son, si son de ella, de él, o sea, me puede inventar cinco contenedores."* → **María Helena reconcilia 135 contenedores cruzando manualmente con sus chats de WhatsApp** (busca el número OMC en chats). *"yo no puedo estar haciendo eso diario porque al quinto me distraigo... entonces nunca termino de revisar la lista"*.
4. **Hector quiere "todo en papel impreso"** por miedo a auditoría en USA. *"si nos llega una auditoría en Estados Unidos, todo lo tiene en papel, impreso. Pero no tiene la base de datos registrada"*. Hector usa su laptop personal, no quiso nunca usar la computadora de la empresa.
5. **Empleados: archivos no digitalizados.** María Helena quisiera expedientes digitales de empleados (contratos, documentos oficiales, hoja de vida del personal, hoja de vida de los camiones).

**Ricardo (SPEAKER_00) — primera idea aterrizada:** *"Lo que se puede hacer es montar un servidor donde hay un documento donde todo el mundo pueda tener acceso y cada quien maneja su información... un tercero puede ser Google, podemos ser nosotros, puede ser la compañía que ustedes quieran"*.

→ **Primera puerta abierta para implementación de baja fricción:** Google Workspace + Drive estructurado como quick-win. Lo dice explícitamente más tarde.

## Bloque 4 — IT legacy: hosting/correo con Carlos como hostage situation (~15-20 min)

Andrea (SPEAKER_03) explica el dolor IT acumulado:

- **Dominio en GoDaddy**, pero el **hosting** está con un proveedor externo llamado **Carlos**.
- Andrea: *"cada que hablo para GoDaddy, tengo un problema con no sé qué, ah, esto, velo con tu host."*
- *"Y no lo quiere soltar, yo le dije, no te decía la cantidad de veces que le he hablado de que cóbrame... Y no quiere. No, no, no me contesta."*
- Cotizó devolución del hosting vía Zoom; Carlos no responde con número final.
- **Problema concreto actual:** *"No se pueden mandar correos a Gmail"* desde el dominio empresarial.

Ricardo identifica el patrón: *"si el correo electrónico está asociado al correo electrónico de él, entonces en el momento que tú quieras cambiar la clave, le va a llegar esa a él"* → hostage situation clásica.

María Helena sobre correos corporativos internos: *"tenemos un correo, nadie lo quiere usar. Luis usó el Google de él, Miguel está en el mercado de usar el de él"* → adopción cero del correo corporativo entre operativos.

→ **Pain #3 confirmado:** infraestructura IT controlada por un tercero no-responsivo. Migración email + hosting es un quick-win con valor alto y baja complejidad.

**Ricardo posiciona:** *"de pronto también ofrecer como entre las primeras ofertas también una posibilidad de solventar ese problema y asociarlo con algo que sea una plataforma más fácil"*.

## Bloque 5 — Change management: la historia de Querétaro (~20-25 min)

María Helena cuenta una experiencia previa de su carrera: una compañía la mandó **3 días a una hacienda en Querétaro** a entrenarse en gestión del cambio antes de implementar un sistema nuevo. Lenguaje: *"la negación, la aceptación, hasta que llegue un punto en el que tienes que darle seguimiento... como si fuera un duelo"*.

Aplicado a Trixx: en **Guadalajara** ya intentaron implementar control con escaneos foto-entrada/foto-salida; **hubo negación del personal**. *"No sabes cómo se usa el personal... es miedo, qué tal si yo no aprendo, qué tal si me echan"*.

Ricardo concuerda: *"hay que generar una idea de... que la gente sí lo tome bien y que se dé cuenta que eso es un beneficio a ellos a largo tiempo. Y no lo están reemplazando, que no lo están cambiando, que no va a perder el empleo"*.

→ **Insight de fit:** María Helena ya tiene el framework de change-management mentalizado y aplicado. No hay que vendérselo — hay que ejecutar con su soporte. Esto **reduce riesgo de implementación significativamente**.

## Bloque 6 — Cierre comercial + propuesta de pricing (~25-30 min)

**María Helena pregunta directamente:** *"¿Cómo son tus honorarios?"*

**Ricardo (transcripción literal, importante):**

> *"A ver, si te doy 100% sincero, la compañía está empezando. Ustedes son nuestro primer cliente, la verdad. Entonces, sí tenemos unas tarifas establecidas. También depende mucho de las implementaciones, entonces más que todo es por implementación."*

→ ⚠️ **Discrepancia con la directiva del PrepLlamada.** El checkpoint session 19 + el PrepLlamada §0 explícitamente decían: *"I will not propose to them any solution today, I need to gather as much information as possible"*. En la grabación Ricardo SÍ presenta modelo de pricing + dos caminos comerciales + se posiciona como "ustedes son nuestro primer cliente". **Esto no es necesariamente malo** — la conversación llegó orgánicamente a ese punto por iniciativa de María Helena, y el contexto del momento puede haberlo ameritado. Pero **es información que debe actualizarse en el checkpoint** para reflejar la realidad de la reunión vs. la directiva pre-reunión.

**Estructura de pricing presentada por Ricardo:**

| Modelo | Descripción |
|---|---|
| **Camino A — In-house** | Implementación entregada al cliente. Cliente lo opera. *"Eso requiere un poquito más de temas de logística, por así decirlo"*. |
| **Camino B — Servicio gestionado** | Fee inicial (análisis + implementación) + **fee mensual** por mantenimiento, atención al cliente, sistema corriendo en infra Nexostrat. |
| **Caso lite (sin IA)** | Google Workspace + Sheets centralizados → sin fee mensual, solo cobro por implementación. |
| **Caso con IA** | Ej: bot WhatsApp con NLP + extracción a base de datos → requiere fee mensual porque consume cómputo + APIs. |

Ricardo dice abiertamente: *"yo soy muy abierto con los costos, les decimos: vea, el discriminado es este, nuestra tarifa es esta y esto es lo que le vamos a cobrar"*.

**María Helena acepta acompañamiento total:** *"Sí, sí, hay muchas oportunidades, como viste, como empresa con mucha necesidad"*.

**Trigger event explícito de María Helena:** *"ahorita un cliente, ahorita me cae Silvia, que es la que tenía, no sé, que estaba mandando, a lo mejor, 5 contenedores, ahorita van a dar 80, entonces como que necesitamos estar preparados para lo que va a pasar a futuro"*.

→ **Demanda viene en crecimiento 16×.** Pain de escalamiento inminente. Aprovechable como urgency hook en propuesta.

**María Helena cierra con scheduling:** *"¿Y a ver cuándo agendamos? La ida, pues a ver si ahorita hablo con Héctor, a ver si el jueves"* → siguiente sesión propuesta jueves o próxima semana, posiblemente acompañando a Ricardo a Guadalajara donde tienen otra sede.

## Action items extraídos (para feed a Skill 05)

1. **Quick-win #1 — Google Workspace centralizado**: migrar Excel sprawl a Google Sheets/Drive con permisos por rol. Costo: implementación únicamente, sin fee mensual. Valor: información buscable en <3 min (KPI implícito de María Helena).
2. **Quick-win #2 — Email/hosting migration**: liberar el dominio del control de Carlos, migrar a Google Workspace empresarial. Costo: implementación + soporte de transición.
3. **Quick-win #3 — Conciliación broker Damián**: automatizar el match entre relación de contenedores facturada (Damián) y chats internos de WhatsApp (búsqueda manual de OMC actual). Bot WhatsApp con extracción a base de datos. **Esto requiere fee mensual** (consume cómputo IA).
4. **Mid-term — Plataforma in-house** que reemplace Tracking Premium gradualmente, eliminando riesgo de pérdida de datos por cancelación de SaaS.
5. **Mid-term — Expedientes digitales de personal + camiones**: hojas de vida digitalizadas, no en papel.
6. **Estructura de pricing**: por implementación, no por hora. Dos caminos A (in-house) o B (gestionado, recurring).
7. **Change management**: aprovechar que María Helena ya tiene el framework mentalizado (lección Querétaro). Co-construir plan de adopción con ella.
8. **Trigger de escalamiento**: cliente de Silvia subió de 5 a 80 contenedores — pain inmediato si no se ordena la operación.

## Datos accionables nuevos vs. session 19

- **"María Helena", no "María Helena"** es el nombre por el que se le conoce. Actualizar `state.json` + `final_report.md`.
- **Damián** = broker USA, sacaba fianzas, factura 135 contenedores a María Helena con riesgo de inflar conteo.
- **Graciela** = empleada que organiza los containers del cliente chino. Punto único de falla operativo.
- **Silvia** = capturista cuyo cliente está escalando 5→80 contenedores. Trigger de pain inmediato.
- **Carlos** = proveedor de hosting/web no-responsivo. Hostage situation IT.
- **Miguel** = posee información de relación cajas/camiones pero la mantiene en su Excel personal.
- **"Amundi"** = plataforma global mencionada como alternativa potencial a Tracking Premium (verificar: no encontré referencia clara, puede ser nombre mal capturado por WhisperX o referencia a `Monday.com` mal interpretada — Ricardo más tarde dice "Monday" en la transcripción línea 40).
- **Tracking Premium** = SaaS actual para cliente chino, pago mensual, propietario externo, datos en riesgo si se descontinúa.
- **Bodega Vernon** = bodega externa contratada, mencionada repetidamente como destino frecuente post-Mexicali.
- **México Envíos** = otro usuario con acceso al Tracking Premium (sin permisos de escritura).

## Cualidad de la transcripción WhisperX (12:05)

Excelente — 95% inteligible, nombres propios captados (María Helena, Damián, Carlos, Graciela, Silvia, Miguel, Vernon, Mexicali, Sonora, Guadalajara, Querétaro, Tracking Premium, GoDaddy). Diarización correcta (4 voces, asignación estable). Pequeñas confusiones esperables ("San Luis de Colorado" en vez de "San Luis Río Colorado"; "María Helena" vs "María Helena" — ambas formas aparecen).

Limitaciones: no captura entonación / pausas largas / risa explícita. Para Skill 05 esta versión curada es feed suficiente.
