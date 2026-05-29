# Nexostrat Template Reference
*Specs exactos de la plantilla base — fuente de verdad para implementación PptxGenJS*

---

## Constantes Globales

```javascript
// Paleta Aurora (sin # — requerido por PptxGenJS)
const C = {
  midnight:  "0C1A2E",   // Base primaria
  ocean:     "0D4A6B",   // Estructural
  sky:       "0EA5E9",   // Acento interactivo
  emerald:   "10B981",   // Validación / éxito
  amber:     "F59E0B",   // CTA exclusivo — SOLO números de impacto
  arctic:    "F0FBFF",   // Fondo claro principal
  white:     "FFFFFF",
  grayLight: "F5F5F5",
  grayMid:   "D1D5DB",
  grayText:  "6B7280",
  darkText:  "1F2937",
  slateLight:"A5B4C1",   // Texto secundario sobre fondos oscuros
};

// Dimensiones (LAYOUT_WIDE = 13.3" × 7.5")
const W  = 13.3;
const H  = 7.5;
const ML = 0.72;          // Margen izquierdo de contenido
const MR = 0.6;           // Margen derecho
const CW = W - ML - MR;  // Ancho de contenido ≈ 11.98"
const HDR_LINE_Y = 0.54;  // Y de la línea Sky Blue del header
const TITLE_Y    = 0.972; // Y del título de slide  (+0.222" desde HDR_LINE — breathing room corregido por JP)
const BODY_Y     = 1.672; // Y del cuerpo de contenido (+0.222" — corregido por JP)
const FTR_Y      = 7.12;  // Y del footer

// Logo PNG — lockup 2350×520 (ratio 4.519:1)
// IMPORTANTE: los logos NO se bundlean en el skill. Viven en la fuente única de marca
// operations/marketing/brand/logos (ver operations/marketing/brand/brand-identity.md).
// Resolvemos la ruta ascendiendo hasta encontrar el home de marca canónico — mismo patrón
// que pipeline/.../reunion_andrea/build_andrea.py (gold standard).
const path = require("path");
const fs   = require("fs");
function findBrandLogos(start) {
  let dir = start || process.cwd();
  for (let i = 0; i < 10; i++) {
    const cand = path.join(dir, "operations", "marketing", "brand", "logos");
    if (fs.existsSync(cand)) return cand;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error("No encuentro operations/marketing/brand/logos — corré el script desde dentro del repo Nexostrat.");
}
const LOGOS_DIR  = findBrandLogos(__dirname);
const LOGO_W     = 1.49;                      // inches — ancho estándar en slides
const LOGO_H     = LOGO_W * (520 / 2350);    // ≈ 0.33" — altura proporcional
const LOGO = {
  midnight: path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Midnight_Transparente.png"),
  arctic:   path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Arctic_Transparente.png"),
  blanco:   path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Blanco_Transparente.png"),
  skyblue:  path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_SkyBlue_Transparente.png"),
  iconMidnight: path.join(LOGOS_DIR, "Nexostrat_Icono_Midnight_Transparente.png"),
  iconOcean:    path.join(LOGOS_DIR, "Nexostrat_Icono_Ocean_Deep.png"),
};
// Tagline oficial
const TAGLINE = "Crece sin contratar. Escala sin complicarte.";

```

---

## Funciones Helper

Siempre incluir estas funciones — se reusan en múltiples slides.

