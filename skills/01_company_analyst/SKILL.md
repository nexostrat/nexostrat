---
name: company-analyst
description: |
  Analista de compañías — Nexostrat. Genera un reporte de inteligencia empresarial completo (13 secciones) sobre una empresa colombiana o mexicana: perfil general, productos/servicios, presencia digital, datos financieros, FODA, 5 Fuerzas de Porter, cadena de valor, madurez digital (1-5), señales de presupuesto, Quick Win candidates, conclusiones, talking points y señales de alerta. Detecta el país automáticamente (NIT = Colombia → Supersociedades; RFC = México → SAT/DENUE/SIEM); si no está claro, lo pregunta. Output: .md + .docx.

  Activar SIEMPRE ante: "analiza la empresa X", "investiga [empresa]", "prepara el análisis de [compañía]", "briefing de [empresa]", "company analysis", "análisis de prospecto", "dame todo sobre [empresa]", "quiero saber sobre [empresa] antes de la llamada", NIT/RFC + contexto de consultoría, o cualquier variante que implique investigar una empresa antes de una reunión comercial. Ante la duda, activar.
---

# Company Analyst — Reporte de Inteligencia Empresarial

**Uso:** Interno — Nexostrat  
**Output:** Reporte .md + .docx  
**Propósito:** Alimentar el skill de preparación de llamada y el skill de reporte diagnóstico

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
- `✅ Ingresos: COP $4.200M (Supersociedades, 2024)`
- `⚠️ Empleados: ~80-120 (LinkedIn, estimado por ofertas de empleo publicadas)`
- `❓ Precio relativo: No se encontró información pública.`

### Reglas sin excepción

1. **Sin etiqueta = dato inválido.** Todo número o afirmación verificable lleva etiqueta + fuente + año. No existe el dato sin fuente.
2. **Datos de más de 2 años:** añadir `⚠️ (dato de [año] — verificar vigencia)` aunque vengan de fuente primaria.
3. **Hechos vs. análisis:** Las conclusiones e interpretaciones van bajo el header `> 🔍 Análisis:` para separarlas visualmente de los datos reportados.
4. **Benchmarks y ROI:** Solo citar casos reales con nombre de empresa o estudio + fuente + año. Nunca escribir "empresas similares logran X%" sin fuente nombrada. Si no hay caso verificable → omitir el dato, no inventarlo.
5. **Fuente no disponible:** Escribir exactamente `❓ No se encontró información en [nombre de la fuente].` — nunca omitir la búsqueda ni sustituir con datos inventados.
6. **Prohibido sin fuente:** "aproximadamente", "se estima", "es probable" y "suele ser" aplicados a datos específicos. Reservar estas frases para análisis interpretativo, no para reportar datos.
7. **Nunca omitir una sección:** Si no hay datos, incluir la sección con la etiqueta ❓ correspondiente. La ausencia de datos es información valiosa.

### Verificación de identidad de la empresa

Antes de correr cualquier búsqueda, confirma que el nombre comercial y el NIT/RFC proporcionados corresponden a la misma entidad legal. Errores frecuentes: empresas con nombres similares en el mismo sector, holdings y filiales con NITs distintos, empresas con cambio de razón social. Si hay ambigüedad → mostrar las opciones encontradas y pedir confirmación explícita del usuario antes de continuar.

---

## WORKFLOW COMPLETO

### PASO 0 — Detectar el país de la empresa

**Si el usuario indicó el país explícitamente:** Usa ese país directamente.

**Si no lo indicó, detecta automáticamente:**
- **NIT** (formato: XXXXXXXXX-X o número de 9 dígitos) → **Colombia**
- **RFC** (formato: 3-4 letras + 6 dígitos + 3 homoclave) → **México**
- Sufijo societario "SA de CV", "SRL de CV", "SAPI de CV", "SC" → **México**
- Sufijo societario "SAS", "S.A.S.", "Ltda", "E.S.P." → **Colombia**
- Ciudad mencionada: Bogotá, Medellín, Cali, Barranquilla, Cartagena → Colombia
- Ciudad mencionada: CDMX, Guadalajara, Monterrey, Puebla, Tijuana → México
- Si el contexto sigue sin ser claro, pregunta antes de continuar: *"¿La empresa es colombiana o mexicana?"*

Según el país detectado, sigue el flujo correspondiente:
- 🇨🇴 **Colombia** → PASO 1-CO + fuentes colombianas en PASO 2
- 🇲🇽 **México** → PASO 1-MX + fuentes mexicanas en PASO 2

