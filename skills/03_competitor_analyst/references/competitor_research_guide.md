# Guía de Investigación de Competidores

## Señales de Adopción de IA por Sector

### Salud / Clínicas / IPS
Buscar en sitio web y press:
- Telemedicina propia (no solo por EPS)
- Chatbot de agendamiento (WhatsApp API, web)
- Historia Clínica Electrónica con módulos de IA (ej: Sap, Medilink, Genesys)
- Lectura de imágenes diagnósticas con IA (radiología, patología)
- Modelo predictivo de readmisión o riesgo clínico
- Automatización de glosas / facturación con RPA
- Búsquedas: `"[clínica] inteligencia artificial"`, `"[clínica] telemedicina propia"`, `"[clínica] transformación digital"`

### Logística / Transporte
- TMS (Transport Management System) con IA de ruteo
- WMS (Warehouse Management System) con predicción de inventario
- Tracking en tiempo real (IoT + dashboard)
- Chatbot de rastreo de envíos (WhatsApp)
- Automatización de cotizaciones
- Drones o robots en bodega
- Búsquedas: `"[empresa] TMS"`, `"[empresa] ruteo inteligente"`, `"[empresa] warehouse automation"`

### Retail / Comercio
- Pricing dinámico (algorithmic pricing)
- Recomendación de productos (ML)
- Predicción de demanda / gestión de inventario con IA
- Cashierless checkout (cámaras + IA)
- Programa de fidelización con personalización
- Chatbot de atención al cliente
- Búsquedas: `"[retailer] pricing dinámico"`, `"[retailer] personalización"`, `"[retailer] AI inventory"`

### TI / Software / Consultoría
- Productos o servicios propios con IA embebida
- Uso de IA en desarrollo (GitHub Copilot, Cursor)
- Automatización de soporte con IA
- Portafolio de servicios de IA
- Partnerships con OpenAI, Anthropic, Google, Microsoft Azure AI
- Búsquedas: `"[empresa] IA servicio"`, `"[empresa] inteligencia artificial portafolio"`

### Manufactura / Industria
- Mantenimiento predictivo (IoT + ML)
- Control de calidad con visión computacional
- Optimización de producción con IA
- Gemelo digital (digital twin)
- Búsquedas: `"[empresa] mantenimiento predictivo"`, `"[empresa] industria 4.0 Colombia"`

---

## Fuentes para Investigar Competidores

### Datos de empresa
- **LinkedIn**: tamaño, crecimiento de empleados, tecnologías en perfiles de trabajo
- **Sitio web**: `/nosotros`, `/tecnología`, `/soluciones`, blog corporativo
- **Supersociedades**: revenue real para empresas colombianas (via extract_financials.py)
- **Google Maps / App Stores**: reseñas, calificación, quejas

### Señales tecnológicas (sin hablar con la empresa)
- **Ofertas de empleo**: buscar en LinkedIn Jobs / Computrabajo `"[empresa] data scientist"` o `"[empresa] IA"` — si contratan perfiles de IA, están invirtiendo
- **BuiltWith / Wappalyzer** (extensión Chrome, o wappalyzer.com): detecta stack tecnológico del sitio web
- **GitHub**: si tienen repositorios públicos, indica capacidad técnica interna
- **Crunchbase / AngelList**: inversiones, fundadores, tecnología

### Prensa y reputación
- **Google News**: `"[empresa]" Colombia [año]`
- **Portafolio / La República**: para empresas grandes con cobertura nacional
- **Reclamos.co / Trustpilot**: quejas de clientes (señales de procesos con problemas)
- **RUES** (rues.gov.co): registro mercantil, actividad económica

---

## Cómo Estimar Precio Relativo Sin Datos Públicos

Cuando el precio no es público (frecuente en B2B), usar estas señales indirectas:

| Señal | Indica precio |
|-------|--------------|
| Clientes enterprise (Bancolombia, Ecopetrol, etc.) | Premium |
| Clientes PYME o mencionan "accesible" / "para todos" | Low-cost / mid |
| No hay precios en web, "solicitar cotización" | B2B consultivo, posiblemente premium |
| Precios publicados, comparadores en web | Commodity / price-competitive |
| Certificaciones internacionales (ISO, JCI) | Premium |
| Sede en zona de negocios premium (El Poblado, Zona Rosa) | Señal de premium |
| Sin dirección clara, operación 100% digital | Posiblemente low-cost |

---

## Escala de Madurez Digital para Competidores

Usa la misma escala que company-analyst para que la Tabla Comparativa sea consistente:

| Nivel | Descripción |
|-------|-------------|
| 1 | Sin presencia digital relevante, sin sistemas integrados |
| 2 | Web básica, redes sociales esporádicas, sin autoservicio |
| 3 | Web funcional, CRM/ERP básico, algún canal digital de atención |
| 4 | App o portal de autoservicio, datos centralizados, presencia digital activa |
| 5 | IA como core del negocio, omnicanalidad, decisiones basadas en datos |

---

## Patrones de Puntos Ciegos Comunes

Los prospectos frecuentemente no reconocen competidores de estas categorías:

1. **Plataformas digitales que desintermedian**: apps, marketplaces que conectan oferta y demanda sin pasar por operadores tradicionales
2. **Empresas de otro sector que se expanden al suyo** (ej: bancos ofreciendo seguros, logísticas ofreciendo pagos)
3. **Modelos de bajo costo** (hard discount, freemium) que atraen al segmento de menor valor del prospecto
4. **Consultoras generalistas** que hacen proyectos de IA sin ser especialistas en el sector
5. **Freelancers o equipos pequeños** que cobran mucho menos para el mismo servicio
6. **Competidores regionales** de otras ciudades que están expandiéndose

---

## Anti-Hallucination Checklist para Competidores

Antes de escribir cada ficha, verificar:
- [ ] ¿La empresa realmente opera en Colombia? (No solo tiene nombre en español)
- [ ] ¿El revenue citado viene de Supersociedades o de prensa fechada?
- [ ] ¿La herramienta de IA mencionada tiene fuente (press release, blog, demo, oferta de empleo)?
- [ ] ¿El número de empleados de LinkedIn es reciente (< 2 años)?
- [ ] ¿La calificación de reseñas viene de una fuente real (Google Maps URL, App Store)?