```javascript
const pres = new pptxgen();
pres.layout  = "LAYOUT_WIDE";
pres.title   = "Nexostrat — [Nombre de la Presentación]";
pres.author  = "Nexostrat";

/** Header estándar — slides de fondo claro (Arctic / blanco) */
function addHeader(slide, label) {
  // Línea Sky Blue
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: HDR_LINE_Y, w: W, h: 0.03,
    fill: { color: C.sky }, line: { type: "none" },
  });
  // Logo PNG (Arctic transparent — correcto para fondos claros)
  slide.addImage({ path: LOGO.arctic, x: 0.5, y: 0.14, w: LOGO_W, h: LOGO_H });
  // Label opcional a la derecha del logo
  if (label) {
    slide.addText("  ·  " + label, {
      x: 0.5 + LOGO_W + 0.1, y: 0.14, w: 8, h: LOGO_H,
      fontSize: 10, fontFace: "Inter",
      color: C.grayText, margin: 0, valign: "middle",
    });
  }
}

/** Logo en portada o slide oscuro (Midnight bg) */
function addLogoCover(slide) {
  slide.addImage({ path: LOGO.midnight, x: 0.5, y: 0.28, w: LOGO_W, h: LOGO_H });
}

/** Logo en header de slide de contenido (Arctic/blanco bg) — alternativa explícita a addHeader */
function addLogoHeader(slide) {
  slide.addImage({ path: LOGO.arctic, x: 0.5, y: 0.14, w: LOGO_W, h: LOGO_H });
}

/** Tagline en slide de portada o cierre (fondo Midnight) */
function addTagline(slide, y) {
  slide.addText(TAGLINE, {
    x: 0.5, y: y, w: 8.3, h: 0.35,
    fontSize: 13, fontFace: "Inter", italic: true,
    color: C.slateLight, margin: 0,
  });
}

/** Footer estándar */
function addFooter(slide) {
  slide.addText("nexostrat.com", {
    x: 0.5, y: FTR_Y, w: 3, h: 0.25,
    fontSize: 8, fontFace: "Inter",
    color: C.grayText, margin: 0,
  });
}

/** Barra de acento izquierda Sky Blue (motivo de marca) */
function addLeftAccent(slide, y, h) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 0.07, h: h,
    fill: { color: C.sky }, line: { type: "none" },
  });
}

/** Título de slide estándar — Midnight Blue, 26pt Bold */
function addSlideTitle(slide, title) {
  slide.addText(title, {
    x: ML, y: TITLE_Y, w: CW, h: 0.55,
    fontSize: 26, fontFace: "Inter", bold: true,
    color: C.midnight, margin: 0,
  });
}
```

---

## Slide 1 — Portada (Cover)

**Fondo:** Midnight Blue | **Sin header/footer estándar**

```
Barra vertical izquierda: x=0, y=0, w=0.12, h=H — Sky Blue
Bloque geométrico inferior derecho: x=9.2, y=4.5, w=4.1, h=3.0 — Ocean Deep
Línea horizontal: x=0.5, y=2.35, w=6.5, h=0.05 — Sky Blue

Logo PNG (Midnight transparent): addLogoCover(slide)
  → slide.addImage({ path: LOGO.midnight, x: 0.5, y: 0.28, w: LOGO_W, h: LOGO_H })

Título principal: x=0.5, y=2.55, w=8.3, h=1.55
  fontSize=44, bold=true, color=arctic

Subtítulo: x=0.5, y=4.25, w=8.3, h=0.5
  fontSize=18, color=sky

Tagline (si deck externo): addTagline(slide, 4.88)
  → "Crece sin contratar. Escala sin complicarte." | 13pt italic | color=slateLight

Fecha/cliente: x=0.5, y=6.4, w=7, h=0.35
  fontSize=10, color=grayText

nexostrat.com: x=W-2.5, y=6.4, w=2.3, h=0.35
  fontSize=10, color=grayText, align="right"
```

---

## Slide 2 — Agenda

**Fondo:** Arctic White | **addHeader + addFooter + addLeftAccent(TITLE_Y, 5.6) + addSlideTitle**

```
Barra vertical: addLeftAccent(s, TITLE_Y, 5.6)
Título: addSlideTitle(s, "Agenda")

Por cada item (5 items), con i = índice 0-4:
  Fondo alternado: x=ML, y=BODY_Y + i*0.92, w=CW, h=0.82
    isEven → grayLight | impar → white

  Número: x=ML+0.15, y=BODY_Y + i*0.92 + 0.18, w=0.5, h=0.46
    fontSize=18, bold=true, color=sky
    Texto: String(i+1).padStart(2, "0")  // "01", "02"...

  Texto del item: x=ML+0.75, y=BODY_Y + i*0.92 + 0.2, w=CW-0.9, h=0.42
    fontSize=16, color=darkText
```

---

## Slide 3 — Divisor de Sección (Oscuro)

**Fondo:** Midnight Blue | **Sin header/footer estándar**

```
Barra izquierda: x=0, y=0, w=0.12, h=H — Sky Blue
Panel Ocean Deep: x=9.0, y=0, w=4.3, h=H — ocean, transparency=40

Etiqueta "SECCIÓN": x=0.5, y=1.811, w=4, h=0.4
  fontSize=12, bold=true, color=sky, charSpacing=5

Número grande "01": x=0.45, y=2.161, w=2.5, h=1.6
  fontSize=96, bold=true, color=sky

Línea separadora: x=0.5, y=3.65, w=5.5, h=0.04 — sky

Título de sección: x=0.5, y=3.82, w=8.5, h=0.9
  fontSize=38, bold=true, color=arctic

Descripción: x=0.5, y=4.85, w=8.5, h=0.6
  fontSize=16, color="A5B4C1"  ← NO grayText (contraste insuficiente sobre oscuro)

nexostrat.com: x=W-2.5, y=H-0.4, w=2.3, h=0.3
  fontSize=8, color=grayText, align="right"
```

