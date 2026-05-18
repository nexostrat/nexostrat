---
name: industry-analyst
description: |
  Analista de industrias — Nexostrat. Genera un reporte sectorial completo (10 secciones) sobre una industria colombiana o mexicana: caracterización, actores principales, tendencias 3-5 años, proveedores, clientes, regulación, impacto IA, PESTEL, madurez digital y señales de oportunidad para consultoría. Acepta el reporte de company-analyst para identificar el sector automáticamente y detectar el país (CO vs MX). Output: .md + .docx. Reutilizable por sector.

  Activar SIEMPRE ante: "analiza el sector X", "análisis de la industria X", "¿cómo está el mercado de X en Colombia/México?", "dame un análisis sectorial", "investiga la industria X", "industry analysis", "¿qué tan madura digitalmente está la industria X?", "¿dónde puede entrar IA en el sector X?", cuando el usuario comparte un .md de company-analyst y necesita el análisis sectorial, o cuando se necesita el siguiente paso del pipeline de Nexostrat. Ante la duda, activar.
---

# Industry Analyst — Reporte de Inteligencia Sectorial

**Uso:** Interno — Nexostrat  
**Input:** Reporte .md de company-analyst (`*_AnalisisCompania_*.md`) — opcional, pero recomendado cuando se corre en pipeline  
**Output:** `SECTOR_CO_YYYYMMDD.md` / `SECTOR_MX_YYYYMMDD.md` + `.docx`  
**Propósito:** Alimentar el skill de preparación de llamada y el skill de reporte diagnóstico. Reutilizable: correr una vez por sector, no por empresa.

---

## SISTEMA DE CONFIANZA DE DATOS — REGLA ANTI-ALUCINACIÓN

### Etiquetas obligatorias

Aplica estas etiquetas a **todos** los datos cuantitativos y afirmaciones verificables del reporte:

| Etiqueta | Significado | Cuándo usarla |
|---|---|---|
| ✅ | Verificado | Extraído directamente de la fuente primaria citada |
| ⚠️ | Estimado | Inferido, calculado, o de fuente secundaria/no oficial |
| ❓ | Sin datos | Búsqueda realizada — dato no encontrado en ninguna fuente |

**Formato obligatorio en el reporte:**
- `✅ Tamaño del mercado: COP $12.4 billones (DANE, Cuentas Nacionales 2024)`
- `⚠️ Tasa de adopción de IA: ~15% de empresas del sector (estimado, Deloitte Tech Trends 2023)`
- `❓ PIB sectorial México: No se encontró información en INEGI para este subsector.`

### Reglas sin excepción

1. **Sin etiqueta = dato inválido.** Todo número o afirmación verificable lleva etiqueta + fuente + año. No existe el dato sin fuente.
2. **Datos de más de 2 años:** añadir `⚠️ (dato de [año] — verificar vigencia)` aunque vengan de fuente primaria.
3. **Fuentes discrepantes:** Si dos fuentes dan cifras distintas para el mismo indicador, mostrar ambas: `⚠️ Tamaño del mercado: entre X (Fuente A, año) y Y (Fuente B, año) — cifras no reconciliadas.`
4. **Hechos vs. análisis:** Las conclusiones e interpretaciones van bajo el header `> 🔍 Análisis:` para separarlas visualmente de los datos reportados.
5. **Benchmarks y casos de IA:** Solo citar implementaciones reales con nombre de empresa o estudio + fuente + año. Nunca: "empresas del sector han logrado X% de ahorro" sin fuente nombrada. Si no hay caso verificable → omitir el dato.
6. **Fuente no disponible:** Escribir exactamente `❓ No se encontró información en [nombre de la fuente].` — nunca omitir la búsqueda ni sustituir con datos inventados.
7. **Prohibido sin fuente:** "aproximadamente", "se estima", "es probable" aplicados a datos específicos. Reservar para análisis interpretativo únicamente.
8. **Nunca omitir una sección:** Si no hay datos, incluir la sección con ❓ y la declaración de búsqueda realizada. La ausencia de datos es información válida.

---

## WORKFLOW COMPLETO

### Paso 0 — Identificar el sector y el país