---

### PASO 1-CO (Colombia) — Extraer datos financieros de Supersociedades

Ejecuta el script Python antes de cualquier búsqueda web. Ruta del script:
`<skill_dir>/scripts/extract_financials.py`

```bash
python3 <skill_dir>/scripts/extract_financials.py "<nombre_empresa_o_NIT>"
```

El script buscará en los archivos de Supersociedades incluidos en assets/ y devolverá:
- NIT confirmado, razón social exacta, CIIU, ciudad
- Activos totales, pasivos totales, patrimonio, ingresos, utilidad neta
- Período de corte del reporte
- Señal de presupuesto (clasificación automática)

Si el NIT no fue proporcionado, el script buscará por nombre con matching flexible.

**Si la empresa no está en Supersociedades:** escribir "No se encontró en Supersociedades. Empresa no vigilada o datos no disponibles." No inventar cifras.

---

### PASO 1-MX (México) — Verificar datos en SAT / SIEM / DENUE

Para empresas mexicanas no hay una base centralizada equivalente a Supersociedades. Ejecuta estas búsquedas:

**RFC y estado fiscal:**
- Busca "[empresa] RFC México" para confirmar el RFC
- Estado fiscal en sat.gob.mx → "Activo" o "Cancelado"
- Busca en SIEM (siem.gob.mx): razón social, actividad económica, municipio

**Tamaño y actividad:**
- DENUE (inegi.org.mx/app/mapa/denue/): busca por nombre de empresa o actividad económica para confirmar ubicación, número de empleados estimado, sector SCIAN
- Número de empleados IMSS: busca "[empresa] empleados IMSS" en prensa

**Datos financieros:**
- Si cotiza en BMV: bolsa.mx → sección "Emisoras" → reportes anuales y trimestrales
- Si no cotiza: los estados financieros NO son públicos en México para empresas privadas
- Busca en prensa: expansión.mx, elfinanciero.com.mx, eleconomista.com.mx, forbes.com.mx
- Término: "[empresa] ingresos facturación ventas [año reciente]"

Si no se encuentran datos financieros → escribe: **"No se encontraron estados financieros públicos. En México, esta información no es obligatoriamente pública para empresas no cotizadas en la BMV."**

---

### PASO 2 — Investigación web (hacer todas las búsquedas, en este orden)

Usa WebSearch y WebFetch para cada una.

**Para empresas colombianas**, consulta `references/sources_guide.md` para URLs exactas. Fuentes clave:
- Sitio web oficial, LinkedIn, Instagram/Facebook
- Reseñas: Google reviews, Trustpilot, Reclamos.co
- Prensa: portafolio.co, dinero.com, larepublica.co, elcolombiano.com
- Registro legal: RUES (rues.confecamaras.co)

**Para empresas mexicanas**, usa estas fuentes equivalentes:
- Sitio web oficial, LinkedIn, Instagram/Facebook (igual que Colombia)
- Reseñas: Google reviews, Trustpilot, Profeco (profeco.gob.mx)
- Prensa: expansión.mx, elfinanciero.com.mx, eleconomista.com.mx, milenio.com, forbes.com.mx
- Registro legal: SIEM (siem.gob.mx) + DENUE (inegi.org.mx/app/mapa/denue/)

**2a. Sitio web oficial**
- Busca "[empresa] sitio web oficial [Colombia/México]"
- Extrae: productos/servicios, quiénes somos, cobertura geográfica, tecnologías visibles, formularios/automatización visible