---

## Slide 4 — Divisor de Sección (Acento — Ocean Deep)

**Fondo:** Ocean Deep | **Sin header/footer estándar**

```
Barra izquierda más ancha: x=0, y=0, w=0.15, h=H — Sky Blue

Etiqueta "CHECKPOINT": x=0.5, y=1.8, w=5, h=0.4
  fontSize=11, bold=true, color=sky, charSpacing=5

Título grande: x=0.5, y=2.25, w=9.5, h=1.4
  fontSize=42, bold=true, color=arctic

Línea separadora: x=0.5, y=3.78, w=5.5, h=0.04 — sky, transparency=40

3 puntos clave (i = 0, 1, 2):
  Barra vertical: x=0.5 + i*4.2, y=4.0, w=0.06, h=0.55 — arctic ← NO sky
  Texto: x=0.75 + i*4.2, y=4.0, w=3.8, h=0.55
    fontSize=15, color=arctic

nexostrat.com: x=W-2.5, y=H-0.4, w=2.3, h=0.3
  fontSize=8, color=arctic, align="right"
```

---

## Slide 5 — Contenido + Bullets

**Fondo:** White | **addHeader + addFooter + addLeftAccent(TITLE_Y, 5.58) + addSlideTitle**

```
4 bullets, con i = índice 0-3:
  Separador (si i > 0): x=ML, y=BODY_Y+i*1.22-0.1, w=CW, h=0.01 — grayMid

  Guión Sky Blue: x=ML, y=BODY_Y+i*1.22+0.16, w=0.25, h=0.06 — sky

  Título del bullet: x=ML+0.38, y=BODY_Y+i*1.22+0.05, w=CW-0.4, h=0.38
    fontSize=16, bold=true, color=midnight

  Descripción: x=ML+0.38, y=BODY_Y+i*1.22+0.45, w=CW-0.4, h=0.65
    fontSize=13, color=grayText
```

---

## Slide 6 — Dos Columnas

**Fondo:** White | **addHeader + addFooter + addSlideTitle**

```
colW = (CW - 0.4) / 2  // ≈ 5.79"

2 columnas (ci = 0, 1):
  cx = ML + ci * (colW + 0.4)

  Header de columna: x=cx, y=BODY_Y, w=colW, h=0.52 — midnight
  Barra Sky Blue en header: x=cx, y=BODY_Y, w=0.07, h=0.52 — sky
  Título columna: x=cx+0.2, y=BODY_Y+0.07, w=colW-0.25, h=0.38
    fontSize=15, bold=true, color=arctic

  4 items (ii = 0-3):
    Fondo: x=cx, y=BODY_Y+0.52+ii*1.18, w=colW, h=1.08
      ii%2==0 → col.bg | impar → white

    Guión: x=cx+0.18, y=BODY_Y+0.52+ii*1.18+0.48, w=0.2, h=0.06 — sky

    Texto: x=cx+0.50, y=BODY_Y+0.52+ii*1.18+0.14, w=colW-0.62, h=0.88
      ← x=0.50 (NO 0.18) para no solapar con el guión
      fontSize=14, color=darkText
```

---

## Slide 7 — KPIs / Estadísticas (3 números)

**Fondo:** Midnight Blue | **Sin header/footer estándar**

```
Barra izquierda: x=0, y=0, w=0.12, h=H — sky

Logo PNG (Midnight): addLogoCover(slide)
  → slide.addImage({ path: LOGO.midnight, x: 0.5, y: 0.18, w: LOGO_W, h: LOGO_H })

Título: x=0.5, y=0.65, w=10, h=0.65
  fontSize=26, bold=true, color=arctic

Línea: x=0.5, y=1.42, w=8, h=0.03 — sky, transparency=50

kpiW = CW / 3  // ≈ 3.99"

3 KPIs (i = 0, 1, 2):
  kx = ML + i * (kpiW + 0.05) - 0.2

  Separador vertical (si i > 0): x=kx-0.1, y=1.7, w=0.02, h=4.5
    sky, transparency=70

  Número Amber Gold: x=kx, y=1.7, w=kpiW, h=1.8
    fontSize=80, bold=true, color=amber

  Línea bajo número: x=kx, y=3.55, w=kpiW*0.5, h=0.05 — sky

  Label: x=kx, y=3.72, w=kpiW, h=0.48
    fontSize=17, bold=true, color=arctic

  Descripción: x=kx, y=4.28, w=kpiW-0.15, h=1.2
    fontSize=12, color="A5B4C1"  ← NO grayText

nexostrat.com: x=W-2.5, y=H-0.4, w=2.3, h=0.3
  fontSize=8, color=grayText, align="right"
```

