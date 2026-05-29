# Diseños de Portada — Nexostrat

Composiciones específicas de portada por tipo de documento. Incluye grillas de posicionamiento e implementación en reportlab (PDF) y docx-js (DOCX).

---

## Principios de Portada Nexostrat

Toda portada Nexostrat parte de estos fundamentos:

1. **Fondo Midnight Blue (`#0C1A2E`) como base** — la portada es el único lugar donde el azul oscuro puede dominar
2. **Texto en Arctic White (`#F0FBFF`)** — contraste máximo sobre el fondo oscuro
3. **Sky Blue (`#0EA5E9`) como el único acento** — una línea, un subtítulo, o un elemento decorativo
4. **Logo PNG en esquina superior izquierda** — usar `Nexostrat_Logo_Fondo_Midnight_Transparente.png` para fondos oscuros. Nunca texto tipográfico como logo.
5. **Al menos 50% de whitespace intencional** — el espacio vacío es parte del diseño
6. **El título es el héroe** — el elemento más grande y prominente de la página

---

## Cómo Obtener la Ruta de los Logos

Los logos **no se bundlean** en el skill. Viven en la fuente única de marca `operations/marketing/brand/logos` (ver `operations/marketing/brand/brand-identity.md`). Se resuelven ascendiendo hasta la raíz del repo — mismo patrón que el gold standard `build_andrea.py`.

```python
import os

# Resuelve los logos desde la fuente única de marca (NO desde el skill).
def find_brand_logos(start=None):
    d = os.path.abspath(start or os.getcwd())
    for _ in range(10):
        cand = os.path.join(d, "operations", "marketing", "brand", "logos")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise RuntimeError("No encuentro operations/marketing/brand/logos — correr dentro del repo Nexostrat")

LOGOS_DIR = find_brand_logos()

# Lockups horizontales (2350×520px — ratio 4.52:1)
LOGO = {
    "arctic":      os.path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Arctic_Transparente.png"),    # DEFAULT fondo claro
    "blanco":      os.path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Blanco_Transparente.png"),
    "midnight":    os.path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Midnight_Transparente.png"),  # portadas oscuras
    "skyblue":     os.path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_SkyBlue_Transparente.png"),
    "mono_oscuro": os.path.join(LOGOS_DIR, "Nexostrat_Logo_Monocromatico_Oscuro_Transparente.png"),
    "mono_claro":  os.path.join(LOGOS_DIR, "Nexostrat_Logo_Monocromatico_Claro_Transparente.png"),
}

# Íconos (512×512px — ratio 1:1, cuadrado)
ICONO = {
    "midnight": os.path.join(LOGOS_DIR, "Nexostrat_Icono_Midnight_Transparente.png"),
    "ocean":    os.path.join(LOGOS_DIR, "Nexostrat_Icono_Ocean_Deep.png"),
    "skyblue":  os.path.join(LOGOS_DIR, "Nexostrat_Icono_SkyBlue.png"),
}

def draw_logo(c, logo_key, x, y_top, width=1.5*72):
    """
    Dibuja el lockup horizontal.
    y_top: coordenada Y de la parte SUPERIOR del logo (en puntos)
    width: ancho en puntos (72 pts = 1 pulgada)
    """
    from reportlab.lib.utils import ImageReader
    aspect = 260 / 1175   # ratio fijo del PNG
    height = width * aspect
    c.drawImage(LOGO[logo_key], x, y_top - height,
                width=width, height=height, mask="auto")

def draw_icono(c, icono_key, x, y_top, width=0.5*72):
    """Dibuja el ícono NX cuando el espacio no permite el lockup."""
    from reportlab.lib.utils import ImageReader
    aspect = 512 / 512    # ratio fijo del PNG (1:1 cuadrado)
    height = width * aspect
    c.drawImage(ICONO[icono_key], x, y_top - height,
                width=width, height=height, mask="auto")
```

---

## Composición 1 — Propuesta Comercial

### Descripción Visual
Portada oscura con el nombre del prospecto como elemento de personalización. Logo PNG arriba a la izquierda, título de la propuesta como elemento central, nombre del cliente en Sky Blue, y el tagline + fecha abajo.

### Grilla de Posicionamiento (US Letter 8.5×11")

