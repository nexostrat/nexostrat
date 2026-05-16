---
name: company-analyst
description: |
  Analista de compañías — Mejía, IA & CIA. Genera un reporte de inteligencia empresarial completo (13 secciones) sobre una empresa colombiana antes de una llamada exploratoria: perfil general, productos/servicios, presencia digital, datos financieros de Supersociedades, FODA, 5 Fuerzas de Porter, cadena de valor, madurez digital (1-5), señales de presupuesto, Quick Win candidates, conclusiones, talking points y señales de alerta. Output: .md + .docx.

  Activar SIEMPRE ante: "analiza la empresa X", "investiga [empresa]", "prepara el análisis de [compañía]", "briefing de [empresa]", "company analysis", "análisis de prospecto", "dame todo sobre [empresa]", "quiero saber sobre [empresa] antes de la llamada", NIT + contexto de consultoría, o cualquier variante que implique investigar una empresa antes de una reunión comercial. Ante la duda, activar.
---

# Company Analyst — Reporte de Inteligencia Empresarial

**Uso:** Interno — Mejía, IA & CIA  
**Output:** Reporte .md + .docx  
**Propósito:** Alimentar el skill de preparación de llamada y el skill de reporte diagnóstico

---

## REGLA ANTI-ALUCINACIÓN (obligatoria en cada sección)

Si una fuente no está disponible, no arroja resultados, o el sitio no responde:
→ Escribe explícitamente: **"No se encontró información en [nombre de la fuente]."**

**NUNCA:**
- Inventar cifras financieras
- Asumir productos/servicios no confirmados
- Inferir fundadores o historia sin fuente
- Omitir una sección porque no encontraste datos (siempre incluirla con el texto de no-encontrado)

---

## WORKFLOW COMPLETO

### PASO 1 — Extraer datos financieros de Supersociedades

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

### PASO 2 — Investigación web (hacer todas las búsquedas, en este orden)

Usa WebSearch y WebFetch para cada una. Lee `references/sources_guide.md` para URLs exactas y qué buscar en cada fuente.

**2a. Sitio web oficial**
- Busca "[empresa] sitio web oficial Colombia"
- Visita el sitio, extrae: productos/servicios, quiénes somos, cobertura geográfica, tecnologías visibles, formularios/automatización visible

