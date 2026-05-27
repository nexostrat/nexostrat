# Nexostrat — Brand Identity Guide
*Versión 1.1 | Mayo 2026*

> **Nota de sincronización:** Este archivo es una copia del `brand-identity.md` autoritativo en `nexostrat-editorial-designer`. Al actualizar la identidad de marca, sincronizar ambas copias. Fuente de verdad: `nexostrat-editorial-designer/references/brand-identity.md`. Diferencias de esta copia: (1) paths de logos relativos a este skill; (2) tipografía unificada a Inter en slides (override 2026-05-27 — alinea con `skills/shared/brand.py`; el original mandaba Century Gothic en slides + Inter en docs).

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
| Sky Blue | `#0EA5E9` | `sky` | Acento Interactivo | Links, iconos, CTAs secundarios, líneas decorativas, etiquetas de sección |
| Emerald | `#10B981` | `emerald` | Validación / Éxito | Checkmarks, badges de beneficio, indicadores positivos |

### Colores Secundarios

| Nombre | HEX | Código var | Rol | Uso |
|--------|-----|------------|-----|-----|
| Amber Gold | `#F59E0B` | `amber` | ⚠ CTA Exclusivo | **SOLO**: números estadísticos prominentes y botones CTA primarios |
| Arctic White | `#F0FBFF` | `arctic` | Fondo Claro Principal | Fondo de slides de contenido, callout boxes |
| Gray Light | `#F5F5F5` | `grayLight` | Fondo Alterno | Filas alternas en tablas, cards secundarias |
| Gray Mid | `#D1D5DB` | `grayMid` | Bordes / Separadores | Bordes de tabla, reglas horizontales sutiles |
| Gray Text | `#6B7280` | `grayText` | Texto Secundario | Subtítulos, fechas, notas — **solo sobre fondos claros** |
| Slate Light | `#A5B4C1` | `slateLight` | Texto sobre oscuros | Texto secundario sobre Midnight/Ocean — NUNCA usar grayText sobre oscuros |
| Dark Text | `#1F2937` | `darkText` | Cuerpo de Texto | Párrafos, contenido principal |
| White | `#FFFFFF` | `white` | Fondo Base | Slides de contenido |

---

## Proporciones de Color en Presentaciones

- **70%** Arctic White — fondos de slides de contenido
- **20%** Midnight Blue — fondos de portada y slides oscuros
- **7%** Sky Blue — acentos, iconos, líneas
- **3%** Amber Gold — números de stats, CTAs (máx. 3 instancias por deck)

---

## ⚠ Regla Amber Gold — CRÍTICO

El Amber Gold (`#F59E0B`) es el color de mayor impacto visual de la paleta. Su poder depende de su escasez. Úsalo exclusivamente en:
1. Números estadísticos prominentes (ej. "83%", "16%")
2. Botones CTA primarios

**NUNCA** como fondo de sección, texto corrido, iconos decorativos, encabezados, o cualquier otro uso.

---

## Combinaciones PROHIBIDAS

| Combinación | Razón |
|-------------|-------|
| Amber Gold como fondo de sección o encabezado | Satura visualmente — destruye el efecto de acento estratégico |
| Midnight Blue texto sobre Ocean Deep fondo | Contraste insuficiente — incumple WCAG AA |
| Emerald + Amber Gold juntos en el mismo elemento | Choque visual — dos acentos compiten entre sí |
| Más de 3 colores de la paleta en una composición | Fragmenta la identidad visual |
| `#6B7280` sobre fondos oscuros | Contraste ~2.5:1 — usar `#A5B4C1` en su lugar |
| Gradientes entre colores de la paleta | Apariencia inconsistente con el posicionamiento |

---

## Sistema de Logos — Sistema Finalizado (Mayo 2026)

El logo de Nexostrat es un **lockup horizontal**: "nexo" sin recuadro + "strat" dentro de un recuadro rectangular de esquinas redondeadas. Los archivos PNG están en `assets/logos/` de este skill. **No usar texto tipográfico como logo — usar siempre el PNG correcto.**

### Regla de Selección — Lockup Horizontal

