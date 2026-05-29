# Auditoría Skill 6 (nexostrat-client-deliverables) — Run Trixx 2026-05-28

> **Sesión:** 2026-05-29 | **Auditor:** Ricardo | **Destinatario:** Juan Pablo (corrige el skill)
> **Objeto auditado:** salida cruda `skill_raw/` del run del 2026-05-28 sobre Grupo Trixx.
> **Alcance de esta sesión:** documentar lo que NO funciona (hallazgos de Ricardo, documento por documento) + lo que sí funciona para no romperlo.

**Convención de etiquetas:**
- **[SKILL]** — corrección a nivel del skill (afecta todos los clientes futuros).
- **[CLIENTE]** — ajuste de contenido específico de este run de Trixx.
- **[TEMPLATE]** — estandarización de plantilla visual.
- **[ENTREGA]** — mecanismo de entrega / infraestructura.
- **[BUG]** — fallo técnico (texto cortado, etc.).

---

## A. Hallazgos transversales (prioridad alta — afectan varios documentos)

Estos son los problemas de fondo del skill. Si JP corrige solo estos, la calidad sube en todos los entregables.

### T1 — [SKILL] Afirmaciones que no podemos sostener ("bold claims")
El skill escribe como si supiéramos mucho más de lo que realmente sabemos. Tuvimos **una sola reunión de 3 horas con los altos cargos** (no con el equipo), un análisis online y la conversación. El skill afirma cosas falsas o no verificables: "estudiamos a sus competidores directos", "nos reunimos con el equipo", "conocemos su estructura interna". **Si el cliente nos pregunta por la competencia, estamos muertos.** Trixx "no come cuento": hay que ser honestos.
- **Corrección:** calibrar todo el lenguaje a lo que realmente sabemos. Reemplazar afirmaciones por marcos como "esto entendemos de Trixx hoy", "nuestra visión", "por lo que vimos online y conversamos en la reunión inicial". El skill debe entender **con quién hablamos** (cargos altos, no el equipo) y basar las afirmaciones en eso.
- Si hace falta darle más inputs de contexto al skill para que no caiga en frases genéricas, se los damos — pero no puede inventar.

### T2 — [SKILL] Sobreexposición de "IA"
"IA" aparece en títulos y como gancho de venta. Debemos brillar por el **valor de lo que proponemos**, no porque usamos IA.
- **Corrección:** sacar "IA" de los títulos (ej. "Oportunidades de IA" → "Oportunidades a implementar" / "a desarrollar"). Vender soluciones / herramientas. La IA va en el contenido, no en el encabezado. Si una solución incluye IA, lo decimos con orgullo, pero la IA no es la razón por la que nos contratan.
- Reducir en general la mención de "IA" por área: las herramientas tienen un componente de IA (unas más que otras); si preguntan, decimos que dentro del funcionamiento usan herramientas de IA. No anunciarlo en cada sección.

### T3 — [SKILL] Pricing fuera de los límites acordados
- Floor de entrada acordado = **USD 3,000**. El skill cobra hasta 10k por iniciativa y salta a un total de 73k. Somos una consultora que empieza; sin track record no podemos sostener esos precios.
- **Saltos sin justificar:** el briefing muestra 1 quick win a 10k y salta a un resumen de 73k. ¿De dónde salen los ~63k faltantes? El total debe poder derivarse de las partes.
- **Corrección:** alinear el framework de pricing al floor de 3k y a los números acordados con JP. Cualquier total debe descomponerse en sus partes.

### T4 — [SKILL] Framing "no reemplazamos a nadie / liberar al equipo"
Mensaje central y muy importante a resaltar: **no reemplazamos a nadie, liberamos al equipo** para que dedique su tiempo a lo importante. No pretendemos decirles cómo funciona su negocio, qué hacer o a quién reemplazar. Estamos para mejorar el flujo de la información y quitar fricción (tableros claros, información clara).
- Toda la gente es valiosa — **no existe "gente valiosa" vs "no valiosa".** La idea es liberar de tareas operativas repetitivas **virtuales** (copiar y pegar, transcribir, pasar de físico a virtual, etc. — no tareas de piso) a la mayor cantidad de personas posible, sin importar cargo. Entre más tiempo tengan para pensar, desarrollar y ejecutar, mejor para la compañía.