---

## Slide 8 — Proceso en 4 Pasos

**Fondo:** White | **addHeader + addFooter + addSlideTitle**

```
stepW = CW / 4  // ≈ 2.99"
stepY = BODY_Y + 0.2  // = 1.65"

4 pasos (i = 0-3):
  sx = ML + i * (stepW + 0.15)

  Rectángulo de fondo: x=sx, y=stepY, w=stepW, h=4.6
    i%2==0 → grayLight | impar → white
    border: grayMid, 1pt

  Franja superior Sky Blue: x=sx, y=stepY, w=stepW, h=0.06 — sky

  Número: x=sx+0.2, y=stepY+0.18, w=stepW-0.3, h=0.85
    fontSize=44, bold=true, color=sky

  Título del paso: x=sx+0.2, y=stepY+1.12, w=stepW-0.3, h=0.7
    fontSize=16, bold=true, color=midnight

  Línea interna: x=sx+0.2, y=stepY+1.88, w=stepW*0.45, h=0.04 — sky

  Descripción: x=sx+0.2, y=stepY+2.05, w=stepW-0.35, h=2.3
    fontSize=13, color=grayText

  Conector (si no es el último): x=sx+stepW, y=stepY+1.2, w=0.15, h=0.06 — sky
```

---

## Slide 9 — Cita / Testimonial

**Fondo:** Ocean Deep | **Sin header/footer estándar**

```
Barra izquierda: x=0, y=0, w=0.12, h=H — sky
Barra de acento vertical: x=0.5, y=1.5, w=0.18, h=3.8 — sky

Comillas decorativas """: x=0.8, y=0.8, w=1.8, h=1.6
  fontSize=120, bold=true, color=sky

Texto de la cita: x=0.9, y=2.0, w=10.5, h=2.2
  fontSize=28, italic=true, color=arctic

Línea separadora: x=0.9, y=4.35, w=4, h=0.04 — sky

Atribución: x=0.9, y=4.5, w=8, h=0.45
  fontSize=16, bold=true, color=sky

Contexto adicional: x=0.9, y=5.05, w=8, h=0.4
  fontSize=13, color=arctic  ← NO grayText (contraste insuficiente sobre ocean)

nexostrat.com: x=W-2.5, y=H-0.4, w=2.3, h=0.3
  fontSize=8, color=arctic, align="right"
```

---

## Slide 10 — Grid 2×2 Beneficios

**Fondo:** White | **addHeader + addFooter + addSlideTitle**

```
cardW = (CW - 0.3) / 2  // ≈ 5.84"
cardH = (H - BODY_Y - 0.55) / 2  // ≈ 2.75"
gapX = 0.3, gapY = 0.28

4 cards (i = 0-3):
  col = i % 2, row = Math.floor(i / 2)
  cx = ML + col * (cardW + gapX)
  cy = BODY_Y + row * (cardH + gapY)

  Fondo: row==0 → arctic | row==1 → grayLight
    border: grayMid, 1pt

  Barra superior Sky Blue: x=cx, y=cy, w=cardW, h=0.06 — sky

  Número: x=cx+0.22, y=cy+0.18, w=0.8, h=0.55
    fontSize=28, bold=true, color=sky

  Título: x=cx+0.22, y=cy+0.78, w=cardW-0.35, h=0.45
    fontSize=16, bold=true, color=midnight

  Línea interna: x=cx+0.22, y=cy+1.28, w=cardW*0.35, h=0.04 — sky

  Descripción: x=cx+0.22, y=cy+1.42, w=cardW-0.35, h=cardH-1.58
    fontSize=13, color=grayText
```

---

## Slide 11 — Imagen + Contenido

**Fondo:** White | **addHeader + addFooter** (sin addSlideTitle — el título va en la zona de contenido)

