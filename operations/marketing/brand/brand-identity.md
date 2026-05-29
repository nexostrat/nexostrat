# Nexostrat — Brand Identity Guide (Canónico)
*Versión 2.0 | Mayo 2026*

> **Fuente única de marca (machine-readable).** Este archivo es la **única** fuente autoritativa de identidad de marca que leen los tres expertos de formato (`00_nexostrat_docx`, `00_nexostrat_pptx`, `00_nexostrat_html`) y el Skill 6 (client-deliverables). Consolida y supersede las dos copias previas que vivían en `skills/pptx_expert/references/brand-identity.md` y `skills/nexostrat_editorial_designer/references/brand-identity.md` (esos skills se retiran en la Fase 3 del Plan Maestro).
>
> **Assets canónicos asociados** (referenciar, nunca copiar dentro de cada skill):
> - **Logos:** `operations/marketing/brand/logos/` (18 PNG — única copia tras dedup).
> - **Guía visual (.docx):** `operations/assets/brand/Nexostrat_Brand_Guide.docx` (v1.0).
> - **Buyer persona:** `operations/marketing/buyer_personas/Nexostrat_BuyerPersona_DonCarlos_Ricardo_2026-05-27.md`.
> - **Constantes de render docx:** `skills/shared/brand.py` (paleta + helpers; apunta a `operations/marketing/brand/logos/`).
>
> **Cambios v2.0 vs v1.x:** (1) **Inter en todos los canales** — reemplaza Century Gothic en documentos (decisión D3, 2026-05-29: Century Gothic no está en Linux y rompía la paridad). (2) Geografía **LatAm** (México primario / Colombia secundario), elimina la regla "nunca mencionar México". (3) Pricing retirado del brand (lo posee Skill 6). (4) Persona Don Carlos como audiencia objetivo. (5) Incorpora `Slate Light #A5B4C1` y la regla de contraste sobre fondos oscuros.

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
| Arctic White | `#F0FBFF` | `arctic` | Fondo Claro Principal | Fondo de documentos, slides de contenido, callout boxes, secciones claras |
| Gray Light | `#F5F5F5` | `grayLight` | Fondo Alterno | Filas alternas en tablas, cards secundarias |
| Gray Mid | `#D1D5DB` | `grayMid` | Bordes / Separadores | Bordes de tabla, reglas horizontales sutiles |
| Gray Text | `#6B7280` | `grayText` | Texto Secundario | Subtítulos, fechas, notas al pie, footer — **solo sobre fondos claros** |
| Slate Light | `#A5B4C1` | `slateLight` | Texto sobre oscuros | Texto secundario sobre Midnight/Ocean — **NUNCA usar `grayText` sobre oscuros** |
| Dark Text | `#1F2937` | `darkText` | Cuerpo de Texto | Párrafos, descripciones, contenido principal |
| White | `#FFFFFF` | `white` | Fondo Base | Páginas / slides de contenido |

> Los valores HEX coinciden 1:1 con las constantes en `skills/shared/brand.py` (`HEX_*` y `RGBColor`). Cualquier cambio de paleta debe actualizarse en ambos lugares.

---

## Proporciones de Color por Canal

### Documentos (.docx / .pdf) — `00_nexostrat_docx`
- **70%** Arctic White (`#F0FBFF`) + espacios en blanco
- **20%** Midnight Blue (`#0C1A2E`) — headers, bordes principales
- **7%** Sky Blue (`#0EA5E9`) — líneas, etiquetas de sección, bordes de callout
- **3%** Amber Gold (`#F59E0B`) — datos de impacto únicamente

### Presentaciones (.pptx) — `00_nexostrat_pptx`
- **70%** Arctic White — fondos de diapositivas de contenido
- **20%** Midnight Blue — fondos de portada y diapositivas de cifras
- **7%** Sky Blue — acentos, iconos, líneas
- **3%** Amber Gold — números de stats, CTAs (máx. 3 instancias por deck)

### Web / Digital — `00_nexostrat_html`
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
| `#6B7280` (Gray Text) sobre fondos oscuros | Contraste ~2.5:1 — usar `#A5B4C1` (Slate Light) en su lugar |
| Gradientes entre colores de la paleta | Apariencia inconsistente con el posicionamiento |
| Sky Blue como fondo de texto extenso | Fatiga visual — no cumple contraste para cuerpo de texto |
| Arctic White sobre blanco puro (`#FFFFFF`) | Contraste insuficiente — el borde desaparece |
| Amber Gold en texto corrido o párrafos | Reservado exclusivamente para números clave y botones CTA |