### T5 — [SKILL] Lenguaje "robot" / asistentes
Al hablar de asistentes (ej. WhatsApp) hay que dejar claro que **no es una persona** — es un sistema/programa que hace el trabajo — pero **sin usar la palabra "robot"**.

### T6 — [SKILL] Duplicación docx + html para documentos internos
Se generan dos versiones (docx y html) con exactamente la misma información en documentos que el cliente no ve. No tiene sentido. **Crear solo una.** Ricardo prefiere HTML (se ve mejor, más organizado). Que JP elija el formato de sus propios documentos.

### T7 — [SKILL] Emojis — CRITERIO REVISADO: se mantienen (bien usados)
**Decisión de Ricardo (2026-05-29):** los emojis del `skill_raw` **gustaron** — no eran exagerados y estaban bien usados. **Se mantienen** siempre que se implementen de manera **correcta y formal**. Esto revierte el hallazgo original del README ("eliminar todos los emojis").
- **Criterio para el skill:** uso formal y mesurado, no decorativo ni excesivo. No es "cero emojis"; es "emojis con propósito".
- Pendiente menor heredado del README: las estrellas de rating `★☆` pueden migrar a formato `N/5` (a confirmar con JP; ya no es bloqueante).

### T8 — [TEMPLATE] Estandarización de plantilla (logo + footer + justificado)
- **Logo de la compañía** en la parte superior izquierda.
- **Página web (nexostrat.com)** en el pie de página, a la izquierda o centrada (donde mejor entre).
- **Texto justificado** — se ve más organizado.
- Para Claude: asegurar que los templates estén estandarizados con estos elementos.

### T9 — [SKILL/TEMPLATE] Assets de marca reales de Nexostrat
En todos los documentos (incluida la presentación) debe usarse la **identidad visual real** de Nexostrat, no aproximaciones:
- **Logo real** (el isotipo/imagen), **no la versión escrita** del nombre.
- **Tipografías reales** de marca (no fonts genéricas).
- **Paleta de colores real** de marca.
- Aplica a docx, html y pptx por igual. (Referencia: brand guide Aurora / skill `nexostrat-editorial-designer`.)

### T10 — [SKILL/CLIENTE] Nombre legal del cliente
El nombre correcto del cliente es **"Trixx Logistics Corp"**, NO "Grupo Trixx". El insumo (`Trixx_Diagnostico_Refinado` y `data_Trixx.json`) trae "Grupo Trixx (Trixx Logistics)" — debe corregirse en la capa de datos para que todos los entregables usen el nombre legal. (Confirmado por Ricardo 2026-05-29.) Aplica a este y a todos los documentos futuros de este cliente.

---

## B. Briefing Interno Ricardo — `Ricardo_BriefingInterno_Trixx_20260528.docx`

- **B1 — [CLIENTE/SKILL] Pricing roto.** Cobra 10k cuando el floor es 3k (ver T3). Salta de 1 quick win de 10k a un resumen de 73k sin explicar los ~63k faltantes.
- **B2 — [SKILL] No muestra valor.** Solo menciona 1 quick win y un total. Suelta información dispersa que es valiosa solo en conjunto con el resto. Por sí solo, este briefing no muestra nada.
- **B3 — [SKILL] Debe ser un resumen de cada etapa.** El briefing debería ser el resumen de cada una de las etapas/secciones del documento "importante" (el documento cliente), no datos sueltos.

## C. Briefing Interno Ricardo — `Ricardo_BriefingInterno_Trixx_20260528.html`

- **C1 — [SKILL] Duplicado del docx** con el mismo contenido, solo más bonito (ver T6). Eliminar la duplicación; mantener una sola versión. Ricardo prefiere HTML.
- **C2 — [CLIENTE/SKILL] Mismos problemas de contenido que el docx:** arranca con precio de 10–15k y salta a 73k; no menciona painpoints ni otra información importante que debe estar en un briefing.

