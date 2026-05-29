# Patrones del gold standard (encodables)

Patrones extraídos del deck + cheat sheet hechos a mano para la reunión con Andrea (Trixx, mayo 2026) — la vara de calidad. El motor `assets/build_nexostrat_html.py` los implementa; esta referencia los documenta para usarlos también en diseños propios (landing, documento-HTML, microsite).

## 1. Motor de slides (vanilla-JS, sin framework)

```html
<div class="deck"><div class="slides" id="slides">
  <section class="slide dark">...</section>
  <section class="slide light">...</section>
</div></div>
```
```css
.deck{height:100vh;width:100vw;overflow:hidden;position:relative}
.slides{display:flex;height:100%;transition:transform .55s cubic-bezier(.22,.61,.36,1)}
.slide{min-width:100vw;height:100vh;display:flex;flex-direction:column;justify-content:center;
  padding:clamp(2.5rem,7vw,8rem);position:relative}
```
```js
function go(n){i=Math.max(0,Math.min(total-1,n));
  track.style.transform='translateX('+(-i*100)+'vw)';
  document.getElementById('counter').textContent=(i+1)+' / '+total;
  document.getElementById('prog').style.width=((i)/(total-1)*100)+'%';
  for(var k=0;k<dots.length;k++)dots[k].classList.toggle('on',k===i);}
// teclado: ArrowRight/' '/PageDown -> go(i+1); ArrowLeft/PageUp -> go(i-1); Home -> go(0); End -> go(total-1)
```
Navegación: teclado + dots clicables + botones prev/next + barra de progreso fija arriba. Es ~25 líneas; portable a cualquier contexto de plantilla.

## 2. Tokens de marca en `:root` (cambiar marca = cambiar este bloque)

```css
:root{
  --midnight:#0C1A2E; --ocean:#0D4A6B; --sky:#0EA5E9; --emerald:#10B981;
  --amber:#F59E0B; --arctic:#F0FBFF; --grayL:#F5F5F5; --grayMid:#D1D5DB;
  --grayTxt:#6B7280; --darkTxt:#1F2937; --white:#fff;
  --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
}
```
Inter por CDN con fallback de sistema:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

## 3. Temas de slide + estructura sandwich

- `.slide.dark` → `radial-gradient(circle at 78% 18%,#15375b 0%,var(--midnight) 55%)` — portada, cierre, KPIs.
- `.slide.ocean` → `linear-gradient(135deg,var(--ocean) 0%,var(--midnight) 100%)` — stats, divisores.
- `.slide.light` → `var(--arctic)` — contenido.
- Sandwich: portada oscura → contenido claro/mixto → cierre oscuro.
- Sobre oscuros: texto en Arctic o `#bcd3e6`/Slate; **nunca** Gray Text. Amber (`--amber`) solo en `.stat .n` y CTA.

## 4. Responsive (clamp + un breakpoint)

```css
h1{font-size:clamp(2.6rem,6vw,5rem)} h2{font-size:clamp(1.9rem,3.6vw,3.1rem)}
@media(max-width:860px){
  .g3,.g4,.g5,.stats,.principles{grid-template-columns:1fr 1fr}
  .slide{padding:2.2rem 1.6rem;justify-content:flex-start;padding-top:4.5rem;overflow-y:auto;height:auto;min-height:100vh}
  html,body{overflow:auto}
}
```
Desktop: slides full-viewport con scroll horizontal por transform. Celular: contenido scrollable vertical, grids a 2 columnas, tipografía reducida. Centrado y legible en ambos (auditoría F1/H3).

## 5. Logos en base64 (self-contained)

```python
def datauri(p):
    import base64
    return "data:image/png;base64," + base64.b64encode(open(p,"rb").read()).decode("ascii")
# Midnight transparente -> fondos oscuros ; Arctic transparente -> fondos claros
```
Embeber el PNG hace el `.html` autónomo (cero dependencias externas salvo la fuente). Resolver el PNG desde `operations/marketing/brand/logos` (nunca bundlear en el skill).

## 6. QR (auditoría F2)

```python
import io, base64, qrcode          # pip install qrcode[pil]
def qr_datauri(url):
    buf = io.BytesIO(); qrcode.make(url).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
```
Dos al cierre del deck: (1) web de Nexostrat, (2) documentos del cliente (link privado). Embebidos en base64 para mantener el archivo self-contained.

## 7. Cheat sheet (interno) — orden importa

Secciones en este orden: header (logo + badge "USO INTERNO") → objetivo → perfil de la persona → **advertencias (cajas rojas `border-left`) ANTES del guion** → guion por slide (numerado, en el orden del deck) → preguntas para sacar información → FAQ ("si pregunta...") → glosario. Las advertencias van primero porque se leen antes de entrar a la reunión. `@media print` lo deja imprimible (sin sombras, break-inside:avoid).

```css
.warn{background:#FEF2F2;border-left:4px solid #B91C1C;border-radius:0 8px 8px 0;padding:.7rem 1rem;margin-bottom:.6rem}
.warn b{color:#B91C1C;font-weight:800} .warn .arrow{color:var(--emerald);font-weight:700}
```

## 8. Componentes reutilizables (clases del motor)

`.card` (border-top sky, sombra), `.grid.g3/.g4/.g5`, `.stats` + `.stat .n` (Amber), `.strip` (callout emerald), `.steps`/`.step`/`.arrow` (proceso), `.principles`/`.principle` (border-top sky), `.nsteps`/`.ns` (próximos pasos numerados), `.eyebrow` (etiqueta de sección con barra sky), `.tagline` (cierre, con `<span>` sky), `.qrs`/`.qr`.
</content>