---

## Sistema de Logos — Sistema Finalizado (Mayo 2026)

El logo de Nexostrat es un **lockup horizontal** compuesto por "nexo" sin recuadro + "strat" dentro de un recuadro rectangular de esquinas redondeadas. El recuadro es el elemento identitario — crea el bloque visual de "estrategia" dentro del nombre.

**Ubicación canónica de los PNG:** `operations/marketing/brand/logos/` (resuelta desde la raíz del repo). **No usar texto tipográfico como logo — usar siempre el PNG correcto.** Los skills resuelven la ruta desde la raíz del repo; no se copian los PNG dentro de cada skill.

### Regla de Selección — Lockup Horizontal

| Fondo | Archivo | Cuándo |
|-------|---------|--------|
| Arctic White (`#F0FBFF`) | `Nexostrat_Logo_Fondo_Arctic_Transparente.png` | **DEFAULT para fondos claros** — headers, páginas/slides interiores, portadas de reporte |
| Blanco puro (`#FFFFFF`) | `Nexostrat_Logo_Fondo_Blanco_Transparente.png` | Sobre fondo blanco puro |
| Midnight Blue (`#0C1A2E`) | `Nexostrat_Logo_Fondo_Midnight_Transparente.png` | Portadas oscuras, bandas de header Midnight, slides KPI/cierre |
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

### Contextos de Uso

| Contexto | Logo recomendado | Tamaño |
|----------|-----------------|--------|
| Portada documento (fondo Midnight) | `Fondo_Midnight_Transparente` | 3.2 – 3.5 in |
| Header página interior (fondo Arctic/blanco) | `Fondo_Arctic_Transparente` (**default**) | 1.5 in |
| Portada/KPI/cierre pptx (fondo Midnight) | `Fondo_Midnight_Transparente` | `w: 1.49, h: 0.33` |
| Header slide de contenido (fondo claro) | `Fondo_Arctic_Transparente` | `w: 1.49, h: 0.33` |
| Espacio muy reducido | Ícono correspondiente | 0.5 in / `w: 0.33, h: 0.33` |
| Footer | Solo texto "nexostrat.com" — **no usar logo PNG en footer** | — |

### Dimensiones PNG

| Tipo | Dimensiones (px) | Ratio | Fórmula de altura |
|------|-----------------|-------|-------------------|
| Lockup horizontal | 2350 × 520 | 4.52 : 1 | `ancho × (520/2350) = ancho × 0.2213` |
| Ícono | 512 × 512 | 1 : 1 (cuadrado) | `ancho × 1.0` |

### Zona de Protección

El logo debe tener un espacio de protección equivalente a la altura de la letra "n" del lockup. Ningún elemento ajeno debe entrar en esa zona.

---

## Sistema Tipográfico — Inter (todos los canales)

**Fuente única: Inter** en documentos, presentaciones y web. **JetBrains Mono** para fragmentos monoespaciados (código, datos tabulares técnicos). Decisión D3 (2026-05-29): Inter reemplaza Century Gothic en documentos — Century Gothic no está disponible en Linux y rompía la paridad de render. Unificado con `skills/shared/brand.py` (`BRAND_FONT = "Inter"`, `BRAND_FONT_MONO = "JetBrains Mono"`). **No usar Century Gothic, Calibri ni Arial en ningún canal.**

### Documentos (.docx / .pdf)

| Nivel | Tamaño | Peso | Color | Uso |
|-------|--------|------|-------|-----|
| Título de portada / H1 | 28–36pt | Bold | Midnight Blue o Arctic White | Portada, título de sección principal |
| H2 | 18–22pt | Bold | Midnight Blue | Subsecciones, encabezados de tabla |
| H3 | 13–15pt | Bold | Ocean Deep (`#0D4A6B`) | Títulos de bloque, categorías |
| Cuerpo | 11–12pt | Regular | Dark Text (`#1F2937`) | Párrafos, descripciones |
| Caption | 9–10pt | Regular | Gray Text (`#6B7280`) | Notas al pie, fuentes, meta-datos |
| Stat / Dato Clave | 36–52pt | Bold | Amber Gold (`#F59E0B`) | Números de impacto — uso excepcional |