### C3 — [SKILL] Propuesta de rediseño: "Briefing" → "Cheat Sheet" (HTML)
Convertir el briefing interno en un **cheat sheet** — "la hoja de trampa con la que entramos al examen". Es el documento que Ricardo tendrá a la mano **durante** la presentación para apoyarse. Debe contener:
- Los **talking points** y lo importante a saber.
- El documento del cliente en **versión puntual y directa**.
- **Respuestas a posibles preguntas** del cliente.
- **Explicación de palabras técnicas.**
- **Advertencias inline** tipo "OJO: cuidado con decir robot", "cuidado con decir X o Y" — colocadas **en el orden de la presentación**, NO todas al final.
- **Decisión de producto:** si JP quiere un brief, el Skill 6 debe sacar **dos documentos**: (1) un **brief completo** y (2) un **cheat sheet** (para leer antes y tener a la mano durante las presentaciones). El cheat sheet **debe ser HTML**. Que JP escoja el formato de sus propios documentos.

---

## D. Documento Cliente — `Trixx_Diagnostico_Documento_20260528.docx`

> Valoración general de Ricardo: **"En general me gustó el reporte"**, los cambios son pequeños (algunos de skill, otros puntuales del cliente).

### D-1. Resumen ejecutivo
- **[SKILL/CLIENTE]** Bajar el tono de los "bold claims" (ver T1): no decir "estudiamos a sus competidores directos" (ni siquiera sabemos quiénes son). Usar lenguaje como "miramos la industria", "analizamos lo que utilizan".
- **[SKILL]** No decir que nos reunimos con el equipo — hablamos solo con los cargos importantes. Las afirmaciones deben basarse en con quién realmente hablamos.

### D-2. Hallazgos principales
- **[BUG] Bullets cortados:** cada bullet empieza bien pero **se corta**, no termina la idea. Hay que identificar de quién es el fallo (¿skill? ¿Claude? ¿LibreOffice?) y corregirlo.
- **[SKILL] "Gente valiosa":** eliminar la idea de gente valiosa vs no valiosa (ver T4). Reescribir hacia "liberar a la mayor cantidad de personas de tareas operativas repetitivas virtuales".

### D-3. Punto de entrada recomendado
- **[POSITIVO]** Gusta el uso puntual de emoji aquí y que el recuadro resalte en **verde** (ver T7).
- **[SKILL] Formato:** dividir las tareas en **bullet points**, no en párrafo. Estructura sugerida:
  > **Quick wins identificados:**
  > - Asistente virtual de WhatsApp (dejar claro que **no es una persona**, es un sistema/programa que hace el trabajo).
  > - Documentos vivos con tablero maestro.
  >
  > Alto impacto; diseño, construcción y pruebas **en paralelo** al trabajo actual — no disrumpe ni interrumpe la operación.
- **[SKILL] "Problema":** no usar la palabra "problema"; cambiar por "oportunidades" o "situaciones críticas" (aunque "crítica" tampoco convence del todo).
- **[SKILL] Precios:** no poner precios/valores todavía aquí; los precios van al final.

### D-4. Metodología del diagnóstico
1. **Análisis de la empresa — [SKILL/CLIENTE]:** solo tuvimos 1 reunión de 3 horas con los altos rangos; no hemos analizado ni leído información interna. Ser abiertos: decir que hicimos un **análisis online** para entender su modelo de negocio, y que estudiamos la reunión inicial para entender su tecnología actual. No sabemos su estructura ni su posición de mercado; entendemos a grandes rasgos el modelo. Poner solo lo que realmente sabemos / encontramos / nos dijeron. (Darle más inputs al skill si hace falta, pero sin frases genéricas.)
2. **Análisis de la industria — [CLIENTE]:** ¿realmente hicimos el análisis de la industria? ¿Eso fue lo que encontramos? Escribir solo lo que de verdad tenemos e hicimos, no rellenar.
3. **Competidores — [SKILL/CLIENTE]:** ¿realmente identificamos qué hacen los competidores? ¿Cómo lo sabemos? ¿Cuáles son? Podemos hablar de la tecnología y cómo se implementa en otras áreas (ej. Amazon usa robots en bodegas), pero no sabemos qué competidores usan qué. Si dentro de la información que tengamos hay datos de competencia, **eso va en el cheat sheet**.
4. **Mensaje — [SKILL]:** cambiar a "comenzar a entender / comenzar a visualizar". Estamos **empezando** a entender las situaciones internas; aún no las sabemos, no nos reunimos con todo el equipo, ni sabemos cuántos empleados son. No afirmar conocimiento interno tras solo 3 horas. Ser honestos.

