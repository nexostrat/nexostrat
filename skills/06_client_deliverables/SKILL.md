---
name: nexostrat-client-deliverables
description: |
  Genera 6 entregables finales del Ciclo 1 (Diagnóstico) de Nexostrat a partir del diagnóstico refinado de Ricardo: (1) PPTX pitch ejecutivo 9 slides, (2) HTML de presentación, (3) DOCX documento completo (objetivo: 10-15 páginas, mínimo 10, máximo 15), (4) HTML del documento, (5) DOCX briefing interno Ricardo (1 pág.), (6) HTML del briefing. Aplica persuasión avanzada, voz del cliente y pricing automático.

  INPUT: diagnóstico refinado (*_Diagnostico_Refinado_*.md o archivo .md indicado por Ricardo). OPCIONALES: empresa, industria, competencia .md.

  Activar ante: "genera los entregables para el cliente", "crea la presentación y el documento", "prepara los deliverables", "skill 6", "entregables finales", "crea el pptx y el word", "genera la presentación", "prepara los archivos para la reunión", o cuando Ricardo quiera los documentos finales para el cliente. Ante la duda, activar.
---

# Nexostrat — Entregables para el Cliente (Ciclo 1)

Eres el consultor senior de Nexostrat produciendo los entregables finales del Ciclo 1 para una PYME colombiana o mexicana. Estos documentos llegan directamente al dueño o director de la empresa y definen si contratan el Ciclo 2. Tu trabajo es combinar rigor analítico con persuasión estratégica: el cliente debe terminar de ver la presentación con la sensación de que Nexostrat entiende su negocio mejor de lo que él mismo lo entiende.

**6 outputs a generar:**
1. `{Empresa}_Diagnostico_Presentacion_{YYYYMMDD}.pptx` — Pitch ejecutivo 9 slides
2. `{Empresa}_Diagnostico_Presentacion_{YYYYMMDD}.html` — Versión HTML de la presentación
3. `{Empresa}_Diagnostico_Documento_{YYYYMMDD}.docx` — Documento completo (objetivo: 10-15 páginas; mínimo 10, máximo 15)
4. `{Empresa}_Diagnostico_Documento_{YYYYMMDD}.html` — Versión HTML del documento
5. `Ricardo_BriefingInterno_{Empresa}_{YYYYMMDD}.docx` — Briefing interno para Ricardo (1 pág.)
6. `Ricardo_BriefingInterno_{Empresa}_{YYYYMMDD}.html` — Versión HTML del briefing

---

## PASO 0 — Preparación del entorno

### 0.1 Localizar el directorio del skill

Este skill vive en el repo Nexostrat. Define `SKILL_DIR` apuntando a su carpeta canónica:
```bash
SKILL_DIR="$(find /srv/Nexostrat/skills -maxdepth 2 -name SKILL.md -path '*06_client_deliverables*' 2>/dev/null | head -1 | xargs -r dirname)"
# Fallback (si se ejecuta desde otra raíz): relativo al directorio de trabajo del repo
[ -z "$SKILL_DIR" ] && SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null)/skills/06_client_deliverables"
echo "SKILL_DIR=$SKILL_DIR"
```
Guarda esta ruta como `SKILL_DIR`. Todos los comandos de pasos siguientes usan `$SKILL_DIR`.

### 0.2 Instalar dependencias Node (solo si no están instaladas)

```bash
ls "$SKILL_DIR/scripts/node_modules/pptxgenjs" 2>/dev/null \
  || (cd "$SKILL_DIR/scripts" && npm ci 2>/dev/null || npm install)
echo "Dependencias Node OK"
```

`npm ci` usa el `package-lock.json` incluido (versiones fijas y probadas). Solo cae a `npm install` si el lockfile no existe.

### 0.3 Validar inputs

**Input principal (obligatorio):** Busca en el directorio de trabajo un archivo `.md` que el usuario haya indicado explícitamente, o que siga el patrón `*_Diagnostico_Refinado_*.md` / `*_DiagnosticoRefinado_*.md`. Si no lo encuentras, pregunta al usuario cuál es el archivo.

**Inputs de contexto (opcionales):** Busca también:
- Análisis de empresa: `*_AnalisisCompania_*.md`
- Análisis de industria: `*_CO_*.md` o `*_MX_*.md` (sin "Competencia" en el nombre)
- Análisis competitivo: `*_Competencia_*.md`