### Presentaciones (.pptx)

| Nivel | Tamaño | Peso | Color |
|-------|--------|------|-------|
| Título de portada | 44pt | Bold | Arctic White |
| Título de sección (H1) | 26–28pt | Bold | Midnight Blue o Arctic White |
| Subsección (H2) | 18–22pt | Bold | Midnight Blue |
| Cuerpo | 13–16pt | Regular | Dark Text (claro) / Arctic White (oscuro) |
| KPI / dato de impacto | 52–80pt | Bold | Amber Gold |
| Etiqueta / caption | 8–11pt | Regular | Gray Text (claro) / Slate Light (oscuro) |
| Tagline | 13pt | Italic | Slate Light (`#A5B4C1`) |

### Web / Digital

| Nivel | Tamaño | Peso | Color |
|-------|--------|------|-------|
| Display / H1 | 40–56px | Bold | White / Midnight |
| H2 | 28–36px | SemiBold | Midnight Blue |
| H3 | 20–24px | SemiBold | Ocean Deep |
| Cuerpo | 15–17px | Regular | Dark Text / Arctic |
| Label / Badge | 11–13px | Bold | Sky Blue / Emerald |
| CTA Button | 15–17px | Bold | Midnight Blue (sobre fondo Amber Gold) |

### Reglas Tipográficas

1. Inter es la única familia tipográfica de texto; JetBrains Mono solo para monoespaciado puntual. Máximo 2 familias en cualquier composición.
2. El interlineado mínimo para cuerpo de texto es 1.4× el tamaño de fuente.
3. El Amber Gold en tipografía se reserva exclusivamente para números de impacto (estadísticas, datos clave).
4. Sobre fondos oscuros, el texto secundario usa Slate Light (`#A5B4C1`) o Arctic White — nunca Gray Text (`#6B7280`).

---

## Voz y Tono

### Personalidad de Marca

| Atributo | Qué significa | Cómo se manifiesta |
|----------|---------------|-------------------|
| Experto | Conocemos la IA y su aplicación a PYMEs de LatAm | Datos verificados, cifras concretas, proceso documentado |
| Honesto | Decimos lo que encontramos, aunque no sea lo que el cliente quiere escuchar | Sin presión de cierre, lenguaje sin eufemismos, afirmaciones calibradas a lo que realmente sabemos |
| Transparente | El cliente siempre sabe qué esperar | Metodología documentada, alcance claro por etapas |
| Profesional | Rigor metodológico en todo contacto | Documentos bien formateados, comunicación puntual |
| Innovador | Adoptamos primero las herramientas que recomendamos | Herramientas actuales, casos de uso reales, propuestas concretas |

### Correcto vs. Incorrecto

| ✓ Voz Correcta | ✗ Voz Incorrecta |
|----------------|-----------------|
| "El 83% de las empresas que adoptan IA reportan incremento en ingresos." | "¡La IA va a TRANSFORMAR tu empresa y llevarla al siguiente nivel!" |
| "Esto entendemos de tu operación hoy, por lo que vimos online y conversamos." | "Estudiamos a fondo a tus competidores directos y a tu equipo." |
| "No reemplazamos a nadie: liberamos al equipo para que dedique su tiempo a lo importante." | "Esto te va a permitir reducir personal." |
| "No vendemos plantillas. Cada solución se diseña sobre tu operación." | "Tenemos soluciones para todos los presupuestos." |

### Principios de Comunicación

1. **Calibrar al conocimiento real.** Afirmar solo lo que sabemos y cómo lo supimos ("por lo que vimos online y conversamos", "esto entendemos hoy"). Nunca inventar conocimiento interno que no tenemos.
2. Lenguaje de negocio, no jerga técnica — "horas recuperadas", no "automatización RPA".
3. Resultados concretos y verificables — nunca promesas abstractas ni superlativos vacíos.
4. **No reemplazamos a nadie: liberamos al equipo.** Toda persona es valiosa; el objetivo es quitar tareas operativas repetitivas, no sustituir gente.
5. Al hablar de asistentes (WhatsApp, etc.) dejar claro que **no es una persona** — es un sistema/programa que hace el trabajo — **sin usar la palabra "robot"**.
6. **Vender el valor, no la IA.** La IA va en el contenido, no en los títulos. Si una solución usa IA, lo decimos con orgullo, pero no es la razón por la que nos contratan.
7. **Emojis: mesurados y con propósito**, nunca decorativos ni excesivos. No es "cero emojis"; es "emojis con sentido" (criterio T7, 2026-05-29). *Nota: esta regla rige los deliverables de marca; las respuestas internas de chat siguen sin emojis.*
8. Idioma: español neutro de negocios para LatAm.