```
┌─────────────────────────────────────────┐
│ [logo nexostrat]             [espacio]  │ ← y=10%–12% | PNG 1.5" ancho
│                                         │
│                                         │
│                                         │ ← ~35%: whitespace intencional
│                                         │
│ ─────────────────────────               │ ← y=38% | línea Sky Blue 60% ancho
│                                         │
│ Propuesta de Consultoría en IA          │ ← y=42% | Inter Bold 36pt Arctic White
│                                         │
│ Para: [Nombre de la Empresa]            │ ← y=52% | Inter Regular 18pt Sky Blue
│                                         │
│                                         │
│                                         │
│ Crece sin contratar.                    │ ← y=82% | tagline itálica 12pt Arctic White
│ Escala sin complicarte.                 │
│ Mayo 2026  ·  Confidencial              │ ← y=88% | Inter Regular 11pt Gray 500
│ nexostrat.com                           │ ← y=91%
└─────────────────────────────────────────┘
```

### Implementación PDF (reportlab)

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

# Colores Nexostrat
MIDNIGHT = colors.HexColor('#0C1A2E')
ARCTIC   = colors.HexColor('#F0FBFF')
SKY      = colors.HexColor('#0EA5E9')
GRAY     = colors.HexColor('#6B7280')

# Fuente de marca: Inter (D3). OJO: reportlab embebe solo TrueType (glyf), NO CFF/OTF.
# En Linux, Inter suele venir solo como .otf (CFF); en ese caso este bloque cae a Helvetica.
# El entregable PRIMARIO de este skill es el .docx (docx-js), que sí renderiza Inter por
# nombre vía LibreOffice/Word sin esta limitación. Para PDF pixel-perfect con Inter real,
# instalar Inter TTF o convertir OTF->TTF (fonttools); o usar 00_nexostrat_html para portadas premium.
import subprocess
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
def _inter_ttf(query):
    p = subprocess.run(["fc-match", "-f", "%{file}", query],
                       capture_output=True, text=True).stdout.strip()
    if not p.lower().endswith(".ttf"):
        raise RuntimeError("Inter TrueType no disponible (solo CFF/OTF)")
    return p
try:
    pdfmetrics.registerFont(TTFont('Inter',      _inter_ttf("Inter:weight=regular")))
    pdfmetrics.registerFont(TTFont('Inter-Bold', _inter_ttf("Inter:weight=bold")))
    HF, HFB = 'Inter', 'Inter-Bold'
except Exception:
    HF, HFB = 'Helvetica', 'Helvetica-Bold'

def draw_cover_propuesta(c, titulo, empresa, fecha="Mayo 2026"):
    w, h = letter  # 612 × 792 pts

    # Fondo completo Midnight Blue
    c.setFillColor(MIDNIGHT)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Logo PNG — esquina superior izquierda
    draw_logo(c, "midnight", x=0.75*inch, y_top=h - 0.65*inch, width=1.5*inch)

    # Línea Sky Blue
    c.setStrokeColor(SKY)
    c.setLineWidth(1.5)
    c.line(0.75*inch, h * 0.60, 0.75*inch + w * 0.55, h * 0.60)

    # Título principal (con wrapping automático)
    c.setFillColor(ARCTIC)
    lines = simpleSplit(titulo, HFB, 36, w - 1.5*inch)
    for i, line in enumerate(lines):
        c.setFont(HFB, 36)
        c.drawString(0.75*inch, h * 0.56 - i * 36 * 1.2, line)

    # Nombre del prospecto
    c.setFillColor(SKY)
    c.setFont(HF, 18)
    c.drawString(0.75*inch, h * 0.47, f"Para: {empresa}")

    # Tagline (solo en propuestas y documentos externos)
    c.setFillColor(ARCTIC)
    c.setFont(HF, 12)
    c.drawString(0.75*inch, h * 0.175, "Crece sin contratar. Escala sin complicarte.")

    # Fecha y confidencialidad
    c.setFillColor(GRAY)
    c.setFont(HF, 11)
    c.drawString(0.75*inch, h * 0.13, f"{fecha}  ·  Confidencial")
    c.drawString(0.75*inch, h * 0.10, "nexostrat.com")

    c.showPage()
```

### Implementación DOCX (docx-js)

```javascript
// Portada como tabla full-width con fondo Midnight Blue
// El logo se inserta con ImageRun — requiere leer el PNG desde operations/marketing/brand/logos
const fs = require('fs');
const path = require('path');