### D-5. "Tu Empresa Hoy" (sección 3)
- **[POSITIVO]** Va en lo correcto y gusta.
- **[SKILL]** No decir "esta es tu compañía" — ellos la conocen mejor que nosotros. Reencuadrar: **"Esto entendemos de Trixx hoy"** / "Nuestra visión de Trixx hoy" / "Así visualizamos Trixx hoy". Mostrar lo que **nosotros vemos** por la reunión y lo que vimos en internet.
- **[VENTA]** Si hay errores en lo que vemos, sirve para mostrarles que **pueden comunicarse mucho mejor en internet** y darse a conocer más (esto es algo que tenemos que vender).
- **[SKILL] Comparaciones:** cuidado al decir que están "por debajo / por encima". Encuadrar como nuestra visión por lo poco hablado y lo encontrado online: "están por debajo de Nuvocargo y Flexport, pueden mejorar en X o Y".

### D-6. Situación actual por área (sección 4)
- **[SKILL]** No sabemos cuáles son los grupos/áreas reales — nos hablaron de equipo, ciudades y sedes, pero no si están organizados. Cambiar el lenguaje a "lo que entendemos / lo que vimos": es **nuestra lectura** de la compañía, puede ser correcta o equivocada. (Si es incorrecta, probablemente sea por falta de comunicación — poco probable tras 3 h — o por lo que la compañía muestra externamente, que sabemos es una debilidad.)
- **[SKILL] Reducir "IA":** no es necesario mencionar que las soluciones son IA (ver T2). Venderlas como soluciones/herramientas; si preguntan, tienen componentes de IA.
- **[TEMPLATE] Justificar el texto** (ver T8).
- **[SKILL] Oportunidades por área — precisiones de contenido:**
  - *"Un punto central donde toda la información viva en tiempo real, alimentado desde WhatsApp..."* → en realidad son **dos soluciones**: el asistente de WhatsApp **y** la centralización/organización de la información.
  - *"Hoja de vida digital por camión y caja, alimentada desde WhatsApp y Samsara..."* → la alimentación es desde **WhatsApp, Excel y Samsara**; la solución es un **unificador de información** que agrega los resultados de cada fuente.
  - *"Filtrado inteligente que extrae lo accionable de cada correo..."* → **[POSITIVO]** gusta cómo está expuesta: clara, corta, sin entrar en detalles.

### D-7. Problemas identificados (sección 5)
- **[SKILL/DECISIÓN] Tono:** ¿conviene un lenguaje tan fuerte? Ricardo personalmente prefiere decir las cosas de frente, pero: ¿le va a gustar al cliente? ¿es bueno confrontarlo así con la realidad? Y más importante: ¿estamos en posición de decirles "ustedes tienen un problema" tras solo 3 horas? (Decisión a tomar con JP; ligado a renombrar "problema" → "oportunidad/situación", ver D-3.)