---

## Tagline Oficial

**"Crece sin contratar. Escala sin complicarte."**

Tagline aprobado de la marca (Mayo 2026). Resume la propuesta de valor central: crecimiento sin necesidad de contratar personal adicional.

| Tipo de documento | ¿Incluir? | Dónde |
|------------------|-----------|-------|
| Propuesta comercial | ✓ Sí | Portada + cierre |
| Diagnóstico para cliente | ✓ Sí | Portada |
| One-pager / sell sheet | ✓ Sí | Banda de header o pie |
| Hoja de Ruta para cliente | ✓ Sí | Portada + cierre |
| Pitch / deck de ventas | ✓ Sí | Portada + cierre |
| Reporte interno / operativo | ✗ No | — |
| Carta / comunicación formal | ✗ No | — |
| Contrato o acuerdo | ✗ No | — |
| Documento de trabajo / cheat sheet | ✗ No | — |

**Regla general:** si el documento es para un cliente externo o busca persuadir, incluir el tagline. Si es interno u operativo, omitirlo.

---

## Audiencia Objetivo — Don Carlos

El buyer persona canónico es **Don Carlos**. Documento completo (90 preguntas + notas estratégicas): `operations/marketing/buyer_personas/Nexostrat_BuyerPersona_DonCarlos_Ricardo_2026-05-27.md`. **Todo mensaje de marca debe hablarle a Don Carlos.**

| Dimensión | Descripción |
|-----------|-------------|
| Cargo | Dueño / Fundador (decide pero consulta con su mano derecha) |
| Edad / perfil | 46–55 años, primera generación, construyó la empresa a pulso (20+ años) |
| Tamaño empresa | 26–100 empleados; facturación USD 1–10M |
| Sector | Logística/transporte, manufactura, servicios profesionales (transversal al patrón, no a la industria) |
| Geografía | **México primario (Tijuana cross-border)** · Colombia secundario · LatAm |
| Madurez digital | Nivel 1–2: WhatsApp como sistema operativo de hecho, Excel disperso, sin CRM, web descuidada |
| Dolor principal | Información dispersa, stack de parches que no se hablan, tiempo del líder absorbido por la operación |
| Motivación clave | Ordenar la operación, preparar su salida operativa, dejar un legado que camine sin él |
| Decide por | Confianza y relación (no comparación). Referido de un par pesa más que cualquier funnel digital. |
| Qué NO oír jamás | "Transformación digital integral", ROI a 18 meses sin entregables, "reducir personal", assessment de 6 semanas antes de valor |
| Tono que funciona | Directo, sin rodeos, cercano. El tono formal o motivacional lo cierra. |

> **Riesgo estructural (Nota 2 del persona):** "empresa demasiado nueva sin track record" es exactamente el perfil de Nexostrat hoy. Mitigación: apoyarse en el track record individual de los founders + casos tempranos verificables + honestidad como ventaja. La marca nunca debe sobre-afirmar experiencia que no tiene.

---

## Aplicaciones por Canal

### Documentos Word (.docx)

| Elemento | Especificación |
|----------|---------------|
| Fondo de página | Blanco puro (`#FFFFFF`) o Arctic White (`#F0FBFF`) |
| Header | "NEXOSTRAT" Inter Bold 11pt Midnight Blue + línea Sky Blue 0.75pt inferior |
| Footer | "nexostrat.com · Pág. X" Inter 9pt Gray Text |
| Portada | Fondo Midnight Blue, texto Arctic White, acento Sky Blue, **logo PNG** (no texto) |
| Títulos H1 | Inter Bold 28pt, Midnight Blue, sin subrayado |
| Cuerpo | Inter Regular 11–12pt, **texto justificado** |
| Callout boxes | Borde izquierdo 4pt Sky Blue + fondo Arctic White |
| Tablas | Header Midnight Blue / texto blanco. Filas alternas: blanco / Gray Light |
| Datos de impacto | Inter Bold 36pt+ Amber Gold — uso excepcional |