**Si hay un reporte de company-analyst disponible (pipeline):**  
Busca en el directorio de trabajo un archivo con el patrón `*_AnalisisCompania_*.md`. Si existe, léelo y extrae:
- El sector o industria de la empresa (del campo CIIU o SCIAN, los productos/servicios principales)
- El **país** de la empresa: Colombia (campo "NIT" o "País: Colombia") o México (campo "RFC" o "País: México")
- El nombre canónico del sector en ese país
- Subsectores relevantes para el tipo de empresa
- Contexto de tamaño y geografía

Usa esta extracción como base: así el reporte sectorial no es genérico sino calibrado al tipo de empresa que lo originó.

**Si no hay reporte de company-analyst (uso standalone):**  
Usa el sector y país indicados en el prompt directamente. Si no están especificados con claridad suficiente, pregunta antes de comenzar.

**Con el sector y país identificados, define:**
- ¿Cuál es el nombre canónico del sector en ese país? (ej: "sector salud privado", "industria textil y confección", "sector TI y software")
- ¿Hay subsectores relevantes que deben cubrirse?
- ¿Hay empresas internacionales con operaciones significativas en ese país?

**Nomenclatura de archivos según país:**
- Colombia → `SECTOR_CO_YYYYMMDD.md` / `SECTOR_CO_YYYYMMDD.docx`
- México → `SECTOR_MX_YYYYMMDD.md` / `SECTOR_MX_YYYYMMDD.docx`

### Paso 1 — Investigar cada sección sistemáticamente

Para cada sección del reporte, usa las fuentes del país correspondiente.

**Para Colombia:** Consulta `references/sources_guide.md` para fuentes específicas. Orden recomendado:
1. Asociación gremial del sector (ANDI, ACOPI, asociación específica) — fuente más valiosa para cifras nacionales
2. DANE — estadísticas nacionales del sector
3. MinComercio / DNP — políticas y proyecciones
4. Press colombiana — portafolio.co, larepublica.co, dinero.com, elcolombiano.com
5. LinkedIn + web corporativa de los líderes del sector
6. Reportes de consultoras (Deloitte, McKinsey, PwC) versiones públicas
7. Fuentes internacionales con datos de Colombia: World Bank, IFC, CEPAL

**Para México:** Orden recomendado:
1. Asociación gremial del sector en México (CANACINTRA, CONCAMIN, CÁMARA DE COMERCIO DE MÉXICO, o asociación específica del sector)
2. INEGI — estadísticas nacionales (inegi.org.mx)
3. Secretaría de Economía / CONCANACO — políticas y proyecciones
4. Press mexicana — expansión.mx, elfinanciero.com.mx, eleconomista.com.mx, milenio.com, forbes.com.mx
5. LinkedIn + web corporativa de los líderes del sector en México
6. Reportes de consultoras versiones públicas para México
7. Fuentes internacionales con datos de México: World Bank, IDB, CEPAL

**Para la sección de IA (Sección 7), busca también en ambos países:**
- "inteligencia artificial [sector] [Colombia/México] casos"
- "[sector] automation [país] 2024 2025"
- Herramientas de IA adoptadas globalmente en el sector con presencia en el país objetivo

### Paso 2 — Escribir el reporte completo

Usa el template de abajo. **No omitas ninguna sección.** Si los datos de una subsección son insuficientes, escríbelo explícitamente. Cada sección debe tener densidad real: datos concretos, nombres de empresas reales, cifras con fuente y año.

El reporte debe tener al menos 3,500 palabras.

### Paso 3 — Generar el .docx

Una vez que el .md esté completo y guardado, ejecuta:

```bash
pip install python-docx --break-system-packages -q
python skills/02_industry_analyst/scripts/generate_docx.py <ruta_al_md> <ruta_output_docx>
```

Guarda ambos archivos en el directorio de outputs con el formato:  
- Colombia: `SECTOR_CO_YYYYMMDD.md` y `SECTOR_CO_YYYYMMDD.docx`
- México: `SECTOR_MX_YYYYMMDD.md` y `SECTOR_MX_YYYYMMDD.docx`

---

## TEMPLATE DEL REPORTE

Usa exactamente estos encabezados. El texto entre corchetes es guía — reemplázalo con contenido real.