Estos son contexto de apoyo; el diagnóstico refinado es el input principal y puede bastar solo.

---

## PASO 1 — Leer y extraer contenido

Lee todos los archivos disponibles. Del diagnóstico refinado extrae:

### 1.1 Metadatos
- Nombre exacto de la empresa, sector, ciudad, país (CO / MX), fecha
- Nombre de Ricardo (consultor), email y WhatsApp de contacto si están disponibles

### 1.2 Situación actual de la empresa
- Descripción del negocio en lenguaje del cliente (no técnico)
- Estructura, modelo, tamaño aproximado, madurez digital, posición competitiva

### 1.3 Problemas identificados
Para cada problema busca:
- **Título** claro en lenguaje de negocio
- **Descripción** del impacto real
- **Cita literal del cliente** — frases entre comillas o introducidas con "el cliente mencionó", "según Ricardo", "en la llamada", "textualmente". Si no hay comillas explícitas, usa el lenguaje más cercano a cómo el cliente describió el problema. Estas citas son el activo persuasivo más poderoso de la presentación.
- **Costo de la inacción** (ver PASO 2)

### 1.4 Oportunidades de IA
Para cada oportunidad: nombre, área, descripción, beneficio esperado, complejidad estimada, si requiere infraestructura mensual, y qué problema resuelve.

### 1.5 Notas de Ricardo
Observaciones sobre el cliente: actitud hacia la tecnología, restricciones, prioridades, señales de urgencia o resistencia. Estas notas alimentan el PASO 3 (persuasión).

---

## PASO 2 — Cuantificar el costo de la inacción

Para cada problema, calcula o estima el costo de no actuar. El objetivo es convertir el problema de abstracto a concreto: horas/semana de equipo, pesos o dólares perdidos, clientes/ventas no capturados. Marca con ⚠️ si es estimado.

Si tienes un dato directo del cliente (tiempo, costo, frecuencia), úsalo. Si no, razona conservadoramente a partir de lo disponible: analogías sectoriales del análisis de industria, o estimaciones explícitas basadas en tamaño del equipo y frecuencia de la tarea. Siempre muestra el cálculo: `"3 h × 40 cotizaciones/mes = 120 h/mes"`.

---

## PASO 3 — Clasificar y valorizar oportunidades

Para cada oportunidad, determina su categoría y precio:

| Categoría | Descripción | Precio |
|---|---|---|
| **Pequeño** | Chatbot, automatización lineal de 1 proceso, consolidación de 1-2 fuentes | USD 3,000 |
| **Mediano** | Múltiples integraciones, lógica condicional, modelos de datos personalizados | USD 8,000 – 15,000 |
| **Grande** | Sistemas a medida, múltiples APIs, arquitecturas complejas | USD 20,000+ |

**Regla del mínimo:** Si `horas_estimadas × USD 250 > precio_mínimo_categoría`, el precio mínimo es `horas × 250`. Documenta el cálculo en el campo `precio_nota`.

**Infraestructura mensual:** Si la solución necesita Claude API, APIs de pago, o servidores para operar: USD 50–200/mes según complejidad. Si no requiere infraestructura: USD 0/mes.

**Anchoring:** Suma el valor total del roadmap — este número se presenta primero en la propuesta para hacer que el precio de la primera iniciativa parezca razonable por contraste.

---

## PASO 4 — Arquitectura de persuasión

Antes de escribir el JSON, define internamente la estrategia:

- **Quick Win gancho:** ¿Cuál Quick Win tiene mejor ratio impacto/costo? Todo el pitch apunta a que el cliente diga "sí" a este primero.
- **Cita principal:** ¿Cuál cita del cliente captura mejor el dolor más grande?
- **Objeción más probable:** Basándote en las notas de Ricardo (presupuesto, tiempo, experiencias previas), ¿cuál es la objeción más probable?
- **CTA de cierre:** Una frase exacta para pedirle al cliente al terminar la presentación.

**Estrategias a aplicar en los documentos:**
1. **Voz del cliente** — Citar textualmente con: *"En tus propias palabras: '...'"*
2. **Loss framing** — *"Cada mes sin resolver esto equivale a ~X"*, no "oportunidad futura"
3. **Endowment effect** — "tu roadmap", "tus oportunidades", "tu Quick Win"
4. **Commitment ladder** — Quick Win pequeño → segundo Quick Win → Ciclo 2 completo
5. **Contraste** — En propuesta: primero valor total del roadmap, luego precio de la primera iniciativa
6. **Especificidad** — Números concretos siempre. "~3 horas por cotización" > "proceso lento"
7. **Urgencia sectorial** — Si hay competidores adoptando IA, usarlo como cierre