| Fondo del slide | Archivo | Cuándo |
|-----------------|---------|--------|
| Arctic White (`#F0FBFF`) | `Nexostrat_Logo_Fondo_Arctic_Transparente.png` | **DEFAULT para fondos claros** |
| Blanco puro (`#FFFFFF`) | `Nexostrat_Logo_Fondo_Blanco_Transparente.png` | Slides sobre blanco puro |
| Midnight Blue (`#0C1A2E`) | `Nexostrat_Logo_Fondo_Midnight_Transparente.png` | Portada, KPIs, cierre (fondos oscuros) |
| Sky Blue (`#0EA5E9`) | `Nexostrat_Logo_Fondo_SkyBlue_Transparente.png` | Elementos sobre fondo Sky Blue |
| Mono claro | `Nexostrat_Logo_Monocromatico_Oscuro_Transparente.png` | Impresión B/N |
| Mono oscuro | `Nexostrat_Logo_Monocromatico_Claro_Transparente.png` | Impresión B/N fondo oscuro |

### Regla de Selección — Ícono (cuando el espacio no permite el lockup 4.5:1)

| Fondo | Archivo |
|-------|---------|
| Midnight Blue | `Nexostrat_Icono_Midnight_Transparente.png` |
| Ocean Deep | `Nexostrat_Icono_Ocean_Deep.png` |
| Sky Blue | `Nexostrat_Icono_SkyBlue.png` |
| Claro (mono) | `Nexostrat_Icono_Monocromatico_Oscuro_Transparente.png` |
| Oscuro (mono) | `Nexostrat_Icono_Monocromatico_Claro_Transparente.png` |

### Contextos de Uso en Presentaciones

| Contexto | Logo | Tamaño PptxGenJS |
|----------|------|------------------|
| Portada (fondo Midnight) | `Fondo_Midnight_Transparente` | `w: 1.49, h: 0.33` |
| Header slides de contenido (fondo claro) | `Fondo_Arctic_Transparente` | `w: 1.49, h: 0.33` |
| Slides KPIs/Cierre (fondo Midnight) | `Fondo_Midnight_Transparente` | `w: 1.49, h: 0.33` |
| Espacio muy reducido | Ícono correspondiente | `w: 0.33, h: 0.33` |
| Footer | Solo texto "nexostrat.com" 8pt — **no usar logo PNG** | — |

### Dimensiones PNG

| Tipo | Dimensiones (px) | Ratio | Fórmula de altura |
|------|-----------------|-------|-------------------|
| Lockup horizontal | 2350 × 520 | 4.52 : 1 | `ancho × (520/2350) = ancho × 0.2213` |
| Ícono | 512 × 512 | 1 : 1 | `igual al ancho` |

---

## Tagline Oficial

**"Crece sin contratar. Escala sin complicarte."**

Tagline aprobado de la marca (Mayo 2026).

### Reglas de uso en presentaciones

| Tipo de presentación | ¿Incluir? | Dónde |
|---------------------|-----------|-------|
| Propuesta comercial | ✓ Sí | Portada + slide de cierre |
| Diagnóstico para cliente | ✓ Sí | Portada |
| Hoja de Ruta para cliente | ✓ Sí | Portada + slide de cierre |
| Pitch / deck de ventas | ✓ Sí | Portada + slide de cierre |
| Reporte de resultados a cliente activo | ✓ Sí | Portada |
| Presentación interna / operativa | ✗ No | — |
| Capacitación interna | ✗ No | — |

**Regla general:** deck para cliente externo o deck de ventas → tagline en portada y cierre. Deck interno → sin tagline.

---

## Sistema Tipográfico — Presentaciones

**Fuente única: Inter** en todos los elementos. Unificada con `skills/shared/brand.py` (`BRAND_FONT = "Inter"`); no usar Century Gothic, Calibri ni Arial en slides.