### Presentaciones (.pptx)

| Elemento | Especificación |
|----------|---------------|
| Portada | Fondo Midnight Blue, título Arctic White Inter Bold 44pt, logo `Fondo_Midnight_Transparente` |
| Contenido | Fondo Arctic White o blanco, texto Midnight Blue, logo `Fondo_Arctic_Transparente` |
| Cifras | Fondo Ocean Deep, número Amber Gold Inter Bold 52–80pt, label Arctic White |
| Iconos | Sky Blue o Emerald (nunca Amber, nunca más de 2 colores por slide) |
| CTA final | Fondo Ocean Deep, botón Amber Gold, texto Midnight Blue |

### Web / HTML

| Elemento | Especificación |
|----------|---------------|
| Tipografía | Inter (vía `@font-face` self-hosted o Google Fonts CDN con fallback de sistema) |
| Logos | PNG en base64 embebido (entregables self-contained) o ruta a `operations/marketing/brand/logos/` |
| Hero | Fondo Midnight, título Arctic White, acento Sky Blue |
| CTA primario | Botón Amber Gold, texto Midnight |
| Entrega | Centrado y responsive (celular + desktop). Preferir **link privado** sobre archivo `.html` suelto. |

### Redes Sociales (LinkedIn · WhatsApp Business)

| Elemento | Especificación |
|----------|---------------|
| Banner LinkedIn | Fondo Midnight Blue, tagline Arctic White, acento Sky Blue inferior |
| Posts con dato | Fondo Ocean Deep, número Amber Gold Bold, texto Arctic White |
| Tono LinkedIn | Autoridad sin arrogancia. Datos concretos. |
| WhatsApp Business | Cercano y conversacional. Respuestas directas. Nunca plantillas genéricas. |

---

## Información de Contacto y Datos de Marca

- **Web:** nexostrat.com
- **Email:** contacto@nexostrat.com
- **Líneas telefónicas (CO / MX):** se configuran por entregable; la línea MX dedicada está pendiente de provisión. No hardcodear un celular personal en plantillas de marca.
- **Pricing:** **no vive en el brand guide.** El modelo de precios (floor USD 3K · 8K · 15K + "depende del alcance") lo posee y mantiene el Skill 6 (`nexostrat-client-deliverables`). Mantener el precio en un solo lugar.
- **Diagnóstico:** según oferta vigente definida por Skill 6 / dirección.
- **Fuentes de estadísticas a citar:** Microsoft LatAm 2024, SAP 2025, IT Reseller 2024.

---

## Checklist de Consistencia de Marca

Antes de entregar cualquier material de Nexostrat:

- [ ] Los colores usados pertenecen exclusivamente a la paleta Aurora
- [ ] El Amber Gold aparece SOLO en números estadísticos o botones CTA (máx. 3 por composición/deck)
- [ ] No se usan más de 3 colores en ninguna composición
- [ ] La tipografía es **Inter** en todos los canales (JetBrains Mono solo para monoespaciado) — nunca Century Gothic, Calibri ni Arial
- [ ] El logo es el **PNG correcto** para el fondo — nunca texto tipográfico como logo
- [ ] Texto sobre fondos oscuros usa Arctic White o Slate Light (`#A5B4C1`) — nunca Gray Text (`#6B7280`)
- [ ] El tono es directo, específico y basado en datos — sin superlativos vacíos
- [ ] Las afirmaciones están calibradas a lo que realmente sabemos (sin inventar conocimiento interno)
- [ ] El mensaje "no reemplazamos a nadie, liberamos al equipo" está presente donde aplica
- [ ] No se usa la palabra "robot" al describir asistentes/sistemas
- [ ] "IA" no aparece en títulos como gancho — el valor va primero
- [ ] Las estadísticas tienen fuente citada
- [ ] El mensaje le habla a Don Carlos (ver buyer persona)
- [ ] El tagline aparece solo en material externo/persuasivo
</content>
</invoke>