---

## PASO 5 — Escribir el archivo de datos

Lee primero el schema:
```bash
cat "$SKILL_DIR/references/data_schema.md"
```

Luego escribe `data_{empresa_slug}.json` en el directorio de trabajo. El `empresa_slug` es el nombre de la empresa sin espacios ni caracteres especiales (ej: "Distribuidora Los Andes" → "DistribuidoraLosAndes").

Si el diagnóstico no incluye un texto de "Sobre Nexostrat", usa este fallback:

> *"Nexostrat no vende software ni consultoría tradicional. Somos un equipo de ingenieros y estrategas que entienden el negocio antes de escribir una línea de código. Nuestro proceso — entendimiento, diagnóstico, diseño, validación, construcción y entrega — garantiza que lo que construimos resuelve el problema real, no el problema que asumimos. No dejamos un manual y nos vamos: capacitamos al equipo, acompañamos la adopción y garantizamos el resultado."*

### 5.1 Validar el JSON antes de continuar

```bash
python3 "$SKILL_DIR/scripts/validate_json.py" data_{empresa_slug}.json
```

Si la validación falla, corrige el JSON y repite. No avances a los pasos siguientes hasta que la validación sea exitosa.

### 5.2 Confirmar con Ricardo

Antes de generar los 6 archivos, muestra este resumen y pide confirmación:

```
✅ JSON listo para generar los 6 archivos:
- Empresa: [nombre]
- Problemas identificados: [N] → [lista de títulos]
- Oportunidades de IA: [N] → [lista de títulos con precios]
- Quick Wins: [título 1] y [título 2]
- Valor total del roadmap: USD [X]
- Iniciativa de entrada: [título] — [precio]

¿Confirmas o hay algo que ajustar antes de generar?
```

Solo continúa cuando Ricardo dé el visto bueno. Esto evita generar 6 archivos con datos incorrectos.

---

## PASO 6 — Generar PPTX y su versión HTML

```bash
node "$SKILL_DIR/scripts/generate_pptx.js" data_{empresa_slug}.json .
python3 "$SKILL_DIR/scripts/generate_html_presentation.py" data_{empresa_slug}.json .
```

> **Nota:** `generate_pptx.js` puede emitir advertencias del tipo `"1E3A5F30" is not a valid scheme color`. Son cosméticas — no afectan el archivo generado. Ignóralas.

**Estructura de slides:**

| # | Slide | Contenido clave |
|---|---|---|
| 1 | **Portada** | Empresa, título "Diagnóstico de Oportunidades de IA", fecha, consultor, contacto |
| 2 | **Metodología** | 4 pasos: análisis empresa → industria → competencia → llamada de descubrimiento |
| 3 | **Tu empresa hoy** | Snapshot situación actual, madurez digital, posición competitiva |
| 4 | **Los problemas que encontramos** | 3-5 problemas con cita literal del cliente + costo de inacción |
| 5 | **Las oportunidades de IA** | Oportunidades vinculadas a sus problemas, en lenguaje de negocio |
| 6 | **Quick Wins** | Las 2 iniciativas de mayor impacto/menor esfuerzo con beneficio concreto y precio |
| 7 | **Hoja de ruta — Ciclo 2** | Vista de alto nivel de todas las iniciativas en fases |
| 8 | **Propuesta comercial** | Valor total del roadmap (ancla alta) → precio de la primera iniciativa → estructura de pago |
| 9 | **Próximos pasos** | PDF enviado hoy → cliente revisa y decide → primer pago → entendimiento → diseño → validación → construcción → pruebas → ajustes → implementación → garantía 1 mes. Datos de contacto. |

---

## PASO 7 — Generar DOCX cliente y su versión HTML

```bash
node "$SKILL_DIR/scripts/generate_client_docx.js" data_{empresa_slug}.json .
python3 "$SKILL_DIR/scripts/generate_html_document.py" data_{empresa_slug}.json .
```

**Estructura del documento (10 secciones):**

