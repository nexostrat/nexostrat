---
name: industry-analyst
description: |
  Analista de industrias — Nexostrat. Genera un reporte sectorial completo (10 secciones) sobre una industria colombiana: caracterización, actores principales, tendencias 3-5 años, proveedores, clientes, regulación, impacto IA, PESTEL, madurez digital y señales de oportunidad para consultoría. Acepta como input el reporte de company-analyst (`*_AnalisisCompania_*.md`) para identificar el sector automáticamente. Output: .md + .docx. Reutilizable por sector.

  Activar SIEMPRE ante: "analiza el sector X", "análisis de la industria X", "¿cómo está el mercado de X en Colombia?", "dame un análisis sectorial", "investiga la industria X", "industry analysis", "¿qué tan madura digitalmente está la industria X?", "¿dónde puede entrar IA en el sector X?", cuando el usuario comparte un .md de company-analyst y necesita el análisis sectorial, o cuando se necesita el siguiente paso del pipeline de Nexostrat. Ante la duda, activar.
---

# Industry Analyst — Reporte de Inteligencia Sectorial

**Uso:** Interno — Nexostrat  
**Input:** Reporte .md de company-analyst (`*_AnalisisCompania_*.md`) — opcional, pero recomendado cuando se corre en pipeline  
**Output:** `SECTOR_CO_YYYYMMDD.md` + `SECTOR_CO_YYYYMMDD.docx`  
**Propósito:** Alimentar el skill de preparación de llamada y el skill de reporte diagnóstico. Reutilizable: correr una vez por sector, no por empresa.

---

## REGLA ANTI-ALUCINACIÓN (obligatoria en cada sección)

Si una fuente no está disponible, no arroja resultados, o el sitio no responde:
→ Escribe explícitamente: **"No se encontró información en [nombre de la fuente]."**

**Nunca inventes cifras, tamaños de mercado, nombres de empresas, ni casos de uso de IA.**  
Si no encuentras datos recientes, indica el año de los datos que sí encontraste.  
Si encuentras rangos o estimaciones, cítalos como tal: "se estima entre X y Y según [fuente]."

---

## WORKFLOW COMPLETO

### SETUP — Destino de outputs

**Convención canónica (per spec §7).** Cuando se ejecuta dentro del pipeline de un cliente, los outputs van a:

```
pipeline/clients/<slug>/02_industry_analysis/runs/<YYYY-MM-DD_HHMM>_mode-a/
├── final_report.md      ← reporte principal (este skill)
├── final_report.docx    ← versión Word (generada por scripts/generate_docx.py)
└── notes.md             ← opcional: juicio cualitativo del operador (útil para iteración de prompts)
```

Para este skill, `<stage>` = `02_industry_analysis` (corresponde a `pipeline/clients/_template/02_industry_analysis/`).

**Reutilización por sector (no por empresa):** este skill produce análisis sectoriales reutilizables ~6-12 meses. Si ya hay un reporte vigente del sector salud (por ejemplo), reutilizarlo en lugar de regenerarlo. Considerar mantener un caché en `knowledge/sector-reports/` (fuera de pipeline/) para reportes compartidos entre múltiples prospectos.

**Invocación standalone (fuera del pipeline):** guardar en el directorio de trabajo actual usando la convención de nombre `[SectorCamelCase]_CO_YYYYMMDD.md/.docx` (ver Paso 3 abajo).

**Captura de versión:** el SHA del commit Git al momento del run identifica la versión exacta del prompt usado (per ADR-022).

---

### Paso 0 — Identificar el sector

**Si hay un reporte de company-analyst disponible (pipeline):**  
Busca en el directorio de trabajo un archivo con el patrón `*_AnalisisCompania_*.md`. Si existe, léelo y extrae:
- El sector o industria de la empresa (del campo CIIU, la descripción del giro del negocio, o los productos/servicios principales)
- El nombre canónico del sector en Colombia (ej: si la empresa es de software y BPO → "sector TI y software"; si es distribución textil → "industria textil y confección")
- Subsectores relevantes para el tipo de empresa
- Contexto de tamaño y geografía — útil para calibrar qué actores del sector son más comparables

Usa esta extracción como base para el análisis: así el reporte sectorial no es genérico sino calibrado al tipo de empresa que lo originó.

**Si no hay reporte de company-analyst (uso standalone):**  
Usa el sector indicado en el prompt directamente. Si el sector no está especificado con claridad suficiente, pregunta antes de comenzar la investigación.

Con el sector identificado (por cualquiera de las dos vías), define mentalmente:
- ¿Cuál es el nombre canónico del sector en Colombia? (ej: "sector salud privado", "industria textil y confección", "sector TI y software")
- ¿Hay subsectores relevantes que deben cubrirse?
- ¿Hay empresas internacionales con operaciones significativas en Colombia?

Consulta `references/sector_associations.md` para identificar la asociación gremial correspondiente — es la fuente de datos más valiosa para cifras nacionales.

### Paso 1 — Investigar cada sección sistemáticamente

Para cada sección del reporte, consulta `references/sources_guide.md` para saber qué fuentes buscar. El orden recomendado de investigación:

1. Asociación gremial del sector (ANDI, ACOPI, y/o asociación específica)
2. DANE — estadísticas nacionales del sector
3. MinComercio / DNP — políticas y proyecciones
4. Press colombiana — portafolio.co, larepublica.co, dinero.com, elcolombiano.com
5. LinkedIn + web corporativa de los líderes del sector (para actores principales)
6. Reportes de consultoras (Deloitte, McKinsey, PwC) si hay versiones públicas
7. Fuentes internacionales con datos de Colombia: World Bank, IFC, CEPAL

Para la sección de IA (Sección 7), busca también:
- "inteligencia artificial [sector] Colombia casos"
- "[sector] automation Colombia 2024 2025"
- Herramientas de IA adoptadas globalmente en el sector con presencia en CO

### Paso 2 — Escribir el reporte completo

Usa el template de abajo. **No omitas ninguna sección.** Si los datos de una subsección son insuficientes, escríbelo explícitamente (ver regla anti-alucinación). Cada sección debe tener densidad real: datos concretos, nombres de empresas reales, cifras con fuente y año.

El reporte debe tener al menos 3,500 palabras.

### Paso 3 — Generar el .docx

Una vez que el .md esté completo y guardado, ejecuta el renderer local (desde la raíz del repo `/srv/Nexostrat/`):

```bash
pip install python-docx --break-system-packages -q
python3 skills/02_industry_analyst/scripts/generate_docx.py <ruta_al_md> <ruta_output_docx>
```

Guarda ambos archivos en el directorio de outputs (ver § PASO 0 — Setup). Convenciones de nombre:
- **Dentro del pipeline:** `final_report.md` + `final_report.docx` (canónico per spec §7)
- **Standalone:** `[SectorCamelCase]_CO_YYYYMMDD.md/.docx` — ej: `SaludPrivada_CO_20260511.md`, `LogisticaCarga_CO_20260511.md`

---

## TEMPLATE DEL REPORTE

Usa exactamente estos encabezados. El texto entre corchetes es guía — reemplázalo con contenido real.

```markdown
# Análisis de Industria: [NOMBRE DEL SECTOR]
**Colombia · [Mes Año]**  
**Preparado por:** Nexostrat — Uso Interno  
**Reutilizable para prospectos del sector hasta:** [fecha estimada de vigencia, ej: dic 2026]

---

## 1. CARACTERIZACIÓN DEL SECTOR

### Definición y alcance
[Qué incluye este sector, qué excluye, cómo lo clasifica el DANE/CIIU]

### Subsectores principales
[Lista de subsectores con descripción breve de cada uno]

### Tamaño del mercado en Colombia
- **PIB sectorial / participación en PIB nacional:** [dato + fuente + año]
- **Ingresos del sector:** [cifra en COP o USD + fuente + año]
- **Número de empresas activas:** [dato + fuente]
- **Empleo directo generado:** [dato + fuente]
- **Tasa de crecimiento reciente:** [% CAGR últimos 3-5 años + fuente]

### Cifras clave adicionales
[2-4 métricas específicas del sector que sean relevantes para entender su dinámica]

---

## 2. PRINCIPALES ACTORES

### Líderes nacionales
| Empresa | Tipo | Facturación aprox. | Presencia | Notas clave |
|---------|------|-------------------|-----------|-------------|
[5-8 empresas colombianas líderes con datos reales]

### Internacionales con presencia en Colombia
| Empresa | País de origen | Tipo de presencia | Participación en CO |
|---------|---------------|-------------------|---------------------|
[3-6 empresas internacionales con operaciones reales en CO]

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
[Qué está pasando a nivel global que llegará a Colombia en 2-4 años]

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
[Nombre, rol, jurisdicción]

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
[Nivel general de adopción de IA en el sector colombiano vs. global]

### Casos de uso ya implementados (con nombres de empresas o herramientas reales)
| Caso de uso | Herramienta / empresa | País / empresa | Resultado reportado |
|-------------|----------------------|----------------|---------------------|
[4-6 casos reales con nombres concretos — no genéricos]

### Herramientas de IA dominantes en el sector
[Software, plataformas, o modelos que ya están siendo adoptados por empresas del sector]

### Barreras de adopción en Colombia
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
[Características de empresas del sector que indican baja propensión a comprar — presupuesto bajo, cultura resistente, etc.]

---

## FUENTES CONSULTADAS

[Lista de todas las URLs, publicaciones y fuentes utilizadas para este reporte, con fecha de consulta]

---
*Reporte generado por /industry-analyst · Nexostrat · [fecha]*
```

---

## NOTAS OPERATIVAS

**Naming convention:** `[SectorCamelCase]_CO_[YYYYMMDD].[ext]`  
Ejemplos: `SaludPrivada_CO_20260511.md`, `LogisticaCarga_CO_20260511.docx`, `TecnologiaTI_CO_20260511.md`

**Vigencia:** Los análisis sectoriales son válidos ~6-12 meses. Incluye siempre la fecha en el nombre del archivo y en el encabezado del reporte.

**Reutilización:** Este reporte es sectorial, no por empresa. Si Ricardo ya tiene un análisis del sector salud de hace 3 meses, puede reutilizarlo para todos los prospectos clínicos de ese período sin regenerarlo.

**Datos financieros de Supersociedades:** Para citar cifras de empresas específicas del sector, el skill de company-analyst tiene acceso a los Excel de Supersociedades. Este skill no los incluye — cubre el sector macro, no empresa individual.