**⚠ REGLA CRÍTICA:** El panel de imagen empieza en `y = HDR_LINE_Y + 0.04` (= 0.58"), NO en y=0. Si empieza en y=0, tapa el header.

```
imgW = 5.8
imgY = HDR_LINE_Y + 0.04  // = 0.58"

Panel de imagen: x=0, y=imgY, w=imgW, h=H-imgY
  color=midnight (placeholder para foto real)

Barra vertical Sky Blue: x=imgW, y=imgY, w=0.12, h=H-imgY — sky

Label de imagen (placeholder):
  imgMidY = imgY + (H - imgY) / 2
  "[ IMAGEN ]": x=0, y=imgMidY-0.3, w=imgW, h=0.6
    fontSize=18, bold=true, color=grayText, align="center"
  Instrucción: x=0, y=imgMidY+0.4, w=imgW, h=0.4
    fontSize=11, italic=true, color=grayText, align="center"

Contenido derecho:
  cx = imgW + 0.35  // = 6.15"
  cw = W - cx - 0.55  // ≈ 6.5"

  Título: x=cx, y=0.75, w=cw, h=0.65
    fontSize=24, bold=true, color=midnight

  Línea Sky Blue: x=cx, y=1.5, w=cw*0.45, h=0.05 — sky

  3 puntos (i = 0-2):
    Barra: x=cx, y=1.75+i*1.35, w=0.06, h=0.85 — sky
    Texto: x=cx+0.2, y=1.75+i*1.35, w=cw-0.25, h=0.85
      fontSize=14, color=darkText

  Fuente/nota: x=cx, y=6.55, w=cw, h=0.4
    fontSize=10, italic=true, color=grayText
```

---

## Slide 12 — Cierre / CTA

**Fondo:** Midnight Blue | **Sin header/footer estándar**

```
Barra izquierda: x=0, y=0, w=0.12, h=H — sky

Logo PNG (Midnight): addLogoCover(slide)
  → slide.addImage({ path: LOGO.midnight, x: 0.5, y: 0.28, w: LOGO_W, h: LOGO_H })

CTA principal "¿Empezamos?": x=0.5, y=1.3, w=9, h=1.4
  fontSize=62, bold=true, color=arctic

Línea: x=0.5, y=2.85, w=7, h=0.05 — sky

Descripción CTA: x=0.5, y=3.05, w=9, h=0.65
  fontSize=18, color="A5B4C1"  ← NO grayText

Botón CTA (Amber Gold): x=0.5, y=3.9, w=4.2, h=0.72 — amber
Texto del botón: x=0.5, y=3.9, w=4.2, h=0.72
  fontSize=16, bold=true, color=midnight, align="center", valign="middle"

Datos de contacto: x=0.5, y=4.85, w=5, h=0.9
  fontSize=14, color=arctic
  [usar array de runs para nexostrat.com (bold), email, WhatsApp]

Garantía: x=0.5, y=5.5, w=9.822, h=0.6
  fontSize=13, italic=true, color="A5B4C1"  ← NO grayText

Tagline (si deck externo): addTagline(slide, 6.2)
  → "Crece sin contratar. Escala sin complicarte." | 13pt italic | color=slateLight
```

---

## Reglas de Color por Tipo de Fondo

| Fondo | Texto principal | Texto secundario | Acento |
|-------|-----------------|------------------|--------|
| Midnight Blue | Arctic White | `#A5B4C1` | Sky Blue |
| Ocean Deep | Arctic White | `#A5B4C1` / Sky Blue | Sky Blue |
| White / Arctic | Midnight Blue / Dark Text | Gray Text | Sky Blue |

**Nunca usar `#6B7280` (grayText) sobre fondos oscuros** — contraste ~2.5:1, muy por debajo del mínimo WCAG AA (4.5:1). Siempre usar `#A5B4C1` o Arctic White en su lugar.

---

## Notas de Regeneración

El script `create_nexostrat_template.js` en el directorio de outputs regenera el archivo PPTX desde cero. Para regenerar:

```bash
cd <outputs-dir>
node create_nexostrat_template.js
```

**Importante:** El script resuelve los logos desde la fuente única de marca `operations/marketing/brand/logos` (NO desde el skill) vía `findBrandLogos(__dirname)`, que asciende hasta encontrar el home canónico. Correr el script desde cualquier punto dentro del repo Nexostrat. No copiar logos dentro del skill.

La fuente es **Inter** (decisión D3, fuente única de todos los canales). Está fijada por la marca — no cambiarla sin actualizar `operations/marketing/brand/brand-identity.md` y `skills/shared/brand.py`.

El TAGLINE se gestiona con la constante `TAGLINE` en el bloque de constantes globales — no hardcodear la cadena.
