# Nexostrat — Brand Identity Guide
*Versión 1.0 | Mayo 2026*

> "Democratizar la inteligencia empresarial. Las herramientas de IA que usan las corporaciones ya existen para las PYMEs — lo que falta es el proceso correcto para implementarlas bien."

---

## Filosofía de Marca

Rigor sin frialdad. Tecnología con accesibilidad. Estrategia sin abstracción. Nexostrat nació de una convicción simple: una PYME bien asesorada puede competir con la inteligencia operativa de una corporación. La brecha no es de tecnología — es de acceso, proceso y acompañamiento.

La identidad visual refleja esa misión: sofisticación que no intimida, profesionalismo que genera confianza, claridad que no simplifica demasiado.

---

## Paleta de Colores — Paleta Aurora

### Colores Primarios

| Nombre | HEX | Código var | Rol | Uso |
|--------|-----|------------|-----|-----|
| Midnight Blue | `#0C1A2E` | `midnight` | Base Primaria | Fondos de portada, headers principales, texto de alto contraste |
| Ocean Deep | `#0D4A6B` | `ocean` | Estructural | Fondos secundarios, subtítulos, bordes de secciones, iconos, H3 |
| Sky Blue | `#0EA5E9` | `sky` | Acento Interactivo | Links, iconos, CTAs secundarios, líneas decorativas, etiquetas de sección, bordes de callout |
| Emerald | `#10B981` | `emerald` | Validación / Éxito | Checkmarks, badges de beneficio, indicadores positivos |

### Colores Secundarios

| Nombre | HEX | Código var | Rol | Uso |
|--------|-----|------------|-----|-----|
| Amber Gold | `#F59E0B` | `amber` | ⚠ CTA Exclusivo | **SOLO**: números estadísticos prominentes y botones CTA primarios. Nunca en texto corrido, fondos de sección, iconos decorativos ni encabezados. |
| Arctic White | `#F0FBFF` | `arctic` | Fondo Claro Principal | Fondo de documentos, propuestas, callout boxes, secciones claras |
| Gray Light | `#F5F5F5` | `grayLight` | Fondo Alterno | Filas alternas en tablas, cards secundarias |
| Gray Mid | `#D1D5DB` | `grayMid` | Bordes / Separadores | Bordes de tabla, reglas horizontales sutiles |
| Gray Text | `#6B7280` | `grayText` | Texto Secundario | Subtítulos, fechas, notas al pie, footer, texto de apoyo |
| Dark Text | `#1F2937` | `darkText` | Cuerpo de Texto | Párrafos, descripciones, contenido principal |
| White | `#FFFFFF` | `white` | Fondo Base | Páginas de contenido |

---

## Proporciones de Color por Canal

### Documentos (.docx / .pdf)
- **70%** Arctic White (`#F0FBFF`) + espacios en blanco
- **20%** Midnight Blue (`#0C1A2E`) — headers, bordes principales
- **7%** Sky Blue (`#0EA5E9`) — líneas, etiquetas de sección, bordes de callout
- **3%** Amber Gold (`#F59E0B`) — datos de impacto únicamente

### Presentaciones (.pptx)
- **70%** Arctic White — fondos de diapositivas de contenido
- **20%** Midnight Blue — fondos de portada y diapositivas de cifras
- **7%** Sky Blue — acentos, iconos
- **3%** Amber Gold — números de stats, CTAs

### Web / Digital
- **55%** Midnight Blue + Arctic White (alternados)
- **30%** Ocean Deep + Dark Text (tipografía y fondos secundarios)
- **12%** Sky Blue (CTAs secundarios, links)
- **3%** Amber Gold (botones CTA primarios)

---

## ⚠ Regla Amber Gold — CRÍTICO

El Amber Gold (`#F59E0B`) es el color de mayor impacto visual de la paleta. Su poder depende de su escasez. Úsalo exclusivamente en:
1. Números estadísticos prominentes (ej. "83%", "16%")
2. Botones CTA primarios

**NUNCA** como fondo de sección, texto corrido, iconos decorativos, encabezados, o cualquier otro uso que no sea los dos listados arriba.

---

## Combinaciones PROHIBIDAS

