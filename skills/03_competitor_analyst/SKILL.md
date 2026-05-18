---
name: competitor-analyst
description: |
  Análisis competitivo — Mejía, IA & CIA. Lee el reporte de company-analyst de la empresa prospecto y genera un análisis completo de la competencia (8 secciones): mapa competitivo (3-5 directos + 2-3 indirectos), fichas por competidor con bullet points de IA adoptada, tabla comparativa empresa vs. competidores, análisis de brechas, posicionamiento relativo, oportunidades de diferenciación con IA, señales de punto ciego, y síntesis lista para la llamada. Output: .md + .docx.

  Activar SIEMPRE ante: "analiza la competencia de [empresa]", "¿quiénes son los competidores de [empresa]?", "competitive analysis", "análisis competitivo", "¿cómo está [empresa] vs. sus competidores?", "dame las fichas de los competidores de [empresa]", "quiero saber cómo se compara [empresa] con su competencia", o cualquier variante que implique mapear y analizar competidores antes de una reunión comercial. Activar también cuando el usuario comparte un .md de company-analyst y pide el siguiente paso. Ante la duda, activar.
---

# Competitor Analyst — Análisis Competitivo

**Uso:** Interno — Mejía, IA & CIA  
**Input:** Reporte .md de company-analyst de la empresa prospecto (obligatorio)  
**Output:** `[Empresa]_Competencia_CO_YYYYMMDD.md` + `.docx`  
**Propósito:** Mapear el paisaje competitivo del prospecto para enriquecer la llamada exploratoria y la propuesta de IA

---

## REGLA ANTI-ALUCINACIÓN

Si una fuente no arroja resultados o no está disponible:
→ Escribe: **"No se encontró información en [fuente]."**

Nunca inventes tamaños de mercado, revenue de competidores, ni herramientas de IA sin fuente verificable.  
Si no encuentras adopción de IA específica de un competidor, escríbelo: "No se encontró evidencia pública de adopción de IA en [competidor]."

---

## INPUTS REQUERIDOS

**Paso 0 — Leer el reporte de company-analyst**

Antes de hacer cualquier búsqueda, lee el .md de company-analyst del prospecto. Extrae:
- Nombre de la empresa, NIT, ciudad, sector CIIU
- Tamaño (empleados, ingresos si disponibles)
- Productos y servicios principales
- Clientes objetivo y geografía de operación
- Madurez digital actual (calificación 1-5)
- Principales fortalezas y debilidades identificadas

Esta información define los criterios para identificar competidores directos e indirectos, y ancla el lado izquierdo de la Tabla Comparativa (Sección 3).

Si el usuario no proporcionó el .md de company-analyst, busca el archivo más reciente con el nombre de la empresa en el directorio de trabajo antes de pedir que lo suban.

---

## WORKFLOW

### SETUP — Destino de outputs

**Convención canónica (per spec §7).** Cuando se ejecuta dentro del pipeline de un cliente, los outputs van a:

```
pipeline/clients/<slug>/03_competitor_analysis/runs/<YYYY-MM-DD_HHMM>_mode-a/
├── final_report.md      ← reporte principal (este skill)
├── final_report.docx    ← versión Word (generada por scripts/generate_docx.py)
└── notes.md             ← opcional: juicio cualitativo del operador (útil para iteración de prompts)
```

Para este skill, `<stage>` = `03_competitor_analysis` (corresponde a `pipeline/clients/_template/03_competitor_analysis/`).

**Input requerido:** el reporte .md de company-analyst del mismo cliente. Típicamente ubicado en `pipeline/clients/<slug>/01_company_analysis/runs/<RUN_ANTERIOR>/final_report.md`.

**Invocación standalone (fuera del pipeline):** guardar en el directorio de trabajo actual usando la convención de nombre `[EmpresaCamelCase]_Competencia_CO_YYYYMMDD.md/.docx` (ver Paso 5 abajo).

**Captura de versión:** el SHA del commit Git al momento del run identifica la versión exacta del prompt usado (per ADR-022).

---

### Paso 1 — Identificar el mapa competitivo

Con base en el perfil extraído del company-analyst:

**Competidores directos (3–5):** Mismos productos/servicios + mismo segmento de cliente + misma geografía.  
**Competidores indirectos (2–3):** Producto diferente pero que compite por el mismo presupuesto del cliente o resuelve la misma necesidad de otra forma.

Criterio de selección: prioriza empresas con presencia verificable en Colombia. Para competidores directos, incluye tanto empresas colombianas como internacionales con operación activa en CO. Para indirectos, documenta explícitamente por qué compiten (ej: "compiten por el mismo presupuesto de TI del cliente").

