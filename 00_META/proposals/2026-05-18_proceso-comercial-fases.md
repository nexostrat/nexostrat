# Proceso Comercial Nexostrat — Cuatro Fases

> Estado: 90 % acordado en reunión Ricardo–JP del 2026-05-18. Pendiente confirmación final.
> Para: JP · De: Ricardo

## Resumen

Cuatro fases secuenciales. **Fase 0 gratuita** (gancho de entrada). **Fase 1 paga — $900.000 COP** (primera venta; incluye **dos reuniones de 1 hora** cara al cliente). **Fase 2** implementación. **Fase 3** retainer. Entre cada skill, **revisión humana obligatoria**.

---

## Fase 0 — Pre-engagement gratuito

> *Nota sobre el alcance:* la estructura de Fase 0 (reunión de 30 minutos + documento de 2 páginas, todo gratuito) aplica para los **pilotos iniciales**. Una vez validado el modelo con varios casos reales, evaluamos si Fase 0 se mantiene gratuita, se cobra una parte, o cambia de forma.

1. **Humano** diligencia un formato pre-armado con: nombre de la empresa, redes sociales, sitio web, contacto interno conocido + cargo, sector.
2. **Claude** corre **Skill 01 Company Analyst** sobre el formato. Produce el reporte de la compañía.
3. **Humano** lee el reporte, corrige, agrega información si la tiene.
4. **Claude** corre **Skill 02 Industry Analyst** con el reporte corregido de Skill 01. Produce el reporte sectorial.
5. **Humano** lee, corrige, agrega información.
6. **Claude** corre **Skill 03 Competitor Analyst** con los reportes corregidos de 01 + 02. Produce el reporte de competidores.
7. **Humano** lee, corrige, agrega información.
8. **Claude** corre **Skill 04 Briefing + Guion 30 min** con los tres reportes corregidos. Produce: brief de compañía / industria / competidores; terminología clave del sector; pain points comunes; oportunidades conocidas; implementaciones de IA conocidas en la industria y por competidores; **guion para una reunión inicial de 30 minutos** (llegar con curiosidad, descubrir procesos y dolores del cliente).
9. **Humano** lee, ajusta, lleva la **reunión de 30 minutos** con el cliente. Se graba completa.
10. **Claude** corre **Skill 05 Resumen Pre-engagement** con todos los reportes + la transcripción de la reunión. Produce un documento de **máximo 2 páginas**: resumen de lo recolectado + respuestas organizadas de la reunión + **oportunidades iniciales de alto nivel** (sin solución ni implementación) + gancho a la reunión pagada.
11. **Humano** lee, ajusta, envía por correo al cliente con el enlace de Calendly.
12. **Sistema:** a la **semana 1 sin respuesta**, envía correo de seguimiento automático.
13. **Sistema:** a la **semana 2 sin respuesta**, alerta a Ricardo (o JP) para contactar por llamada o WhatsApp.
14. **Sistema:** Calendly recibe la reserva. El cliente diligencia un campo libre: qué quiere discutir, otras oportunidades a explorar, dudas sobre la propuesta inicial.

---

## Fase 1 — Diagnóstico pagado · $900.000 COP

**El precio incluye dos reuniones de 1 hora cara al cliente:**

- **Reunión 1 — Discovery profundo** (después de Skill 06). Nexostrat lidera con cuestionario preparado para profundizar en procesos, dolores y oportunidades del cliente.
- **Reunión 2 — Socialización** (después de Skill 08). Presentación del PDF final al cliente, explicación por solución, preguntas y resolución de dudas.

### Pasos