### D-8. "Oportunidades de IA" (sección 6)
- **[SKILL] Título:** sacar "IA" del título → "Oportunidades a implementar / a desarrollar" (ver T2).
- **[SKILL] Lenguaje:** evitar frases como *"...y hasta cuadros escritos a mano"* — no buscamos sorprender; somos una empresa profesional, esto es lo que hacemos. Cambiar a "...y cuadros o documentos escritos a mano".
- **[SKILL] Resaltar:** *"No reemplazamos a nadie: liberamos al equipo para que dedique su tiempo a lo importante."* — frase clave, debe resaltarse (ver T4).
- **[SKILL/CLIENTE] Alcance del fee mensual:** el fee incluye **mantenimiento, soporte para reparaciones y asegurar que todo funcione**, más gastos de consumo de IA. **No** incluye implementación de nuevas soluciones/herramientas ni el cambio de las ya desarrolladas. No llamarlo "fee modesto".
- **[SKILL] Aprobación por etapas:** cada etapa de la hoja de ruta se aprueba y **firma** por el cliente; una vez se avanza no se cambia la estructura. No escribirlo textual, pero el cliente debe entender que así funciona, para evitar que pida cambios/extras sobre lo ya construido y aprobado.

### D-9. Datos de contacto (cliente / template)
- **[CLIENTE]** Correo: `contacto@nexostrat.com`. Teléfono Colombia: **+57 333 286 3963**.
- **[ENTREGA]** Pendiente número de México: Ricardo tiene varios celulares; su número personal es **+52 664 670 0049**. Plan preferido: conseguir línea mexicana (o americana) para el celular principal y que ese sea el número de Nexostrat en México.

---

## E. Faltantes / nuevas capacidades a agregar

- **E1 — [SKILL] Solución faltante: presencia online / redes.** Agregar a las posibles soluciones: organizar y mejorar la presencia online, crear LinkedIn empresarial, mejorar/optimizar Instagram, herramienta que entrega **3 artículos semanales** sobre la industria + iniciativas/ideas a desarrollar. El manejo automatizado de redes sociales es un valor extra.

---

## F. Entrega / formato (infraestructura)

- **F1 — [ENTREGA] HTML cliente no es entregable como archivo.** El HTML para el cliente se ve muy bien pero debe **centrarse** para visualizarse bien; y si entregamos un archivo `.html` suelto, el cliente no podrá verlo en celular ni computador. **Ideal:** entregar un **link privado** donde el cliente escriba el nombre de la compañía y vea el reporte (HTML) y la presentación (PowerPoint).
- **F2 — [ENTREGA] Códigos QR en la presentación.** Agregar dos QR al final: (1) a la página web de Nexostrat / nuestra información; (2) a los documentos del cliente (HTML y/o presentación).

---

## G. Lo que SÍ funciona (no romper)

- El reporte cliente en general gustó; los cambios son pequeños.
- El recuadro verde + emoji puntual del "Punto de entrada recomendado".
- La sección "Tu Empresa Hoy" va en la dirección correcta (solo ajustar el encuadre de propiedad).
- La oportunidad de "filtrado inteligente de correos" está bien expuesta: clara, corta, sin sobre-detalle.
- El **HTML para el cliente** gusta mucho visualmente (resolver solo el tema de entrega/centrado).

---

## H. Presentación (PPTX + su HTML) — `Trixx_Diagnostico_Presentacion_20260528.*`

> **Estado:** JP está corrigiendo las presentaciones actualmente (2026-05-29).

- **H1 — [SKILL] Mismos comentarios de contenido** que el documento cliente (la presentación y su HTML son copias del mismo contenido). Aplican todos los hallazgos de D y las transversales A.
- **H2 — [TEMPLATE/T9] Identidad de marca real:** usar en todo el contenido el **logo real** de Nexostrat (no la versión escrita) y las **fonts y colores reales** de marca.
- **H3 — [ENTREGA] Visualización/centrado:** en la pantalla de Ricardo el texto **no está centrado**. Corregir para que la visualización sea correcta (ver también F1).
- **H4 — [ENTREGA/F2] QR:** agregar al final los dos códigos QR (web Nexostrat + documentos del cliente).

---

## Pendiente de revisar (documentos aún sin comentar)

- [ ] HTML del documento cliente — `Trixx_Diagnostico_DocumentoCliente_20260528.html` (probablemente mismos comentarios que el docx + T9 marca + F1 visualización)
- [ ] Data — `data_Trixx_skill.json`