// Logos desde la fuente única de marca (NO bundleados en el skill) — resolver canónico.
function findBrandLogos(start){ let d = start || process.cwd();
  for(let i=0;i<10;i++){ const c = path.join(d,"operations","marketing","brand","logos");
    if(fs.existsSync(c)) return c; const p = path.dirname(d); if(p===d) break; d=p; }
  throw new Error("No encuentro operations/marketing/brand/logos — correr dentro del repo Nexostrat"); }
const LOGOS_DIR = findBrandLogos();
const logoPath = path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Midnight_Transparente.png");
const logoData = fs.readFileSync(logoPath);

// Logo PNG: 2350×520px (ratio 4.52:1) → ancho 1.5" = 1371600 EMU → alto = 1371600 × (520/2350) ≈ 303497 EMU
const LOGO_W = 1371600;
const LOGO_H = Math.round(LOGO_W * (520 / 2350));

new Table({
  width: { size: 12240, type: WidthType.DXA },
  columnWidths: [12240],
  rows: [
    new TableRow({
      height: { value: 15840, rule: 'exact' },
      children: [
        new TableCell({
          shading: { fill: '0C1A2E', type: ShadingType.CLEAR },
          borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                     left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
          margins: { top: 3600, bottom: 1440, left: 1440, right: 1440 },
          verticalAlign: VerticalAlign.TOP,
          children: [
            // Logo PNG
            new Paragraph({
              children: [new ImageRun({
                type: "png", data: logoData,
                transformation: { width: Math.round(LOGO_W / 9144), height: Math.round(LOGO_H / 9144) },
                altText: { title: "Nexostrat", description: "Logo Nexostrat", name: "Logo" }
              })],
              spacing: { before: 0, after: 1440 }
            }),
            // Línea decorativa Sky Blue
            new Paragraph({
              children: [new TextRun({ text: '─────────────────────────', color: '0EA5E9', size: 24 })],
              spacing: { before: 0, after: 200 }
            }),
            // Título de la propuesta
            new Paragraph({
              children: [new TextRun({
                text: titulo, font: 'Inter', size: 72, bold: true, color: 'F0FBFF'
              })],
              spacing: { before: 0, after: 240 }
            }),
            // Nombre del prospecto
            new Paragraph({
              children: [new TextRun({
                text: `Para: ${empresa}`, font: 'Inter', size: 36, color: '0EA5E9'
              })],
              spacing: { before: 0, after: 3600 }
            }),
            // Tagline
            new Paragraph({
              children: [new TextRun({
                text: 'Crece sin contratar. Escala sin complicarte.',
                font: 'Inter', size: 22, italic: true, color: 'F0FBFF'
              })],
              spacing: { before: 0, after: 120 }
            }),
            // Fecha y confidencialidad
            new Paragraph({
              children: [new TextRun({
                text: `${fecha}  ·  Confidencial`, font: 'Inter', size: 22, color: '6B7280'
              })]
            }),
            new Paragraph({
              children: [new TextRun({ text: 'nexostrat.com', font: 'Inter', size: 22, color: '6B7280' })]
            }),
          ]
        })
      ]
    })
  ]
})
```

---

## Composición 2 — Diagnóstico / Reporte

### Descripción Visual
Similar a la propuesta pero el nombre de la empresa analizada es el protagonista. El tagline aparece en portada si el documento va para el cliente.

### Grilla de Posicionamiento

```
┌─────────────────────────────────────────┐
│ [logo nexostrat]                        │ ← y=10%–12%
│                                         │
│                                         │
│                                         │
│ DIAGNÓSTICO INICIAL DE IA               │ ← y=40% | Inter Regular 16pt Sky Blue
│ ─────────────────────────               │ ← y=44% | línea Sky Blue
│                                         │
│ [Nombre de la Empresa]                  │ ← y=48% | Inter Bold 42pt Arctic White
│                                         │
│ Reporte de Oportunidades                │ ← y=58% | Inter Regular 18pt Arctic
│                                         │
│                                         │
│ Crece sin contratar.                    │ ← y=82% | tagline itálica 12pt Arctic White
│ Escala sin complicarte.                 │
│ Mayo 2026  ·  Confidencial              │ ← y=88%
│ nexostrat.com                           │ ← y=91%
└─────────────────────────────────────────┘
```

### Implementación PDF (reportlab)

```python
def draw_cover_diagnostico(c, empresa, subtitulo="Reporte de Oportunidades",
                            fecha="Mayo 2026", incluir_tagline=True):
    w, h = letter

    # Fondo completo
    c.setFillColor(MIDNIGHT)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Logo PNG
    draw_logo(c, "midnight", x=0.75*inch, y_top=h - 0.65*inch, width=1.5*inch)

    # Etiqueta de tipo de documento
    c.setFillColor(SKY)
    c.setFont(HF, 16)
    c.drawString(0.75*inch, h * 0.60, "DIAGNÓSTICO INICIAL DE IA")

    # Línea Sky Blue
    c.setStrokeColor(SKY)
    c.setLineWidth(1.5)
    c.line(0.75*inch, h * 0.57, 0.75*inch + w * 0.55, h * 0.57)

    # Nombre de la empresa (protagonista)
    c.setFillColor(ARCTIC)
    c.setFont(HFB, 42)
    c.drawString(0.75*inch, h * 0.52, empresa)

    # Subtítulo
    c.setFont(HF, 18)
    c.drawString(0.75*inch, h * 0.43, subtitulo)

    # Tagline (incluir si el documento va para el cliente)
    if incluir_tagline:
        c.setFont(HF, 12)
        c.drawString(0.75*inch, h * 0.175, "Crece sin contratar. Escala sin complicarte.")

    # Fecha
    c.setFillColor(GRAY)
    c.setFont(HF, 11)
    c.drawString(0.75*inch, h * 0.13, f"{fecha}  ·  Confidencial")
    c.drawString(0.75*inch, h * 0.10, "nexostrat.com")

    c.showPage()