**2b. Redes sociales**
- LinkedIn: busca la empresa y extrae: tamaño (# empleados declarado), empleados recientes, actividad de posts
- Instagram/Facebook: presencia, frecuencia de posts, engagement visible
- Si no tiene redes: documentarlo explícitamente

**2c. Reseñas y reputación**
- Google reviews (busca "[empresa] opiniones google")
- Trustpilot si aplica
- Reclamos.co u otras plataformas de quejas

**2d. Prensa y noticias**
- Busca en portafolio.co, dinero.com, larepublica.co, elcolombiano.com
- Términos: "[empresa] Colombia", "[empresa] noticias", "[razón social] expansión"

**2e. RUES (registro legal)**
- Busca "[empresa] RUES rues.confecamaras.co"
- Extrae: estado matrícula, tipo societario, fecha constitución

**2f. Contexto sectorial**
- Busca el sector CIIU en contexto colombiano
- Tamaño del mercado, tendencias, competidores principales en Colombia

---

### PASO 3 — Sintetizar el reporte

Escribe el reporte completo usando el template de la sección siguiente.

**Reglas de calidad:**
- Ser directo y sin diplomacia (uso interno)
- Citar la fuente de cada dato relevante
- Cuantificar siempre que sea posible (%, COP, #empleados, años)
- La sección de Quick Wins y Talking Points debe ser específica para ESTA empresa, no genérica
- El FODA debe tener MÍNIMO 4 puntos por cuadrante, todos basados en evidencia real

---

### PASO 4 — Generar outputs

**4a. Guardar reporte .md** en el directorio de outputs de la sesión.

**4b. Generar DOCX** usando el skill de Word:
- Lee el skill: `/var/folders/.../skills/docx/SKILL.md`
- Genera un documento Word profesional con el mismo contenido
- Nombre del archivo: `EMPRESA_AnalisisCompania_YYYYMMDD.docx`

---

## TEMPLATE DEL REPORTE

Usa exactamente esta estructura. No omitas ninguna sección.

```
# ANÁLISIS DE COMPAÑÍA: [NOMBRE EN MAYÚSCULAS]

**Clasificación:** Interno — Uso exclusivo Mejía, IA & CIA  
**Fecha de análisis:** [fecha]  
**Analista:** Skill de Análisis de Compañías v1  
**NIT:** [NIT o "No encontrado"]  
**CIIU:** [código + descripción]  
**Sector:** [sector en español]  

---

## 1. PERFIL GENERAL

**Historia y fundación:** [año de constitución, origen, hitos relevantes. Fuente: RUES / web]  
**Fundadores:** [nombres si disponibles. Fuente: web / LinkedIn]  
**Sede principal:** [dirección/ciudad]  
**Cobertura geográfica:** [ciudades/regiones donde opera]  
**Tamaño estimado:** [# empleados declarado o estimado. Fuente]  
**Tipo societario:** [SAS / SA / Ltda / otro]  
**Estado legal:** [Activa / En liquidación / En reorganización]  
**Estructura corporativa:** [grupo empresarial, filiales, holding si aplica]  

*Fuentes consultadas: [lista]*

---

## 2. PRODUCTOS Y SERVICIOS

**Portafolio principal:**  
[descripción de productos/servicios con suficiente detalle para entender el negocio]

**Precios públicos:** [si disponibles en el sitio web; si no: "No se encontraron precios públicos en el sitio web."]  

**Propuesta de valor declarada:** [lo que dicen en su web/materiales]  

**Canales de venta:** [directo, distribuidores, e-commerce, etc.]  

*Fuentes consultadas: [lista]*

---

## 3. PRESENCIA DIGITAL

**Sitio web:**  
- URL: [url o "No se encontró sitio web"]
- UX general: [descripción honesta: profesional/amateur/desactualizado/etc.]
- Tecnología visible: [CMS si detectable, chat en vivo, formularios, e-commerce]
- SEO básico: [¿aparece en búsquedas relevantes? ¿meta descripción visible?]
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
- Reclamos.co / otras: [si aplica]

**Puntuación de Madurez Digital: [X]/5**  
- 1 = Sin presencia digital / todo manual
- 2 = Sitio web básico, sin automatización
- 3 = Presencia digital funcional, algo de automatización
- 4 = Digitalización avanzada, CRM, marketing digital activo
- 5 = Empresa nativa digital, automatización extensiva

**Justificación:** [2-3 frases explicando la puntuación]

*Fuentes consultadas: [lista]*

---

## 4. DATOS FINANCIEROS (Supersociedades Colombia)

> ⚠️ Valores en miles de pesos colombianos (COP miles). Para convertir a USD usar TRM vigente (~$4,200 COP/USD).

**Período de reporte:** [fecha de corte]  

| Indicador | Periodo Actual | Periodo Anterior | Variación |
|-----------|---------------|-----------------|-----------|
| Ingresos operacionales | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Costo de ventas | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Ganancia bruta | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Utilidad operacional | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Utilidad neta | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Total activos | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Total pasivos | $ [valor] miles COP | $ [valor] miles COP | [%] |
| Patrimonio total | $ [valor] miles COP | $ [valor] miles COP | [%] |

**Indicadores calculados:**  
- Margen bruto: [%]
- Margen neto: [%]
- Razón de endeudamiento: [pasivos/activos %]
- Ingresos en USD aprox.: [conversión]

**Interpretación financiera:** [3-5 frases sobre la salud financiera, crecimiento, solvencia]

*Fuente: Supersociedades Colombia — archivo 210030 (Balance) y 310030 (P&G)*  
*Si no encontrado: "No se encontró en Supersociedades. Empresa no vigilada por esta entidad o no reportó en el período disponible."*

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

**Aplicadas al contexto específico de esta empresa en Colombia.**

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

**Observación clave:** [1-2 frases sobre dónde está el mayor potencial de automatización basado en la cadena de valor]

---

## 8. CANDIDATOS A QUICK WIN DE IA

> Los 3-5 procesos con mayor potencial de automatización identificables desde el exterior.
> Específicos para ESTA empresa — no genéricos.

**QW1: [Nombre del proceso]**  
- Evidencia observada: [qué viste que sugiere este proceso es manual]
- Impacto estimado: [tiempo, costo, errores]
- Solución probable: [tipo de automatización: agente, workflow, análisis, etc.]
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
| Ingresos anuales (COP miles) | [valor] | [contexto] |
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

> 5 preguntas específicas para ESTA empresa. No preguntas genéricas.
> Cada una debe surgir de algo concreto observado en la investigación.

1. **[Tema]:** "[pregunta específica]"  
   *Por qué preguntar esto: [lo que observaste que hace relevante esta pregunta]*

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
> Si no hay señales de alerta, escribir: "No se identificaron señales de alerta significativas."

⚠️ [Señal 1 si aplica: deuda alta, litigios, sector en declive, reseñas muy negativas, empresa en liquidación, etc.]

⚠️ [Señal 2 si aplica]

---

## FUENTES CONSULTADAS

| Fuente | URL/Referencia | Información obtenida | Disponibilidad |
|--------|---------------|---------------------|----------------|
| Supersociedades | Archivo local | Datos financieros | [Encontrado/No encontrado] |
| Sitio web | [url] | [qué obtuviste] | [Disponible/No disponible] |
| LinkedIn | [url] | [qué obtuviste] | [Disponible/No disponible] |
| RUES | rues.confecamaras.co | [qué obtuviste] | [Disponible/No disponible] |
| Prensa | [medios] | [qué obtuviste] | [Disponible/No disponible] |
| Google reviews | [búsqueda] | [qué obtuviste] | [Disponible/No disponible] |

---
*Reporte generado por skill company-analyst v1 — Mejía, IA & CIA*  
*Para uso interno exclusivo. No compartir con el prospecto.*
```

---

## NOTAS OPERATIVAS

**Sobre los archivos financieros:**
Los archivos de Supersociedades están en `assets/` junto a este skill:
- `supersociedades_balance_general.xlsx` → Balance general (activos, pasivos, patrimonio)
- `supersociedades_estado_resultados.xlsx` → Estado de resultados (ingresos, costos, utilidades)

Ambos archivos contienen datos de ~3,100 empresas colombianas reportando bajo NIIF.  
Los valores están en **miles de pesos colombianos (COP miles)**.  
Cada empresa aparece dos veces: "Periodo Actual" y "Periodo Anterior".

**Sobre el DOCX:**  
Después de escribir el .md completo, usa el skill de docx para generar el Word.  
Llama: `Read /var/folders/.../skills/docx/SKILL.md` y sigue sus instrucciones.  
El documento debe verse profesional con la misma estructura de secciones.

**Sobre el tiempo de ejecución:**
Este skill hace bastante trabajo. Es normal que tome 10-20 minutos.  
Ricardo no necesita hacer nada mientras tanto.