1. **Sistema:** la reserva en Calendly + confirmación de pago disparan Fase 1.
2. **Claude** corre **Skill 06 Análisis Profundo** con toda la información de Fase 0 + el campo libre del Calendly. Profundiza en procesos, busca más oportunidades, mapea vías de implementación de IA (productividad, reducción de costos, ahorro de tiempo). Produce: análisis ampliado + cuestionario y guía para la **Reunión 1**.
3. **Humano** lee, ajusta, lleva la **Reunión 1 (1 hora)** con el cliente. Se graba completa.
4. **Claude** corre **Skill 07 Soluciones Implementables** con toda la información acumulada + transcripción de Reunión 1. Produce listado de soluciones reales que Nexostrat puede ejecutar, con plan concreto por solución.
5. **Humano** lee, ajusta, agrega información.
6. **Claude** corre **Skill 07.5 Scoring de Soluciones** *(a confirmar con JP)*. Por cada solución: costo de construcción + implementación + hosting / suscripciones; capacidad real de Nexostrat (sí / no); score en complejidad, tiempo, recursos, costo para Nexostrat, costo para el cliente.
7. **Humano** lee, ajusta, agrega información.
8. **Claude** corre **Skill 08 PDF Comercial Cliente** consolidando todo. Produce el PDF cara al cliente: listado de soluciones + oportunidades; gráfico de beneficio vs complejidad; costo y tiempo por solución (cuánto cobramos); lenguaje no técnico, ELI5 cuando aplique; organización clara.
9. **Humano** lee el PDF, ajusta, le pide al cliente agendar la **Reunión 2 (1 hora — incluida en el precio)** para socializar el documento.

---

## Fase 2 — Implementación

Ejecutamos las soluciones que el cliente seleccione del PDF de Fase 1. **Aún sin diseñar en detalle** — esperamos al primer cliente real para no diseñar sobre suposiciones.

---

## Fase 3 — Retainer

Cliente paga suscripción mensual por mantenimiento, soporte y mejoras continuas sobre lo implementado en Fase 2. **Aún sin diseñar en detalle** — esperamos al primer cliente que llegue a esta etapa.

---

## Cambios respecto al estado actual

1. **JP construye los skills nuevos y define el contenido / prompts de los skills.** Ricardo arma el wrapping técnico (folder, test harness, integración). El conocimiento de qué tiene que decir cada skill, qué outputs producir y con qué tono — eso lo aporta JP.
2. **Skill 04 = `06_discovery_meeting` rebrandeado, con ajustes.** Para empezar renombramos `06_discovery_meeting` → `04_briefing_30min` (placeholder estructural). El skill actual produce un guion de 60 minutos pensado para una reunión post-pago; **JP ajusta el contenido** para que produzca un guion de 30 minutos pre-pago, con gancho a la reunión pagada en lugar de a una propuesta directa. El guion de 60 minutos se reconstruye como parte de Skill 06 cuando JP lo entregue.
3. **Skills 01, 02, 03 ya están en producción.** Se reusan tal cual. Pendiente: agregar marcado de confianza ✓ / ~ / ? a las cifras de Skill 01 (mejora del piloto del 2026-05-17).
4. **Skills 05, 06, 07, 07.5, 08 son nuevos.** JP los entrega cuando tenga el contenido listo.
5. **Revisión humana entre cada skill** queda como regla del sistema (en el piloto del 2026-05-17 lo hicimos manualmente; ahora es obligatorio).
6. **Automatización nueva por construir** (cuando los skills estén listos): formato pre-armado de entrada (Fase 0 paso 1), integración Calendly + webhook a Fase 1, correo automático día 7, alerta día 14, integración de grabación de reuniones.

---

## Decisiones pendientes (confirmar con JP)

1. ¿Skill 07.5 es un skill aparte o se fusiona con Skill 07?
2. Rango de descuento permitido sobre los $900.000 COP.
3. *Posición de Ricardo:* usar FOSS (Cal.com self-hosted u otra) siempre que el UX para el cliente sea tan simple como Calendly. La elección específica se confirma en el Plan 02 (pila FOSS de Stage 1). ¿JP está de acuerdo?
4. Plantilla y tono del correo automático del día 7 — debe leer como Ricardo, no como bot.
5. *Resuelto:* **Ricardo atiende todas las llamadas y comunicaciones con clientes** (incluyendo la alerta del día 14).
6. ¿Confirmamos dejar Fase 2 y Fase 3 como sketches hasta tener un cliente real en cada una?
7. Confirmar precio: **$900.000 COP** por Fase 1 (incluye las **2 reuniones de 1 hora**).

---

*Una vez JP confirme, pasamos al brainstorm técnico de arquitectura.*