```

---

## Composición 3 — One-pager / Sell Sheet

### Descripción Visual
No hay portada separada — el documento completo es su propia "portada". Banda de header Midnight Blue en la parte superior (~15% de la página) con logo PNG, tagline, y fecha. El contenido ocupa el resto en Arctic White.

```
┌─────────────────────────────────────────┐
│ [logo nexostrat]             Mayo 2026  │ ← banda Midnight Blue, h=15%
│ Crece sin contratar.                    │ ← tagline, 10pt Sky Blue
│ Escala sin complicarte.                 │
├─────────────────────────────────────────┤
│                                         │
│  HEADLINE PRINCIPAL                     │ ← 24-28pt Midnight Blue Bold
│  Subtitle que amplía el headline        │ ← 14pt Gray 500
│                                         │
│  83%                                    │ ← DATO AMBER GOLD
│  de empresas que adoptan IA...          │
│                                         │
│  ● Beneficio 1                          │
│  ● Beneficio 2                          │
│  ● Beneficio 3                          │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  CTA: Diagnóstico sin costo     │   │ ← recuadro Midnight Blue
│  │  nexostrat.com  ·  WhatsApp     │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Implementación PDF (reportlab)

```python
def draw_onepager_header(c, headline, subtitulo):
    w, h = letter

    # Banda header Midnight Blue
    header_h = h * 0.15
    c.setFillColor(MIDNIGHT)
    c.rect(0, h - header_h, w, header_h, fill=1, stroke=0)

    # Logo PNG en la banda
    draw_logo(c, "midnight", x=0.75*inch, y_top=h - 0.5*inch, width=1.5*inch)

    # Tagline en la banda
    c.setFillColor(SKY)
    c.setFont(HF, 10)
    c.drawString(0.75*inch, h - 1.0*inch, "Crece sin contratar. Escala sin complicarte.")

    # Fecha — derecha de la banda
    c.setFillColor(GRAY)
    c.setFont(HF, 10)
    c.drawRightString(w - 0.75*inch, h - 0.6*inch, "Mayo 2026")

    # Fondo Arctic White para el contenido
    c.setFillColor(colors.HexColor('#F0FBFF'))
    c.rect(0, 0, w, h - header_h, fill=1, stroke=0)

    # Headline
    content_top = h - header_h - 0.5*inch
    c.setFillColor(MIDNIGHT)
    c.setFont(HFB, 26)
    c.drawString(0.75*inch, content_top, headline)

    c.showPage()
```

---

## Composición 4 — Hoja de Ruta

### Descripción Visual
Portada estructurada que sugiere proceso. Similar a Diagnóstico pero con énfasis en fases y período. El tagline aparece en portada si va para el cliente.