| Elemento | Tamaño | Peso | Color |
|----------|--------|------|-------|
| Título de portada | 44pt | Bold | Arctic White |
| Título de sección (H1) | 26–28pt | Bold | Midnight Blue o Arctic White |
| Subsección (H2) | 18–22pt | Bold | Midnight Blue |
| Cuerpo de texto | 13–16pt | Regular | Dark Text (claro) / Arctic White (oscuro) |
| KPI / dato de impacto | 52–80pt | Bold | Amber Gold |
| Etiqueta / caption | 8–11pt | Regular | grayText (claro) / slateLight (oscuro) |
| Tagline | 13pt | Italic | Slate Light (`#A5B4C1`) |

---

## Voz y Tono

### Personalidad de Marca

| Atributo | Qué significa | Cómo se manifiesta |
|----------|---------------|-------------------|
| Experto | Conocemos profundamente la IA y su aplicación a PYMEs colombianas | Datos verificados, cifras concretas, proceso documentado |
| Honesto | Decimos lo que encontramos, aunque no sea lo que el cliente quiere escuchar | Garantía de diagnóstico, sin presión de cierre |
| Transparente | El cliente siempre sabe qué esperar | Precios publicados, metodología documentada |
| Profesional | Rigor metodológico en todo contacto | Documentos bien formateados, comunicación puntual |
| Innovador | Adoptamos primero las herramientas que recomendamos | Herramientas actuales, casos de uso reales |

### Correcto vs. Incorrecto

| ✓ Voz Correcta | ✗ Voz Incorrecta |
|----------------|-----------------|
| "El 83% de las empresas que adoptan IA reportan incremento en ingresos." | "¡La IA va a TRANSFORMAR tu empresa! 🚀" |
| "Si no identificamos una oportunidad concreta, no continuamos." | "Somos los #1 en IA para PYMEs." |
| "No vendemos plantillas. Cada solución se diseña sobre tu operación." | "Tenemos soluciones para todos los presupuestos." |

### Principios de Comunicación

1. Lenguaje de negocio, no jerga técnica
2. Resultados concretos y verificables — nunca promesas abstractas
3. Sin superlativos vacíos, sin emojis (excepto en redes con justificación)
4. Lenguaje: español colombiano. Nunca mencionar México como contexto de referencia.

---

## Audiencia Objetivo

| Dimensión | Descripción |
|-----------|-------------|
| Cargo | Dueño, CEO, Gerente General o Director de Operaciones |
| Tamaño empresa | 5 a 200 empleados — PYMEs en crecimiento o formalización |
| Sector | Servicios, comercio, manufactura ligera, salud, educación, agencias |
| Geografía | Colombia (Bogotá, Medellín, Cali, Barranquilla) — operamos remoto |
| Dolor principal | Tiempo del equipo en tareas repetitivas, decisiones sin datos en tiempo real |
| Motivación clave | Crecer sin contratar más personal. No quedarse atrás en adopción tecnológica. |
| Objeción frecuente | "Eso es para empresas grandes." "Es muy costoso." "No tenemos tiempo." |

---

## Información de Contacto

- **Web:** nexostrat.com
- **Email:** contacto@nexostrat.com
- **Precio Hoja de Ruta:** desde COP $900.000
- **Diagnóstico:** gratuito, sin compromiso
- **Garantía:** si no se identifica una oportunidad concreta, no se continúa
- **Fuentes de estadísticas:** Microsoft LatAm 2024, SAP 2025, IT Reseller 2024

---

## Checklist de Consistencia — Presentaciones

- [ ] Colores pertenecen exclusivamente a la paleta Aurora
- [ ] Amber Gold SOLO en estadísticas o CTA (máx. 3 instancias por deck)
- [ ] No más de 3 colores por composición de slide
- [ ] Tipografía es Inter — no Century Gothic, no Calibri, no Arial
- [ ] Logo es PNG correcto para el fondo del slide — no texto tipográfico
- [ ] Texto sobre fondos oscuros usa Arctic White o `#A5B4C1` — nunca `#6B7280`
- [ ] Tagline en portada y cierre si el deck es para cliente externo
- [ ] Tono directo, específico y basado en datos — sin superlativos vacíos
- [ ] Estadísticas tienen fuente citada
- [ ] No hay menciones a México — solo Colombia