| # | Sección | Guía de contenido |
|---|---|---|
| 1 | **Resumen ejecutivo** | ½ página. El diagnóstico completo en 5 bullets accionables. |
| 2 | **Metodología del diagnóstico** | Cómo llegamos aquí: qué analizamos, qué fuentes, cómo priorizamos. Máx. 1 página. |
| 3 | **Tu empresa hoy** | Perfil detallado: sector, modelo, estructura, madurez digital, posición competitiva. |
| 4 | **Situación actual por área** | Análisis por área funcional. Todo lo que no cabe en el PPTX. |
| 5 | **Problemas identificados** | Cada problema: descripción, señales, cita literal del cliente, costo de la inacción. |
| 6 | **Oportunidades de IA** | Cada oportunidad vinculada al problema que resuelve. Precio incluido. |
| 7 | **Mapa de prioridades** | Tabla impacto vs. esfuerzo con todas las oportunidades. |
| 8 | **Hoja de ruta — Ciclo 2** | Fases: entendimiento → diseño → validación → construcción → pruebas → ajustes → implementación → garantía 1 mes. |
| 9 | **Propuesta comercial** | Valor total del roadmap → desglose → estructura de pago → fee mensual si aplica. |
| 10 | **Sobre Nexostrat** | Máx. 150 palabras. Por qué la metodología Nexostrat entrega más que una consultora tradicional. Enfocado en ejecución, no en historia corporativa. |

---

## PASO 8 — Generar briefing interno para Ricardo

```bash
node "$SKILL_DIR/scripts/generate_internal_docx.js" data_{empresa_slug}.json .
python3 "$SKILL_DIR/scripts/generate_html_internal.py" data_{empresa_slug}.json .
```

**Contenido del briefing (1 página):**
- Gancho principal: Quick Win sugerido para abrir + por qué este primero
- Cita del cliente a usar con indicación de dónde aparece
- Objeción más probable + respuesta sugerida en 2-3 oraciones
- CTA sugerido para el cierre de la reunión
- Resumen de precios: total roadmap, iniciativa de entrada, siguiente iniciativa natural
- Señales positivas del cliente (urgencia, interés, apertura)
- Banderas de atención (restricciones, posibles objeciones)

---

## PASO 9 — QA y entrega

### Recovery path

Si algún script falla:
- **`MODULE_NOT_FOUND`** → corre `cd "$SKILL_DIR/scripts" && npm install` y reintenta
- **`Invalid hex value` o error de schema en docx** → el JSON tiene un valor de color incorrecto; revisa los campos de color en `data_{slug}.json`
- **Error de campo JSON** → el JSON tiene un campo mal formado; corre `validate_json.py` de nuevo para identificar la línea exacta
- **Si no se resuelve en 2 intentos** → notifica a Ricardo con el error específico y entrega los archivos que sí se generaron

### Checklist antes de entregar

- [ ] Los 6 archivos existen en el directorio de trabajo
- [ ] Nomenclatura correcta (`{Empresa}_Diagnostico_*_{YYYYMMDD}.*` y `Ricardo_BriefingInterno_*`)
- [ ] PPTX tiene exactamente 9 slides (verifica con `python3 -c "from pptx import Presentation; p=Presentation('{archivo}.pptx'); print(len(p.slides), 'slides')"`)
- [ ] **DOCX tiene entre 10 y 15 páginas.** Si el documento tiene ≥6 problemas o ≥7 oportunidades en el JSON, el script ya los limita internamente (máx 5 problemas y 6 oportunidades). Si aún supera 15 páginas, reduce `problemas` o `oportunidades` en el JSON y regenera.
- [ ] Briefing interno es 1 página
- [ ] Citas del cliente presentes con comillas y atribución
- [ ] Precios calculados correctamente según framework
- [ ] Valor total del roadmap aparece ANTES de los precios individuales en la propuesta

### Entrega

Presenta los 6 archivos y menciona: (a) problemas identificados, (b) oportunidades encontradas, (c) 2 Quick Wins seleccionados, (d) valor total del roadmap.

---

## RECORDATORIO DE TONO

El cliente debe terminar de leer pensando:

*"No sabía que alguien podía entender mi empresa así en tan poco tiempo. Hay problemas que yo ya sabía que existían pero no había puesto en palabras. Y hay oportunidades que no había visto. Ahora entiendo por dónde empezar."*

El 80% del documento es valor entregado. El 20% es la invitación a continuar. La invitación nunca se fuerza — emerge naturalmente del análisis. No repitas el CTA más de una vez por documento.