```
┌─────────────────────────────────────────┐
│ [logo nexostrat]                        │ ← y=10%–12%
│                                         │
│                                         │
│ HOJA DE RUTA DE IA                      │ ← y=38% | 16pt Sky Blue
│ ─────────────────────                   │
│                                         │
│ [Nombre de la Empresa]                  │ ← y=44% | 40pt Arctic White Bold
│                                         │
│ Implementación en 3 fases               │ ← y=54% | 18pt Arctic White
│ Mayo – Agosto 2026                      │ ← y=59% | 14pt Gray 500
│                                         │
│                                         │
│ Crece sin contratar.                    │ ← y=82% | tagline itálica 12pt Arctic White
│ Escala sin complicarte.                 │
│ Confidencial  ·  nexostrat.com          │ ← y=90%
└─────────────────────────────────────────┘
```

### Implementación

Usar `draw_cover_diagnostico()` con parámetros:
- `empresa`: nombre de la empresa
- `subtitulo`: "Implementación en X fases · [Período]"
- Reemplazar la etiqueta "DIAGNÓSTICO INICIAL DE IA" por "HOJA DE RUTA DE IA"
- `incluir_tagline=True` (va para el cliente)

---

## Header de Páginas Interiores — Logo en DOCX

Para el header de páginas interiores, usar `Nexostrat_Logo_Fondo_Arctic_Transparente.png` (default fondo claro), con ancho de 1.5 pulgadas.

```javascript
// En docx-js — header con logo PNG (LOGOS_DIR resuelto con findBrandLogos, ver arriba)
const headerLogoPath = path.join(LOGOS_DIR, "Nexostrat_Logo_Fondo_Arctic_Transparente.png");
const headerLogoData = fs.readFileSync(headerLogoPath);

// Logo 1.5" ancho → 1371600 EMU; alto = 1371600 × (520/2350) ≈ 303497 EMU
const HDR_LOGO_W = 1371600;
const HDR_LOGO_H = Math.round(HDR_LOGO_W * (520 / 2350));

sections: [{
  headers: {
    default: new Header({
      children: [
        new Paragraph({
          children: [
            new ImageRun({
              type: "png", data: headerLogoData,
              transformation: {
                width: Math.round(HDR_LOGO_W / 9144),   // pts
                height: Math.round(HDR_LOGO_H / 9144)
              },
              altText: { title: "Nexostrat", description: "Logo Nexostrat", name: "Logo" }
            }),
          ],
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "0EA5E9", space: 2 } },
          spacing: { after: 0 }
        })
      ]
    })
  },
  // ... resto de la sección
}]
```

Si el espacio del header es muy reducido, sustituir el lockup por el ícono (`Nexostrat_Icono_Midnight_Transparente.png` sobre fondo oscuro, o `Nexostrat_Icono_Monocromatico_Oscuro_Transparente.png` sobre fondo claro) con ancho de 0.5 pulgadas.

---

## Notas de Implementación

### Fuentes en reportlab

```python
import subprocess
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    # fc-match localiza la fuente; reportlab requiere TrueType (.ttf). Ver nota en "Implementación PDF".
    def _inter_ttf(q):
        p = subprocess.run(["fc-match","-f","%{file}",q], capture_output=True, text=True).stdout.strip()
        if not p.lower().endswith(".ttf"): raise RuntimeError("Inter TrueType no disponible (solo CFF/OTF)")
        return p
    pdfmetrics.registerFont(TTFont('Inter',      _inter_ttf("Inter:weight=regular")))
    pdfmetrics.registerFont(TTFont('Inter-Bold', _inter_ttf("Inter:weight=bold")))
    HF, HFB = 'Inter', 'Inter-Bold'
except Exception:
    # Fallback a Helvetica si Inter TrueType no está disponible en el sistema
    HF, HFB = 'Helvetica', 'Helvetica-Bold'
```

### Texto largo en portadas

```python
from reportlab.lib.utils import simpleSplit

def draw_wrapped_title(c, text, x, y, font, size, color, max_width):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = simpleSplit(text, font, size, max_width)
    line_height = size * 1.2
    for i, line in enumerate(lines):
        c.drawString(x, y - (i * line_height), line)
    return y - (len(lines) * line_height)  # retorna la Y final
```