**2b. Redes sociales**
- LinkedIn: tamaño (# empleados declarado), empleados recientes, actividad de posts
- Instagram/Facebook: presencia, frecuencia de posts, engagement visible

**2c. Reseñas y reputación**
- Google reviews: "[empresa] opiniones google"
- Trustpilot si aplica
- Colombia: Reclamos.co | México: Profeco (profeco.gob.mx)

**2d. Prensa y noticias**
- Usa los medios del país correspondiente (ver arriba)
- Términos: "[empresa] [país]", "[empresa] noticias", "[razón social] expansión"

**2e. Registro legal**
- Colombia: RUES (rues.confecamaras.co) → estado matrícula, tipo societario, fecha constitución
- México: SIEM (siem.gob.mx) + RFC en SAT

**2f. Contexto sectorial**
- Colombia: CIIU en contexto colombiano (DANE, ANDI, ACOPI)
- México: SCIAN en contexto mexicano (INEGI, CANACINTRA, CONCAMIN)

---

### PASO 3 — Sintetizar el reporte

Escribe el reporte completo usando el template de la sección siguiente.

**Reglas de calidad:**
- Ser directo y sin diplomacia (uso interno)
- Citar la fuente de cada dato relevante
- Cuantificar siempre que sea posible (%, COP/MXN, #empleados, años)
- La sección de Quick Wins y Talking Points debe ser específica para ESTA empresa, no genérica
- El FODA debe tener MÍNIMO 4 puntos por cuadrante, todos basados en evidencia real

---

### PASO 4 — Generar outputs

**4a. Guardar reporte .md** en el directorio de outputs de la sesión.

**4b. Generar DOCX** usando el script local del skill:

```bash
pip install python-docx --break-system-packages -q
python skills/01_company_analyst/scripts/generate_docx.py <ruta_al_md> <ruta_output_docx>
```

- Genera un documento Word profesional con el mismo contenido del .md
- Nombre del archivo: `EMPRESA_AnalisisCompania_YYYYMMDD.docx`

---

## TEMPLATE DEL REPORTE

Usa exactamente esta estructura. No omitas ninguna sección.

```
# ANÁLISIS DE COMPAÑÍA: [NOMBRE EN MAYÚSCULAS]

**Clasificación:** Interno — Uso exclusivo Nexostrat  
**Fecha de análisis:** [fecha]  
**Analista:** Skill de Análisis de Compañías v1  
**País:** [Colombia / México]  
**NIT / RFC:** [número o "No encontrado"]  
**CIIU / SCIAN:** [código + descripción]  
**Sector:** [sector en español]  

---

## 1. PERFIL GENERAL

**Historia y fundación:** [año de constitución, origen, hitos relevantes. Fuente: RUES/SIEM/web]  
**Fundadores:** [nombres si disponibles. Fuente: web / LinkedIn]  
**Sede principal:** [dirección/ciudad]  
**Cobertura geográfica:** [ciudades/regiones donde opera]  
**Tamaño estimado:** [# empleados declarado o estimado. Fuente]  
**Tipo societario:** [SAS / SA / Ltda / SA de CV / SRL de CV / otro]  
**Estado legal:** [Activa / En liquidación / En reorganización]  
**Estructura corporativa:** [grupo empresarial, filiales, holding si aplica]  

*Fuentes consultadas: [lista]*

---

## 2. PRODUCTOS Y SERVICIOS

**Portafolio principal:**  
[descripción de productos/servicios con suficiente detalle para entender el negocio]

**Precios públicos:** [si disponibles; si no: "No se encontraron precios públicos en el sitio web."]  
**Propuesta de valor declarada:** [lo que dicen en su web/materiales]  
**Canales de venta:** [directo, distribuidores, e-commerce, etc.]  

*Fuentes consultadas: [lista]*

---

## 3. PRESENCIA DIGITAL

**Sitio web:**  
- URL: [url o "No se encontró sitio web"]
- UX general: [profesional/amateur/desactualizado/etc.]
- Tecnología visible: [CMS, chat en vivo, formularios, e-commerce]
- SEO básico: [¿aparece en búsquedas relevantes?]
- Velocidad percibida: [rápido/lento/sin dato]

**LinkedIn:**  
- Perfil: [URL o "No encontrado"]
- Empleados declarados: [# o "No disponible"]
- Actividad reciente: [activo/inactivo/sin perfil]

**Otras redes sociales:**  
- Instagram: [URL + seguidores + frecuencia + calidad visual. O "No encontrado"]
- Facebook: [URL + seguidores + actividad. O "No encontrado"]
- Otras: [YouTube, TikTok, Twitter/X si aplica]

**Reseñas y reputación:**  
- Google: [calificación / # reseñas / temas recurrentes positivos y negativos]
- Trustpilot: [si aplica]
- CO — Reclamos.co / MX — Profeco: [si aplica]

**Puntuación de Madurez Digital: [X]/5**  
- 1 = Sin presencia digital / todo manual
- 2 = Sitio web básico, sin automatización
- 3 = Presencia digital funcional, algo de automatización
- 4 = Digitalización avanzada, CRM, marketing digital activo
- 5 = Empresa nativa digital, automatización extensiva

**Justificación:** [2-3 frases explicando la puntuación]

*Fuentes consultadas: [lista]*

---

## 4. DATOS FINANCIEROS

> ⚠️ Colombia: valores en miles de pesos colombianos (COP miles). TRM vigente ~$4,200 COP/USD. Fuente: Supersociedades.  
> ⚠️ México: Si cotiza en BMV, valores en MXN. Si es empresa privada, datos de prensa cuando disponibles — los estados financieros no son públicos.

**Período de reporte:** [fecha de corte o "No disponible"]  

| Indicador | Periodo Actual | Periodo Anterior | Variación | Etiqueta |
|-----------|---------------|-----------------|-----------|----------|
| Ingresos operacionales | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Costo de ventas | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Ganancia bruta | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Utilidad operacional | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Utilidad neta | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Total activos | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Total pasivos | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |
| Patrimonio total | $ [valor] | $ [valor] | [%] | ✅/⚠️/❓ |

**Indicadores calculados:**  
- Margen bruto: [%]
- Margen neto: [%]
- Razón de endeudamiento: [pasivos/activos %]
- Ingresos en USD aprox.: [conversión]

**Interpretación financiera:** [3-5 frases sobre la salud financiera, crecimiento, solvencia]

*Fuente: [Supersociedades Colombia / BMV México / Prensa / No disponible]*  

---

## 5. ANÁLISIS FODA

> Mínimo 4 puntos por cuadrante. Todos basados en evidencia real observada.

### Fortalezas (internas, positivas)
1. [fortaleza con evidencia]
2. [fortaleza con evidencia]
3. [fortaleza con evidencia]
4. [fortaleza con evidencia]

### Oportunidades (externas, positivas)
1. [oportunidad con evidencia]
2. [oportunidad con evidencia]
3. [oportunidad con evidencia]
4. [oportunidad con evidencia]

### Debilidades (internas, negativas)
1. [debilidad con evidencia]
2. [debilidad con evidencia]
3. [debilidad con evidencia]
4. [debilidad con evidencia]

### Amenazas (externas, negativas)
1. [amenaza con evidencia]
2. [amenaza con evidencia]
3. [amenaza con evidencia]
4. [amenaza con evidencia]

---

## 6. CINCO FUERZAS DE PORTER

**Aplicadas al contexto específico de esta empresa en [Colombia/México].**

**1. Rivalidad entre competidores existentes** [Alta/Media/Baja]  
[análisis específico con nombres de competidores si identificados]

**2. Amenaza de nuevos entrantes** [Alta/Media/Baja]  
[barreras de entrada, tendencias del sector]

**3. Poder de negociación de clientes** [Alto/Medio/Bajo]  
[concentración de clientes, switching cost, alternativas disponibles]

**4. Poder de negociación de proveedores** [Alto/Medio/Bajo]  
[dependencia, concentración, materias primas críticas]

**5. Amenaza de productos/servicios sustitutos** [Alta/Media/Baja]  
[tecnologías disruptivas, cambios en preferencias del consumidor]

**Implicación estratégica:** [1-2 frases sobre la posición competitiva general]

---

## 7. CADENA DE VALOR

### Actividades Primarias
| Actividad | Descripción observable | ¿Proceso manual probable? |
|-----------|----------------------|--------------------------|
| Logística de entrada | [descripción] | [Sí/No/Probable] |
| Operaciones/Producción | [descripción] | [Sí/No/Probable] |
| Logística de salida | [descripción] | [Sí/No/Probable] |
| Marketing y ventas | [descripción] | [Sí/No/Probable] |
| Servicio postventa | [descripción] | [Sí/No/Probable] |

### Actividades de Soporte
| Actividad | Descripción observable | ¿Proceso manual probable? |
|-----------|----------------------|--------------------------|
| Infraestructura (admin/finanzas) | [descripción] | [Sí/No/Probable] |
| Gestión de RRHH | [descripción] | [Sí/No/Probable] |
| Tecnología/Sistemas | [descripción] | [Sí/No/Probable] |
| Compras/Aprovisionamiento | [descripción] | [Sí/No/Probable] |

**Observación clave:** [1-2 frases sobre dónde está el mayor potencial de automatización]

---

## 8. CANDIDATOS A QUICK WIN DE IA

> Los 3-5 procesos con mayor potencial de automatización identificables desde el exterior.
> Específicos para ESTA empresa — no genéricos.

**QW1: [Nombre del proceso]**  
- Evidencia observada: [qué viste que sugiere este proceso es manual]
- Impacto estimado: [tiempo, costo, errores]
- Solución probable: [tipo de automatización]
- Dificultad estimada: [Baja/Media/Alta]

**QW2: [Nombre del proceso]**  
[misma estructura]

**QW3: [Nombre del proceso]**  
[misma estructura]

[QW4 y QW5 si aplican]

---

## 9. CONCLUSIONES PARA CONSULTORÍA

> 4-6 observaciones clave para Ricardo antes de la llamada. Directas, sin filtro.

1. **[Título observación]:** [desarrollo]
2. **[Título observación]:** [desarrollo]
3. **[Título observación]:** [desarrollo]
4. **[Título observación]:** [desarrollo]
5. **[Título observación]:** [si aplica]

---

## 10. SEÑALES DE PRESUPUESTO

**Capacidad de inversión estimada:** [Alta / Media / Baja / Insuficiente]  

| Factor | Dato | Interpretación |
|--------|------|----------------|
| Ingresos anuales | [valor en COP/MXN miles] | [contexto] |
| Margen neto | [%] | [saludable/ajustado/negativo] |
| Endeudamiento | [%] | [sostenible/alto/crítico] |
| Tamaño empresa (empleados) | [#] | [micro/pequeña/mediana] |
| Sector | [sector] | [presupuestos típicos del sector] |

**Rango de inversión recomendado:**  
- Diagnóstico: USD $500 [confirmar/revisar]
- Implementación Quick Win: [rango estimado según capacidad]
- Retainer mensual: [rango estimado]

**Conclusión:** [1-2 frases directas sobre si vale la pena invertir tiempo en este prospecto]

---

## 11. TALKING POINTS PARA LA LLAMADA

> 5 preguntas específicas para ESTA empresa. Cada una basada en algo concreto observado en la investigación.

1. **[Tema]:** "[pregunta específica]"  
   *Por qué preguntar esto: [lo que observaste]*

2. **[Tema]:** "[pregunta específica]"  
   *Por qué preguntar esto: [fundamento]*

3. **[Tema]:** "[pregunta específica]"  
   *Por qué preguntar esto: [fundamento]*

4. **[Tema]:** "[pregunta específica]"  
   *Por qué preguntar esto: [fundamento]*

5. **[Tema]:** "[pregunta específica]"  
   *Por qué preguntar esto: [fundamento]*

---

## 12. SEÑALES DE ALERTA

> Aspectos que Ricardo debe conocer antes de invertir tiempo en este prospecto.
> Si no hay señales de alerta: "No se identificaron señales de alerta significativas."

⚠️ [Señal 1 si aplica: deuda alta, litigios, sector en declive, reseñas muy negativas, empresa en liquidación, etc.]

⚠️ [Señal 2 si aplica]

---

## FUENTES CONSULTADAS

| Fuente | URL/Referencia | Información obtenida | Disponibilidad |
|--------|---------------|---------------------|----------------|
| Supersociedades / SAT-SIEM | Archivo local / Web | Datos financieros / Registro | [Encontrado/No encontrado] |
| Sitio web | [url] | [qué obtuviste] | [Disponible/No disponible] |
| LinkedIn | [url] | [qué obtuviste] | [Disponible/No disponible] |
| RUES / SIEM | [url] | [qué obtuviste] | [Disponible/No disponible] |
| Prensa | [medios] | [qué obtuviste] | [Disponible/No disponible] |
| Google reviews | [búsqueda] | [qué obtuviste] | [Disponible/No disponible] |

---
*Reporte generado por skill company-analyst v1 — Nexostrat*  
*Para uso interno exclusivo. No compartir con el prospecto.*
```

---

## NOTAS OPERATIVAS

**Sobre los archivos financieros (Colombia):**
Los archivos de Supersociedades están en `assets/`:
- `supersociedades_balance_general.xlsx` → Balance general
- `supersociedades_estado_resultados.xlsx` → Estado de resultados

Valores en **miles de pesos colombianos (COP miles)**. Cada empresa aparece dos veces: "Periodo Actual" y "Periodo Anterior".

**Sobre datos financieros (México):**
No hay equivalente a Supersociedades para empresas privadas. Si la empresa cotiza en BMV, los reportes están disponibles en bolsa.mx. Para empresas privadas, los estados financieros no son públicos — documentarlo siempre.

**Sobre el DOCX:**  
Después de escribir el .md completo, genera el .docx ejecutando el script local del skill:

```bash
pip install python-docx --break-system-packages -q
python skills/01_company_analyst/scripts/generate_docx.py <ruta_al_md> <ruta_output_docx>
```

**Sobre el tiempo de ejecución:**
Este skill hace bastante trabajo. Es normal que tome 10-20 minutos.