```markdown
# Análisis de Industria: [NOMBRE DEL SECTOR]
**[Colombia / México] · [Mes Año]**  
**Preparado por:** Nexostrat — Uso Interno  
**Reutilizable para prospectos del sector hasta:** [fecha estimada de vigencia, ej: dic 2026]

---

## 1. CARACTERIZACIÓN DEL SECTOR

### Definición y alcance
[Qué incluye este sector, qué excluye, cómo lo clasifica el DANE/CIIU (Colombia) o INEGI/SCIAN (México)]

### Subsectores principales
[Lista de subsectores con descripción breve de cada uno]

### Tamaño del mercado en [Colombia/México]
- **PIB sectorial / participación en PIB nacional:** [dato + fuente + año]
- **Ingresos del sector:** [cifra en COP/MXN o USD + fuente + año]
- **Número de empresas activas:** [dato + fuente]
- **Empleo directo generado:** [dato + fuente]
- **Tasa de crecimiento reciente:** [% CAGR últimos 3-5 años + fuente]

### Cifras clave adicionales
[2-4 métricas específicas del sector relevantes para entender su dinámica]

---

## 2. PRINCIPALES ACTORES

### Líderes nacionales
| Empresa | Tipo | Facturación aprox. | Presencia | Notas clave |
|---------|------|-------------------|-----------|-------------|
[5-8 empresas líderes en ese país con datos reales]

### Internacionales con presencia en [Colombia/México]
| Empresa | País de origen | Tipo de presencia | Participación en [CO/MX] |
|---------|---------------|-------------------|--------------------------|
[3-6 empresas internacionales con operaciones reales]

### Panorama competitivo
[Descripción del nivel de concentración del mercado: ¿hay un líder claro? ¿mercado fragmentado? ¿hay consolidación en curso?]

---

## 3. TENDENCIAS CLAVE (3–5 AÑOS)

### Tendencias tecnológicas
[2-3 tendencias tech con ejemplos concretos de adopción en el sector]

### Tendencias del consumidor / cliente final
[Cómo está cambiando el comportamiento del comprador o usuario en este sector]

### Tendencias regulatorias
[Cambios regulatorios esperados o en curso que impactarán el sector]

### Tendencias de globalización / internacionalización
[Qué está pasando a nivel global que llegará al país en 2-4 años]

---

## 4. ANÁLISIS DE PROVEEDORES

### Estructura de la cadena de suministro
[Descripción de los principales tipos de proveedores del sector]

### Concentración y poder de negociación
[¿Hay pocos proveedores dominantes? ¿Cuánto poder tienen sobre precios y condiciones?]

### Disponibilidad y riesgos de suministro
[Vulnerabilidades en la cadena, dependencia de importaciones, proveedores locales vs. internacionales]

### Tendencias en precios de insumos
[Evolución reciente y perspectivas de costos de los principales insumos]

---

## 5. ANÁLISIS DE CLIENTES

### Perfil del comprador actual
[Quién compra, cómo decide, cuál es el ciclo de compra típico]

### Cómo cambió el comprador en los últimos 3 años
[Cambios concretos en comportamiento, expectativas y proceso de compra]

### Qué valoran hoy que antes no valoraban
[2-4 factores de decisión emergentes — velocidad, transparencia, sostenibilidad, autoservicio, etc.]

### Segmentos de mayor crecimiento
[Qué tipo de cliente está creciendo más rápido dentro del sector]

---

## 6. MARCO REGULATORIO

### Entidad reguladora principal
[Nombre, rol, jurisdicción — específica del país]

### Normativa vigente más relevante
| Norma / Ley | Año | Qué regula | Impacto en el sector |
|-------------|-----|------------|---------------------|
[4-6 normas reales con descripción concreta]

### Cambios regulatorios en curso o anticipados
[Proyectos de ley, resoluciones en discusión, cambios internacionales que puedan impactar]

### Riesgos de compliance relevantes para empresas del sector
[Qué incumplimientos son más frecuentes o costosos]

---

## 7. IMPACTO DE LA IA EN EL SECTOR

### Estado actual de adopción
[Nivel general de adopción de IA en el sector en [Colombia/México] vs. global]

### Casos de uso ya implementados (con nombres de empresas o herramientas reales)
| Caso de uso | Herramienta / empresa | País / empresa | Resultado reportado |
|-------------|----------------------|----------------|---------------------|
[4-6 casos reales con nombres concretos — no genéricos]

### Herramientas de IA dominantes en el sector
[Software, plataformas, o modelos que ya están siendo adoptados por empresas del sector]

### Barreras de adopción en [Colombia/México]
[Por qué algunas empresas del sector todavía no han adoptado IA — presupuesto, talento, regulación, cultura]

---

## 8. OPORTUNIDADES Y AMENAZAS DEL ENTORNO (PESTEL)

| Factor | Oportunidades | Amenazas |
|--------|--------------|----------|
| **Político** | [oportunidad concreta] | [amenaza concreta] |
| **Económico** | [oportunidad concreta] | [amenaza concreta] |
| **Social** | [oportunidad concreta] | [amenaza concreta] |
| **Tecnológico** | [oportunidad concreta] | [amenaza concreta] |
| **Ecológico** | [oportunidad concreta] | [amenaza concreta] |
| **Legal** | [oportunidad concreta] | [amenaza concreta] |

---

## 9. MADUREZ DIGITAL DEL SECTOR

**Calificación: [X]/5**

| Nivel | Descripción |
|-------|-------------|
| 1 | Operaciones manuales, sin sistemas integrados |
| 2 | Sistemas básicos (ERP/CRM básico), baja digitalización de procesos |
| 3 | Digitalización parcial, algunos procesos automatizados, datos disponibles pero no explotados |
| 4 | Alta integración de sistemas, datos centralizados, experimentación con IA |
| 5 | IA como core del negocio, toma de decisiones basada en datos en tiempo real |

### Justificación
[Por qué se asigna este puntaje — evidencia concreta del nivel de madurez observado en el sector]

### Qué hace que avance o retroceda
[Factores que están acelerando o frenando la madurez digital en este sector específico]

---

## 10. SEÑALES DE OPORTUNIDAD PARA CONSULTORÍA DE IA

### Procesos repetitivos y costosos típicos del sector
[3-5 procesos que en la mayoría de empresas del sector se hacen manualmente y son candidatos directos a automatización]

### Quick Wins más replicables
| Quick Win | Proceso que reemplaza | Herramienta sugerida | Impacto esperado |
|-----------|----------------------|----------------------|-----------------|
[3-5 quick wins concretos con impacto cuantificable]

### Casos de éxito de IA en el sector (referenciables en ventas)
[2-3 casos de éxito de otras empresas o consultoras — idealmente con números de ROI o ahorro]

### Perfil del decisor típico en este sector
[Cargo, nivel de conocimiento técnico, principales preocupaciones, cómo suele comprar servicios de consultoría]

### Señales de alerta (empresas del sector donde la venta será difícil)
[Características de empresas del sector que indican baja propensión a comprar]

---

## FUENTES CONSULTADAS

[Lista de todas las URLs, publicaciones y fuentes utilizadas para este reporte, con fecha de consulta]

---
*Reporte generado por /industry-analyst · Nexostrat · [fecha]*
```

---

## NOTAS OPERATIVAS

**Naming convention:**
- Colombia: `[SectorCamelCase]_CO_[YYYYMMDD].[ext]` — ej: `SaludPrivada_CO_20260518.md`
- México: `[SectorCamelCase]_MX_[YYYYMMDD].[ext]` — ej: `LogisticaCarga_MX_20260518.md`

**Vigencia:** Los análisis sectoriales son válidos ~6-12 meses. Incluye siempre la fecha en el nombre del archivo y en el encabezado del reporte.

**Reutilización:** Este reporte es sectorial, no por empresa. Si Ricardo ya tiene un análisis del sector salud de hace 3 meses, puede reutilizarlo para todos los prospectos del sector de ese período.

**Datos financieros de empresas:** Para citar cifras de empresas específicas del sector, el skill de company-analyst tiene acceso a los datos de Supersociedades (Colombia) y a fuentes mexicanas equivalentes. Este skill cubre el sector macro, no empresa individual.