Búsquedas recomendadas:
```
"[empresa] competidores Colombia [sector]"
"empresas [sector] Colombia similares a [empresa]"
"[producto/servicio] proveedores Colombia"
"[empresa] vs [competidor candidato]"
```

### Paso 2 — Investigar cada competidor

Para cada competidor, busca en este orden:
1. Sitio web corporativo — propuesta de valor, productos, precios si disponibles
2. LinkedIn — tamaño de empresa, crecimiento, perfil del equipo
3. Google/App stores — reseñas, calificación, quejas frecuentes
4. Press — portafolio.co, larepublica.co, elcolombiano.com + prensa especializada del sector
5. Supersociedades — correr `extract_financials.py` para competidores colombianos

**Para cada competidor, buscar señales de adopción de IA:**
```
"[competidor] inteligencia artificial"
"[competidor] automatización tecnología"
"[competidor] machine learning OR AI OR chatbot OR RPA"
"[competidor] transformación digital"
```

Consulta `references/competitor_research_guide.md` para señales específicas de IA por sector.

### Paso 3 — Buscar datos financieros (competidores colombianos)

Para cada competidor colombiano, ejecuta (desde la raíz del repo `/srv/Nexostrat/`):
```bash
pip install openpyxl pandas --break-system-packages -q
python3 skills/03_competitor_analyst/scripts/extract_financials.py "[nombre o NIT]"
```

El script se auto-localiza y lee los archivos de Supersociedades incluidos en `skills/03_competitor_analyst/assets/` automáticamente (`supersociedades_balance_general.xlsx` + `supersociedades_estado_resultados.xlsx`). No requiere argumentos adicionales.

### Paso 4 — Escribir el reporte

Usa el template de abajo. El reporte completo debe tener al menos 3,000 palabras.

### Paso 5 — Generar el .docx

```bash
pip install python-docx --break-system-packages -q
python3 skills/03_competitor_analyst/scripts/generate_docx.py <ruta_md> <ruta_docx>
```

Convenciones de nombre (ver § PASO 0 — Setup arriba):
- **Dentro del pipeline:** `final_report.md` + `final_report.docx` (canónico per spec §7)
- **Standalone:** `[EmpresaCamelCase]_Competencia_CO_YYYYMMDD.md/.docx`

---

## TEMPLATE DEL REPORTE