| Combinación | Razón |
|-------------|-------|
| Amber Gold como fondo de sección o encabezado | Satura visualmente — destruye el efecto de acento estratégico |
| Midnight Blue texto sobre Ocean Deep fondo | Contraste insuficiente — incumple WCAG AA |
| Emerald + Amber Gold juntos en el mismo elemento | Choque visual — dos acentos compiten entre sí |
| Más de 3 colores de la paleta en una composición | Fragmenta la identidad visual |
| Gradientes entre colores de la paleta | Apariencia inconsistente con el posicionamiento |
| Sky Blue como fondo de texto extenso | Fatiga visual — no cumple contraste para cuerpo de texto |
| Arctic White sobre blanco puro (#FFFFFF) | Contraste insuficiente — el borde desaparece |
| Amber Gold en texto corrido o párrafos | Reservado exclusivamente para números clave y botones CTA |

---

## Sistema de Logos — Sistema Finalizado (Mayo 2026)

El logo de Nexostrat es un **lockup horizontal** compuesto por "nexo" sin recuadro + "strat" dentro de un recuadro rectangular de esquinas redondeadas. El recuadro es el elemento identitario — crea el bloque visual de "estrategia" dentro del nombre.

Los archivos PNG están bundleados en `assets/logos/` del skill. **No usar texto tipográfico como logo — usar siempre el PNG correcto.**

### Regla de Selección — Lockup Horizontal

| Fondo del documento | Archivo | Cuándo |
|---------------------|---------|--------|
| Arctic White (`#F0FBFF`) | `Nexostrat_Logo_Fondo_Arctic_Transparente.png` | **DEFAULT para fondos claros** — headers, páginas interiores, portadas de reporte |
| Blanco puro (`#FFFFFF`) | `Nexostrat_Logo_Fondo_Blanco_Transparente.png` | Páginas sobre fondo blanco puro |
| Midnight Blue (`#0C1A2E`) | `Nexostrat_Logo_Fondo_Midnight_Transparente.png` | Portadas oscuras, bandas de header Midnight |
| Sky Blue (`#0EA5E9`) | `Nexostrat_Logo_Fondo_SkyBlue_Transparente.png` | Elementos sobre fondo Sky Blue |
| Mono sobre fondo claro | `Nexostrat_Logo_Monocromatico_Oscuro_Transparente.png` | Impresión B/N, documentos sin color |
| Mono sobre fondo oscuro | `Nexostrat_Logo_Monocromatico_Claro_Transparente.png` | Impresión B/N con fondo oscuro |

Preferir siempre la versión `_Transparente` — se adapta al color del fondo. Las versiones sin `_Transparente` (fondo sólido incorporado) son respaldo cuando el transparente genera artifacts.

### Regla de Selección — Ícono (NX-Icon)

Usar el ícono cuando el espacio no permite el lockup horizontal (ratio 4.5:1 del lockup).

| Fondo | Archivo |
|-------|---------|
| Midnight Blue | `Nexostrat_Icono_Midnight_Transparente.png` |
| Ocean Deep | `Nexostrat_Icono_Ocean_Deep.png` |
| Sky Blue | `Nexostrat_Icono_SkyBlue.png` |
| Fondo claro (mono) | `Nexostrat_Icono_Monocromatico_Oscuro_Transparente.png` |
| Fondo oscuro (mono) | `Nexostrat_Icono_Monocromatico_Claro_Transparente.png` |

### Contextos de Uso en Documentos

| Contexto | Logo recomendado | Ancho sugerido |
|----------|-----------------|----------------|
| Portada (fondo Midnight) | `Fondo_Midnight_Transparente` | 3.2 – 3.5 pulgadas |
| Header página interior (fondo Arctic/blanco) | `Fondo_Arctic_Transparente` (**default**) | 1.5 pulgadas |
| Header con espacio reducido | Ícono correspondiente | 0.5 pulgadas |
| Banda de header one-pager (fondo Midnight) | `Fondo_Midnight_Transparente` | 1.5 pulgadas |
| Footer | Solo texto "nexostrat.com" en 9pt Gray 500 — no usar logo PNG en footer |

### Dimensiones PNG

| Tipo | Dimensiones (px) | Ratio | Fórmula de altura |
|------|-----------------|-------|-------------------|
| Lockup horizontal | 2350 × 520 | 4.52 : 1 | `ancho × 0.2213` |
| Ícono | 512 × 512 | 1 : 1 (cuadrado) | `ancho × 1.0` |

### Zona de Protección

El logo debe tener un espacio de protección equivalente a la altura de la letra "n" del lockup. Ningún elemento ajeno debe entrar en esa zona.

---

## Sistema Tipográfico

### Canal: Documentos (.docx / .pdf)
*Propuestas · Diagnóstico · Hoja de Ruta · Informes · Contratos*

| Nivel | Fuente | Tamaño | Color | Uso |
|-------|--------|--------|-------|-----|
| Título de portada / H1 | Century Gothic Bold | 28–36pt | Midnight Blue o Arctic White | Portada, título de sección principal |
| H2 | Century Gothic Bold | 18–22pt | Midnight Blue | Subsecciones, encabezados de tabla |
| H3 | Century Gothic Bold | 13–15pt | Ocean Deep (`#0D4A6B`) | Títulos de bloque, categorías |
| Cuerpo | Century Gothic Regular | 11–12pt | Dark Text (`#1F2937`) | Párrafos, descripciones |
| Caption | Century Gothic Regular | 9–10pt | Gray 500 (`#6B7280`) | Notas al pie, fuentes, meta-datos |
| Stat / Dato Clave | Century Gothic Bold | 36–52pt | Amber Gold (`#F59E0B`) | Números de impacto — uso excepcional únicamente |

### Canal: Digital (Web / Email / Redes)

| Nivel | Fuente | Tamaño | Color | Uso |
|-------|--------|--------|-------|-----|
| Display / H1 | Inter Bold | 40–56px | White / Midnight | Hero, portadas de sección web |
| H2 | Inter SemiBold | 28–36px | Midnight Blue | Subtítulos de sección |
| H3 | Inter SemiBold | 20–24px | Ocean Deep | Encabezados de componente |
| Cuerpo | Inter Regular | 15–17px | Dark Text / Arctic | Párrafos, listas |
| Label / Badge | Inter Bold | 11–13px | Sky Blue / Emerald | Etiquetas, indicadores |
| CTA Button | Inter Bold | 15–17px | Midnight Blue | Texto de botón (fondo Amber Gold) |

### Reglas Tipográficas

1. Máximo 2 familias tipográficas en cualquier composición.
2. Nunca mezclar Century Gothic e Inter en el mismo canal o documento.
3. El interlineado mínimo para cuerpo de texto es 1.4× el tamaño de fuente.
4. El Amber Gold en tipografía se reserva exclusivamente para números de impacto (estadísticas, precios en contexto de valor).

---

## Voz y Tono

### Personalidad de Marca

| Atributo | Qué significa | Cómo se manifiesta |
|----------|---------------|-------------------|
| Experto | Conocemos profundamente la IA y su aplicación a PYMEs colombianas | Datos verificados, cifras concretas, proceso documentado |
| Honesto | Decimos lo que encontramos, aunque no sea lo que el cliente quiere escuchar | Garantía de diagnóstico, sin presión de cierre, lenguaje sin eufemismos |
| Transparente | El cliente siempre sabe qué esperar | Precios publicados, metodología documentada, diagnóstico sin costo |
| Profesional | Rigor metodológico en todo contacto | Documentos bien formateados, comunicación puntual |
| Innovador | Adoptamos primero las herramientas que recomendamos | Herramientas actuales, casos de uso reales, propuestas concretas |

### Correcto vs. Incorrecto

| ✓ Voz Correcta | ✗ Voz Incorrecta |
|----------------|-----------------|
| "El 83% de las empresas que adoptan IA reportan incremento en ingresos." | "¡La IA va a TRANSFORMAR tu empresa y llevarla al siguiente nivel! 🚀" |
| "Si al terminar el diagnóstico no identificamos una oportunidad concreta, no continuamos." | "Somos los #1 en IA para PYMEs. Los mejores del mercado." |
| "No vendemos plantillas. Cada solución se diseña sobre tu operación." | "Tenemos soluciones para todos los tipos de empresas y presupuestos." |

### Principios de Comunicación

1. Lenguaje de negocio, no jerga técnica — "horas recuperadas", no "automatización RPA"
2. Resultados concretos y verificables — nunca promesas abstractas
3. Reconocer las limitaciones reales de recursos del cliente (tiempo, presupuesto, equipo pequeño)
4. El diagnóstico gratuito como reductor de riesgo
5. Sin superlativos vacíos, sin emojis (excepto con justificación específica en redes)
6. Lenguaje: español colombiano. Nunca mencionar México como contexto de referencia.

---

## Tagline Oficial

**"Crece sin contratar. Escala sin complicarte."**

Tagline aprobado de la marca (Mayo 2026). Resume la propuesta de valor central: crecimiento sin necesidad de contratar personal adicional.

| Tipo de documento | ¿Incluir? | Dónde |
|------------------|-----------|-------|
| Propuesta comercial | ✓ Sí | Portada, debajo del subtítulo |
| Diagnóstico para cliente | ✓ Sí | Portada |
| One-pager / sell sheet | ✓ Sí | Banda de header o pie de página |
| Hoja de Ruta para cliente | ✓ Sí | Portada |
| Reporte interno / operativo | ✗ No | — |
| Carta / comunicación formal | ✗ No | — |
| Contrato o acuerdo | ✗ No | — |
| Documento de trabajo | ✗ No | — |

**Regla general:** si el documento es para un cliente externo o busca persuadir, incluir el tagline. Si es interno u operativo, omitirlo.

---

## Audiencia Objetivo

### Perfil Principal — Decisor de PYME Colombiana

| Dimensión | Descripción |
|-----------|-------------|
| Cargo | Dueño, CEO, Gerente General o Director de Operaciones |
| Tamaño empresa | 5 a 200 empleados — PYMEs en crecimiento o formalización |
| Sector | Servicios, comercio, manufactura ligera, salud, educación, agencias |
| Geografía | Colombia (Bogotá, Medellín, Cali, Barranquilla) — operamos remoto |
| Tecnología | Usa WhatsApp, Excel, Google Workspace. Curiosidad sobre IA sin claridad de implementación. |
| Dolor principal | Tiempo del equipo en tareas repetitivas, decisiones sin datos en tiempo real |
| Motivación clave | Crecer sin contratar más personal. No quedarse atrás en adopción tecnológica. |
| Objeción frecuente | "Eso es para empresas grandes." "Es muy costoso." "No tenemos tiempo." |

---

## Aplicaciones por Canal

### Documentos Word (.docx)
*Propuestas · Hoja de Ruta · Informes · Contratos*

| Elemento | Especificación |
|----------|---------------|
| Fondo de página | Blanco puro (#FFFFFF) o Arctic White (#F0FBFF) |
| Header | "NEXOSTRAT" Century Gothic Bold 11pt Midnight Blue + línea Sky Blue 1pt inferior |
| Footer | "nexostrat.com · Pág. X" Century Gothic 9pt Gray 500 |
| Portada | Fondo Midnight Blue, texto Arctic White, acento Sky Blue, logo de texto |
| Títulos H1 | Century Gothic Bold 28pt, Midnight Blue, sin subrayado |
| Callout boxes | Borde izquierdo 4pt Sky Blue + fondo Arctic White |
| Tablas | Header Midnight Blue / texto blanco. Filas alternas: blanco / Gray Light |
| Datos de impacto | Century Gothic Bold 36pt+ Amber Gold — uso excepcional únicamente |

### Presentaciones (.pptx)

| Elemento | Especificación |
|----------|---------------|
| Portada | Fondo Midnight Blue, título Arctic White Inter Bold 48pt |
| Contenido | Fondo Arctic White o blanco, texto Midnight Blue |
| Cifras | Fondo Ocean Deep, número Amber Gold Inter Bold 64pt, label Arctic White |
| Iconos | Sky Blue o Emerald (nunca Amber, nunca más de 2 colores por diapositiva) |
| CTA final | Fondo Ocean Deep, botón Amber Gold, texto Midnight Blue |

### Redes Sociales (LinkedIn · WhatsApp Business)

| Elemento | Especificación |
|----------|---------------|
| Banner LinkedIn | Fondo Midnight Blue, tagline Arctic White, acento Sky Blue inferior |
| Posts con dato | Fondo Ocean Deep, número Amber Gold Bold, texto Arctic White |
| Posts de proceso | Fondo Arctic White, iconos Sky Blue, texto Midnight Blue |
| Tono LinkedIn | Autoridad sin arrogancia. Datos concretos. Sin emojis salvo excepciones. |
| WhatsApp Business | Más cercano y conversacional. Respuestas directas. Nunca plantillas genéricas. |

---

## Información de Contacto y Datos de Marca

- **Web:** nexostrat.com
- **Email:** contacto@nexostrat.com
- **Precio Hoja de Ruta:** desde COP $900.000
- **Propuesta de diagnóstico:** gratuito, sin compromiso
- **Garantía de diagnóstico:** si no se identifica al menos una oportunidad concreta, no se continúa
- **Fuentes de estadísticas a citar:** Microsoft LatAm 2024, SAP 2025, IT Reseller 2024

---

## Checklist de Consistencia de Marca

Antes de entregar cualquier material de Nexostrat:

- [ ] Los colores usados pertenecen exclusivamente a la paleta Aurora
- [ ] El Amber Gold aparece SOLO en números estadísticos o botones CTA
- [ ] No se usan más de 3 colores en ninguna composición
- [ ] La tipografía es Century Gothic (documentos) o Inter (digital) — no mezcladas
- [ ] El tono es directo, específico y basado en datos — sin superlativos vacíos
- [ ] Las estadísticas tienen fuente citada
- [ ] No hay menciones a México — solo Colombia
- [ ] El diagnóstico gratuito está correctamente referenciado donde aplica