```markdown
# Análisis Competitivo: [NOMBRE EMPRESA CLIENTE]
**Colombia · [Mes Año]**  
**Preparado por:** Mejía, IA & CIA — Uso Interno  
**Basado en:** company-analyst [fecha del reporte fuente]

---

## 1. MAPA COMPETITIVO

### Criterios de clasificación
[Explica brevemente qué hace a un competidor "directo" vs. "indirecto" para esta empresa específica]

### Competidores directos
| Empresa | País de origen | Presencia CO | Tamaño estimado | Por qué es competidor directo |
|---------|---------------|--------------|-----------------|-------------------------------|
[3-5 filas con datos reales]

### Competidores indirectos
| Empresa | Tipo de competencia | Por qué compite indirectamente |
|---------|--------------------|---------------------------------|
[2-3 filas con criterio claro]

---

## 2. FICHAS POR COMPETIDOR

[Repetir este bloque para cada competidor directo. Para indirectos, una versión abreviada es suficiente.]

### [Nombre del Competidor]

**Propuesta de valor central:**
[1-2 frases que sintetizan qué venden y a quién]

**Presencia digital:**
- Web: [URL + calificación de calidad: básica / media / avanzada]
- LinkedIn: [# seguidores, actividad reciente]
- App / autoservicio: [sí/no + descripción]
- Reseñas: [calificación + fuente + # de reseñas + quejas más comunes]

**Tamaño:**
- Empleados: [dato + fuente]
- Ingresos: [dato en COP miles si está en Supersociedades, o estimado por prensa]
- Presencia geográfica: [ciudades / cobertura]

**Diferenciadores clave:**
- [Diferenciador 1]
- [Diferenciador 2]
- [Diferenciador 3]

**Adopción de IA y tecnología:**
- [Herramienta / plataforma de IA o automatización adoptada, con fuente]
- [Señal de automatización de procesos]
- [Nivel estimado de madurez digital: 1-5]
- *Si no se encontró evidencia: "No se encontró evidencia pública de adopción de IA en [competidor]."*

**Vulnerabilidades observadas:**
[Quejas en reseñas, gaps en propuesta de valor, áreas donde claramente no están invirtiendo]

---

## 3. TABLA COMPARATIVA

| Criterio | [Empresa Cliente] | [Competidor 1] | [Competidor 2] | [Competidor 3] |
|----------|-------------------|----------------|----------------|----------------|
| Propuesta de valor | | | | |
| Presencia web | | | | |
| App / autoservicio | | | | |
| Reseñas (calificación) | | | | |
| Precio relativo | | | | |
| Madurez digital (1-5) | | | | |
| IA adoptada | | | | |
| Fortaleza principal | | | | |
| Debilidad principal | | | | |

*Leyenda: ✅ = fuerte / ⚠️ = medio / ❌ = débil o ausente*

---

## 4. ANÁLISIS DE BRECHAS

### Qué hacen mejor los competidores (que la empresa cliente no hace)
[Lista con evidencia específica: qué competidor, en qué dimensión, con qué evidencia]

### Qué NO está haciendo nadie (oportunidades de mercado abiertas)
[Dimensiones donde toda la competencia tiene gaps — precio, servicio, autoservicio, IA, especialización]

### Brechas de IA específicas
[Qué herramientas de IA está adoptando la competencia que la empresa cliente todavía no tiene — y viceversa]

---

## 5. POSICIONAMIENTO RELATIVO

### Mapa de posicionamiento
[Descripción narrativa de dónde está la empresa cliente en el mapa competitivo, usando 2 ejes relevantes para el sector — ej: precio vs. calidad, especialización vs. cobertura, madurez digital vs. tamaño]

### Posición actual: fortalezas relativas
[En qué dimensiones la empresa cliente está mejor posicionada que sus competidores — con evidencia]

### Posición actual: vulnerabilidades relativas
[En qué dimensiones está peor posicionada — con evidencia]

---

## 6. OPORTUNIDADES DE DIFERENCIACIÓN CON IA

[Para cada oportunidad: qué proceso, qué herramienta de IA, qué ventaja competitiva generaría, quién en la competencia ya lo hace o no lo hace]

### Oportunidades donde la IA daría ventaja sobre competidores que ya adoptaron
[Áreas donde algunos competidores tienen IA y la empresa cliente aún no — riesgo de quedarse atrás]

### Oportunidades donde la IA abriría terreno inexplorado
[Procesos que nadie en el sector ha automatizado todavía — potencial de diferenciación premium]

### Quick Wins de IA recomendados (en orden de impacto competitivo)
| Quick Win | Proceso actual | Herramienta sugerida | Ventaja competitiva generada |
|-----------|---------------|---------------------|------------------------------|
[3-4 filas específicas]

---

## 7. SEÑALES DE PUNTO CIEGO COMPETITIVO

[Competidores que probablemente el prospecto no mencione en la llamada pero que sí compiten por sus clientes]

### Competidores no obvios a señalar en la llamada
[Para cada uno: nombre + por qué compite indirectamente + cómo señalarlo sin sonar condescendiente]

### Tendencias del sector que pueden cambiar el mapa competitivo
[Nuevos entrantes, consolidaciones recientes, modelos de negocio disruptivos que el cliente quizás no está viendo]

---

## 8. SÍNTESIS PARA LA LLAMADA

[3-5 talking points listos para usar. Específicos, con gancho de datos, orientados a crear urgencia o curiosidad en el cliente sobre su posición competitiva]

**Talking Point 1:** [Dato de brecha competitiva + pregunta de apertura]  
**Talking Point 2:** [Qué está haciendo la competencia que el cliente no sabe]  
**Talking Point 3:** [Oportunidad de diferenciación con IA que nadie está aprovechando]  
**Talking Point 4:** [Señal de punto ciego — competidor que no van a mencionar]  
**Talking Point 5:** [Urgencia — qué pasa si no actúan en los próximos 12 meses]

---

## FUENTES CONSULTADAS

[Lista de URLs, reportes y fuentes con fecha de consulta]

---
*Reporte generado por /competitor-analyst · Mejía, IA & CIA · [fecha]*
```

---

## NOTAS OPERATIVAS

**Naming:** `[EmpresaCamelCase]_Competencia_CO_[YYYYMMDD].[ext]`  
Ejemplo: `ARUS_Competencia_CO_20260512.md`, `CreacionesNadar_Competencia_CO_20260512.docx`

**Vigencia:** Este análisis es válido ~3-6 meses. El mapa competitivo cambia más rápido que el análisis sectorial.

**Pipeline completo:** company-analyst → competitor-analyst → call prep → diagnostic report  
Este skill consume el output de company-analyst y alimenta el call prep skill.

**Nota sobre precios:** Los precios de los competidores raramente son públicos para servicios B2B. Si no están disponibles, documentar la percepción de precio relativo ("premium", "mid-market", "low-cost") con evidencia (tipo de cliente, testimonios, posicionamiento de marketing).
