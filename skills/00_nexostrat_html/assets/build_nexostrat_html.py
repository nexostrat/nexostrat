#!/usr/bin/env python3
"""
Motor de HTML de marca Nexostrat — generaliza el gold standard `build_andrea.py`.

Produce entregables HTML self-contained (logos en base64, Inter vía Google Fonts con
fallback de sistema, paleta Aurora en tokens CSS):
  - deck navegable on-brand (cliente) — motor de slides vanilla-JS, responsive
  - cheat sheet (interno) — advertencias ordenadas antes del guion

Uso como librería:
    from build_nexostrat_html import build_deck, build_cheatsheet, slide_cover, slide_content, ...
Uso directo (genera un ejemplo "Empresa Demo"):
    python build_nexostrat_html.py [outdir]

Marca: fuente única en operations/marketing/brand/brand-identity.md.
Los logos NO se bundlean — se resuelven desde operations/marketing/brand/logos.
Voz calibrada: sin "robot", liberar (no reemplazar), sin "IA" en títulos, sin "problema", sin precios.
"""
import base64
import sys
from pathlib import Path


# --------------------------------------------------------------------------
#  Resolución de assets de marca (fuente única — NO bundlear en el skill)
# --------------------------------------------------------------------------
def find_repo_brand_logos(start: Path) -> Path:
    """Asciende hasta encontrar operations/marketing/brand/logos (patrón build_andrea.py)."""
    d = start.resolve()
    for _ in range(12):
        cand = d / "operations" / "marketing" / "brand" / "logos"
        if cand.is_dir():
            return cand
        if d.parent == d:
            break
        d = d.parent
    raise RuntimeError("No encuentro operations/marketing/brand/logos — correr dentro del repo Nexostrat")


LOGOS = find_repo_brand_logos(Path(__file__).resolve().parent)


def datauri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(Path(path).read_bytes()).decode("ascii")


def qr_datauri(url: str):
    """QR como data URI PNG (auditoría F2). Requiere `pip install qrcode[pil]`; None si falta."""
    try:
        import io
        import qrcode
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        return None


LOGO_DARK_BG = datauri(LOGOS / "Nexostrat_Logo_Fondo_Midnight_Transparente.png")   # logo claro → fondos oscuros
LOGO_LIGHT_BG = datauri(LOGOS / "Nexostrat_Logo_Fondo_Arctic_Transparente.png")     # logo oscuro → fondos claros

TAGLINE_HTML = 'Crece sin contratar. <span>Escala sin complicarte.</span>'

# --------------------------------------------------------------------------
#  CSS base — paleta Aurora + Inter + motor de slides (del gold standard)
# --------------------------------------------------------------------------
DECK_CSS = r"""
  :root{
    --midnight:#0C1A2E; --ocean:#0D4A6B; --sky:#0EA5E9; --emerald:#10B981;
    --amber:#F59E0B; --arctic:#F0FBFF; --grayL:#F5F5F5; --grayMid:#D1D5DB;
    --grayTxt:#6B7280; --darkTxt:#1F2937; --white:#fff;
    /* Inter es elección DELIBERADA de marca (D3) — override consciente de la guía base frontend-design */
    --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%;overflow:hidden;background:var(--midnight);font-family:var(--font);
    -webkit-font-smoothing:antialiased;color:var(--darkTxt)}
  .progress{position:fixed;top:0;left:0;height:4px;background:var(--sky);width:0;z-index:50;
    transition:width .4s cubic-bezier(.22,.61,.36,1)}
  .deck{height:100vh;width:100vw;overflow:hidden;position:relative}
  .slides{display:flex;height:100%;transition:transform .55s cubic-bezier(.22,.61,.36,1)}
  .slide{min-width:100vw;height:100vh;display:flex;flex-direction:column;justify-content:center;
    padding:clamp(2.5rem,7vw,8rem);position:relative}
  .slide.light{background:var(--arctic);color:var(--darkTxt)}
  .slide.dark{background:radial-gradient(circle at 78% 18%,#15375b 0%,var(--midnight) 55%);color:var(--arctic)}
  .slide.ocean{background:linear-gradient(135deg,var(--ocean) 0%,var(--midnight) 100%);color:var(--arctic)}
  .eyebrow{font-size:clamp(.72rem,1vw,.85rem);font-weight:800;letter-spacing:.22em;text-transform:uppercase;
    color:var(--sky);margin-bottom:1.1rem;display:flex;align-items:center;gap:.7rem}
  .eyebrow::before{content:"";width:34px;height:2px;background:var(--sky);display:inline-block}
  h1{font-size:clamp(2.6rem,6vw,5rem);font-weight:900;line-height:1.02;letter-spacing:-.02em}
  h2{font-size:clamp(1.9rem,3.6vw,3.1rem);font-weight:800;line-height:1.07;letter-spacing:-.015em;color:var(--midnight)}
  .slide.dark h2,.slide.ocean h2{color:var(--arctic)}
  .lead{font-size:clamp(1.02rem,1.45vw,1.3rem);line-height:1.55;color:var(--grayTxt);max-width:60ch;margin-top:1.2rem}
  .slide.dark .lead,.slide.ocean .lead{color:#bcd3e6}
  .cover-logo{width:clamp(230px,26vw,360px);margin-bottom:auto}
  .cover-foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:.9rem;color:#8fb0ca;letter-spacing:.04em}
  .cover h1{margin:.4rem 0 .2rem}
  .cover .sub{font-size:clamp(1.1rem,1.7vw,1.5rem);color:#cfe3f2;font-weight:500;max-width:46ch}
  .cover .kicker{font-size:clamp(1rem,1.3vw,1.15rem);color:var(--sky);font-weight:700;letter-spacing:.04em}
  .grid{display:grid;gap:clamp(1rem,1.6vw,1.6rem);margin-top:clamp(1.6rem,3vw,2.6rem)}
  .g3{grid-template-columns:repeat(3,1fr)} .g4{grid-template-columns:repeat(4,1fr)} .g5{grid-template-columns:repeat(5,1fr)}
  .card{background:var(--white);border:1px solid var(--grayMid);border-radius:16px;
    padding:clamp(1.2rem,1.8vw,1.7rem);border-top:4px solid var(--sky);
    box-shadow:0 10px 30px -18px rgba(12,26,46,.4);display:flex;flex-direction:column}
  .card .tag{font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--ocean);margin-bottom:.5rem}
  .card h3{font-size:clamp(1.02rem,1.3vw,1.22rem);font-weight:800;color:var(--midnight);line-height:1.18;margin-bottom:.55rem}
  .card p{font-size:clamp(.85rem,1vw,.98rem);line-height:1.5;color:var(--grayTxt)}
  .card .num{width:34px;height:34px;border-radius:50%;background:var(--midnight);color:#fff;font-weight:800;
    display:flex;align-items:center;justify-content:center;font-size:.95rem;margin-bottom:.8rem}
  .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(1.5rem,4vw,4rem);margin-top:clamp(2rem,4vw,3.5rem)}
  .stat .n{font-size:clamp(2.8rem,6vw,5rem);font-weight:900;color:var(--amber);line-height:1;letter-spacing:-.02em}
  .stat .l{font-size:clamp(.92rem,1.15vw,1.1rem);color:#cfe3f2;margin-top:.7rem;line-height:1.4;max-width:24ch}
  .strip{margin-top:clamp(1.5rem,2.5vw,2.2rem);background:rgba(16,185,129,.1);border-left:5px solid var(--emerald);
    border-radius:0 12px 12px 0;padding:1.1rem 1.4rem;font-size:clamp(1rem,1.3vw,1.25rem);font-weight:700;color:var(--midnight);max-width:75ch}
  .slide.dark .strip,.slide.ocean .strip{color:var(--arctic)}
  .steps{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-top:clamp(1.8rem,3vw,2.8rem)}
  .step{background:var(--white);border:1px solid var(--grayMid);border-radius:999px;padding:.65rem 1.25rem;font-weight:700;color:var(--ocean);font-size:clamp(.85rem,1vw,1.02rem)}
  .step.dark{background:var(--midnight);color:#fff;border-color:var(--midnight)}
  .arrow{color:var(--sky);font-weight:900;font-size:1.1rem}
  .principles{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-top:clamp(1.8rem,3vw,2.6rem)}
  .principle{border-top:3px solid var(--sky);padding-top:.9rem}
  .principle h4{font-size:clamp(.98rem,1.2vw,1.12rem);color:var(--midnight);font-weight:800;margin-bottom:.35rem}
  .principle p{font-size:clamp(.85rem,1vw,.96rem);color:var(--grayTxt);line-height:1.45}
  .nsteps{margin-top:clamp(1.8rem,3vw,2.6rem);display:flex;flex-direction:column;gap:1rem;max-width:80ch}
  .ns{display:flex;gap:1.1rem;align-items:flex-start}
  .ns .b{flex:none;width:38px;height:38px;border-radius:10px;background:var(--sky);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:1.05rem}
  .ns p{font-size:clamp(.98rem,1.25vw,1.18rem);line-height:1.5;color:var(--darkTxt);padding-top:.35rem}
  .note{margin-top:clamp(1.6rem,2.5vw,2.2rem);font-size:clamp(.92rem,1.1vw,1.05rem);color:var(--grayTxt);font-style:italic;border-left:3px solid var(--grayMid);padding-left:1.1rem;max-width:78ch}
  .close{align-items:flex-start}
  .close-logo{width:clamp(220px,24vw,330px);margin-bottom:2.2rem}
  .tagline{font-size:clamp(1.6rem,3vw,2.6rem);font-weight:800;color:var(--arctic);letter-spacing:-.01em;line-height:1.15;max-width:20ch}
  .tagline span{color:var(--sky)}
  .contact{margin-top:1.6rem;display:flex;flex-wrap:wrap;gap:.6rem 2.2rem;font-size:clamp(.98rem,1.3vw,1.18rem);color:#cfe3f2;font-weight:500}
  .contact b{color:var(--arctic);font-weight:700}
  /* QR (auditoría F2) */
  .qrs{margin-top:auto;display:flex;gap:2.2rem;flex-wrap:wrap}
  .qr{display:flex;flex-direction:column;align-items:center;gap:.5rem}
  .qr img{width:150px;height:150px;background:#fff;border-radius:12px;padding:9px}
  .qr span{font-size:.78rem;color:#9fc0d8;font-weight:700;letter-spacing:.04em}
  .pagefoot{position:absolute;bottom:clamp(1.4rem,2.5vw,2.4rem);left:clamp(2.5rem,7vw,8rem);font-size:.78rem;color:var(--grayTxt);letter-spacing:.05em;font-weight:600}
  .slide.dark .pagefoot,.slide.ocean .pagefoot{color:#6f93b0}
  .nav{position:fixed;bottom:clamp(1.2rem,2.5vw,2.2rem);right:clamp(1.6rem,4vw,3rem);z-index:40;display:flex;align-items:center;gap:1rem}
  .dots{display:flex;gap:.5rem}
  .dot{width:9px;height:9px;border-radius:50%;background:rgba(120,150,175,.45);cursor:pointer;transition:.25s;border:none;padding:0}
  .dot.on{background:var(--sky);transform:scale(1.35)}
  .ctrl{display:flex;gap:.4rem}
  .btn{width:42px;height:42px;border-radius:50%;border:1px solid var(--grayMid);background:rgba(255,255,255,.9);color:var(--midnight);font-size:1.2rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s}
  .btn:hover{background:var(--sky);color:#fff;border-color:var(--sky)}
  .counter{font-size:.85rem;color:var(--grayTxt);font-weight:700;min-width:48px;text-align:right}
  .hint{position:fixed;bottom:clamp(1.2rem,2.5vw,2.2rem);left:clamp(1.6rem,4vw,3rem);z-index:40;font-size:.78rem;color:var(--grayTxt);opacity:.8}
  @media(max-width:860px){
    .g3,.g4,.g5,.stats,.principles{grid-template-columns:1fr 1fr}
    .slide{padding:2.2rem 1.6rem;justify-content:flex-start;padding-top:4.5rem;overflow-y:auto;height:auto;min-height:100vh}
    html,body{overflow:auto}
  }
"""

# Motor de navegación vanilla-JS (verbatim del gold standard): teclado + dots + botones + progreso
DECK_JS = r"""
  var slides=document.querySelectorAll('.slide');
  var track=document.getElementById('slides');
  var total=slides.length, i=0;
  var dotsWrap=document.getElementById('dots');
  for(var k=0;k<total;k++){var d=document.createElement('button');d.className='dot'+(k===0?' on':'');
    d.setAttribute('aria-label','Slide '+(k+1));d.dataset.k=k;dotsWrap.appendChild(d);}
  var dots=document.querySelectorAll('.dot');
  function go(n){i=Math.max(0,Math.min(total-1,n));
    track.style.transform='translateX('+(-i*100)+'vw)';
    document.getElementById('counter').textContent=(i+1)+' / '+total;
    document.getElementById('prog').style.width=((i)/(total-1)*100)+'%';
    for(var k=0;k<dots.length;k++)dots[k].classList.toggle('on',k===i);}
  document.getElementById('next').onclick=function(){go(i+1)};
  document.getElementById('prev').onclick=function(){go(i-1)};
  for(var k=0;k<dots.length;k++)dots[k].onclick=function(e){go(+e.target.dataset.k)};
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();go(i+1);}
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();go(i-1);}
    else if(e.key==='Home'){go(0);}else if(e.key==='End'){go(total-1);}});
  go(0);
"""

FONTS_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')


# --------------------------------------------------------------------------
#  Constructores de slides (cada uno devuelve el HTML de un <section>)
# --------------------------------------------------------------------------
def slide_cover(kicker, title, subtitle, left_foot, right_foot):
    return f'''<section class="slide dark cover">
  <img class="cover-logo" src="{LOGO_DARK_BG}" alt="Nexostrat">
  <div>
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="sub">{subtitle}</p>
  </div>
  <div class="cover-foot"><span>{left_foot}</span><span>{right_foot}</span></div>
</section>'''


def _cards(items, numbered=False, grid="g3"):
    out = []
    for n, it in enumerate(items, 1):
        head = f'<div class="num">{n}</div>' if numbered else f'<div class="tag">{it.get("tag","")}</div>'
        out.append(f'<div class="card">{head}<h3>{it["h"]}</h3><p>{it["p"]}</p></div>')
    return f'<div class="grid {grid}">' + "".join(out) + '</div>'


def slide_content(eyebrow, title, lead, cards=None, numbered=False, grid="g3", strip=None, theme="light"):
    body = f'<div class="eyebrow">{eyebrow}</div><h2>{title}</h2>'
    if lead:
        body += f'<p class="lead">{lead}</p>'
    if cards:
        body += _cards(cards, numbered=numbered, grid=grid)
    if strip:
        body += f'<div class="strip">{strip}</div>'
    return f'<section class="slide {theme}">{body}</section>'


def slide_stats(eyebrow, title, stats, theme="ocean"):
    cells = "".join(f'<div class="stat"><div class="n">{s["n"]}</div><div class="l">{s["l"]}</div></div>' for s in stats)
    return f'<section class="slide {theme}"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2><div class="stats">{cells}</div></section>'


def slide_steps(eyebrow, title, lead, steps, principles):
    chips = []
    for j, s in enumerate(steps):
        chips.append(f'<span class="step{" dark" if j == 0 else ""}">{s}</span>')
        if j < len(steps) - 1:
            chips.append('<span class="arrow">&rarr;</span>')
    prin = "".join(f'<div class="principle"><h4>{p["h"]}</h4><p>{p["p"]}</p></div>' for p in principles)
    return (f'<section class="slide light"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>'
            f'<p class="lead">{lead}</p><div class="steps">{"".join(chips)}</div>'
            f'<div class="principles">{prin}</div></section>')


def slide_nextsteps(eyebrow, title, steps, note):
    rows = "".join(f'<div class="ns"><div class="b">{n}</div><p>{t}</p></div>' for n, t in enumerate(steps, 1))
    return (f'<section class="slide light"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>'
            f'<div class="nsteps">{rows}</div><p class="note">{note}</p></section>')


def slide_close(contacts, qr_links=None):
    """Cierre con tagline, contacto y (auditoría F2) hasta 2 QR: web + documentos del cliente."""
    contact_html = "".join(f'<span><b>{c}</b></span>' for c in contacts)
    qr_html = ""
    if qr_links:
        chunks = []
        for label, url in qr_links:
            uri = qr_datauri(url)
            if uri:
                chunks.append(f'<div class="qr"><img src="{uri}" alt="QR {label}"><span>{label}</span></div>')
        if chunks:
            qr_html = f'<div class="qrs">{"".join(chunks)}</div>'
    return (f'<section class="slide dark close">'
            f'<img class="close-logo" src="{LOGO_DARK_BG}" alt="Nexostrat">'
            f'<div class="tagline">{TAGLINE_HTML}</div>'
            f'<div class="contact">{contact_html}</div>{qr_html}</section>')


def build_deck(page_title, slides_html):
    nav = ('<div class="hint">Usa &larr; &rarr; o la barra espaciadora</div>'
           '<div class="nav"><div class="dots" id="dots"></div>'
           f'<span class="counter" id="counter">1 / {len(slides_html)}</span>'
           '<div class="ctrl"><button class="btn" id="prev" aria-label="Anterior">&#8249;</button>'
           '<button class="btn" id="next" aria-label="Siguiente">&#8250;</button></div></div>')
    return (f'<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'<title>{page_title}</title>\n{FONTS_LINK}\n<style>{DECK_CSS}</style>\n</head>\n<body>\n'
            f'<div class="progress" id="prog"></div>\n<div class="deck"><div class="slides" id="slides">\n'
            + "\n".join(slides_html)
            + f'\n</div></div>\n{nav}\n<script>{DECK_JS}</script>\n</body>\n</html>')


# --------------------------------------------------------------------------
#  Cheat sheet (interno) — advertencias ANTES del guion (orden del gold standard)
# --------------------------------------------------------------------------
CHEAT_CSS = r"""
  :root{--midnight:#0C1A2E;--ocean:#0D4A6B;--sky:#0EA5E9;--emerald:#10B981;--amber:#F59E0B;
    --arctic:#F0FBFF;--grayTxt:#6B7280;--darkTxt:#1F2937;--warn:#B91C1C;--warnbg:#FEF2F2;
    --font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;}
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:var(--font);color:var(--darkTxt);background:#e8eef3;line-height:1.5;-webkit-font-smoothing:antialiased}
  .wrap{max-width:980px;margin:0 auto;padding:2rem 1.2rem 4rem}
  header{background:linear-gradient(135deg,var(--ocean),var(--midnight));color:var(--arctic);
    border-radius:16px;padding:1.6rem 1.8rem;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}
  header img{height:34px}
  header .t h1{font-size:1.5rem;font-weight:900;letter-spacing:-.01em}
  header .t p{font-size:.92rem;color:#cfe3f2;margin-top:.2rem}
  .badge{display:inline-block;background:rgba(245,158,11,.18);color:var(--amber);border:1px solid var(--amber);
    border-radius:999px;padding:.15rem .7rem;font-size:.72rem;font-weight:800;letter-spacing:.08em;margin-top:.5rem}
  section{background:#fff;border-radius:14px;padding:1.4rem 1.6rem;margin-top:1.1rem;box-shadow:0 6px 20px -14px rgba(12,26,46,.4)}
  h2{font-size:.78rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--sky);
    margin-bottom:.9rem;display:flex;align-items:center;gap:.6rem}
  h2::before{content:"";width:26px;height:2px;background:var(--sky)}
  .obj{font-size:1.05rem;font-weight:600;color:var(--midnight);line-height:1.5}
  .prof{display:grid;grid-template-columns:1fr 1fr;gap:.6rem 1.6rem;font-size:.95rem}
  .prof b{color:var(--ocean)}
  .warn{background:var(--warnbg);border-left:4px solid var(--warn);border-radius:0 8px 8px 0;
    padding:.7rem 1rem;margin-bottom:.6rem;font-size:.95rem}
  .warn b{color:var(--warn);font-weight:800}
  .warn .arrow{color:var(--emerald);font-weight:700}
  .guion .row{display:flex;gap:1rem;padding:.7rem 0;border-bottom:1px solid #eef1f4}
  .guion .row:last-child{border-bottom:none}
  .guion .s{flex:none;width:30px;height:30px;border-radius:8px;background:var(--midnight);color:#fff;
    font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.9rem}
  .guion .c h4{font-size:.98rem;color:var(--midnight);font-weight:800;margin-bottom:.15rem}
  .guion .c p{font-size:.92rem;color:var(--grayTxt)}
  .q{background:#F0FBFF;border:1px solid #cfe6f5;border-radius:10px;padding:.7rem 1rem;margin-bottom:.55rem;font-size:.96rem}
  .q .lbl{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--ocean);display:block;margin-bottom:.2rem}
  .qa{margin-bottom:.7rem}
  .qa .ask{font-weight:800;color:var(--midnight);font-size:.96rem}
  .qa .ans{font-size:.94rem;color:var(--grayTxt);margin-top:.1rem}
  .gloss{display:grid;grid-template-columns:1fr 1fr;gap:.4rem 1.6rem;font-size:.92rem}
  .gloss b{color:var(--ocean)}
  footer{text-align:center;color:var(--grayTxt);font-size:.8rem;margin-top:1.6rem}
  @media(max-width:680px){.prof,.gloss{grid-template-columns:1fr}}
  @media print{body{background:#fff}section{box-shadow:none;border:1px solid #e5e7eb;break-inside:avoid}.wrap{padding:0}}
"""


def build_cheatsheet(title, subtitle, objetivo, perfil, advertencias, guion, preguntas, faq, glosario):
    prof = "".join(f'<div><b>{k}:</b> {v}</div>' for k, v in perfil)
    warns = "".join(f'<div class="warn"><b>{w["bad"]}</b> <span class="arrow">&rarr;</span> {w["good"]}</div>' for w in advertencias)
    rows = "".join(f'<div class="row"><div class="s">{n}</div><div class="c"><h4>{g["h"]}</h4><p>{g["p"]}</p></div></div>' for n, g in enumerate(guion, 1))
    qs = "".join(f'<div class="q"><span class="lbl">{q["lbl"]}</span>{q["q"]}</div>' for q in preguntas)
    faqs = "".join(f'<div class="qa"><div class="ask">{f["ask"]}</div><div class="ans">{f["ans"]}</div></div>' for f in faq)
    gloss = "".join(f'<div><b>{k}:</b> {v}</div>' for k, v in glosario)
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>{FONTS_LINK}<style>{CHEAT_CSS}</style></head><body>
<div class="wrap">
  <header><div class="t"><h1>{title}</h1><p>{subtitle}</p><span class="badge">USO INTERNO</span></div>
    <img src="{LOGO_DARK_BG}" alt="Nexostrat"></header>
  <section><h2>Objetivo de la reunión</h2><p class="obj">{objetivo}</p></section>
  <section><h2>Quién es</h2><div class="prof">{prof}</div></section>
  <section><h2>OJO &mdash; advertencias (leer antes de entrar)</h2>{warns}</section>
  <section><h2>Guion, en el orden del deck</h2><div class="guion">{rows}</div></section>
  <section><h2>Preguntas para sacar información</h2>{qs}</section>
  <section><h2>Si pregunta... (respuestas rápidas)</h2>{faqs}</section>
  <section><h2>Glosario rápido</h2><div class="gloss">{gloss}</div></section>
  <footer>Nexostrat &middot; documento interno &middot; no compartir con el cliente</footer>
</div></body></html>'''


# --------------------------------------------------------------------------
#  Ejemplo end-to-end ("Empresa Demo") — sirve de exemplar y de prueba de render
# --------------------------------------------------------------------------
def _sample(outdir: Path):
    slides = [
        slide_cover("DIAGNÓSTICO INICIAL", "Empresa Demo",
                    "Lo que vimos y conversamos &mdash; y dónde vemos oportunidad.",
                    "Nexostrat &middot; Consultoría de IA para empresas", "Mayo 2026"),
        slide_content("Punto de partida", "Esto entendemos de Empresa Demo hoy",
            "Una lectura inicial, a partir de la conversación con la dirección y de lo que se observa desde afuera. La afinamos con ustedes.",
            cards=[
                {"tag": "Pilar 1", "h": "La información de la operación", "p": "Hoy repartida entre WhatsApp, Excel y la memoria del equipo. Cuesta consolidarla justo cuando se necesita para decidir."},
                {"tag": "Pilar 2", "h": "El seguimiento de pedidos", "p": "Tiempos, costos y avisos viven en hilos sueltos. Sin un lugar único, algo se pierde."},
                {"tag": "Eje transversal", "h": "El tiempo del equipo", "p": "Tareas repetitivas (copiar, transcribir, pasar de físico a digital) absorben horas que podrían ir a pensar y ejecutar."},
            ], grid="g3"),
        slide_stats("Lo que escuchamos", "El reto, en números de ustedes", [
            {"n": "3 min", "l": "El estándar que pide la operación para tener la información a la mano."},
            {"n": "+120", "l": "Registros por consolidar y dar seguimiento cada semana."},
            {"n": "15-20+", "l": "Grupos de WhatsApp por donde llega la información clave."},
        ]),
        slide_content("Oportunidades", "Dónde vemos oportunidad",
            "El objetivo no es cambiar cómo trabaja el equipo, sino que la información deje de perderse y liberar tiempo de lo repetitivo. Construimos alrededor de lo que ya usan.",
            cards=[
                {"h": "Asistente de WhatsApp", "p": "Un sistema que lee los grupos, separa lo importante y organiza la información. No es una persona: hace el trabajo repetitivo."},
                {"h": "Filtros vivos de correo", "p": "Ordenan la bandeja, extraen lo accionable y avisan de vencimientos antes de que cuesten dinero."},
                {"h": "Tablero maestro vivo", "p": "Cada quien sigue con su hoja; todo alimenta un tablero único con la información consolidada al instante."},
                {"h": "Expediente digital", "p": "Una hoja de vida por activo que se alimenta sola desde las fuentes que ya tienen."},
                {"h": "Liberar al equipo", "p": "Automatizar, persona por persona, las tareas que les roban tiempo."},
            ], numbered=True, grid="g5",
            strip="No reemplazamos a nadie: liberamos al equipo para que dedique su tiempo a lo importante."),
        slide_steps("Cómo lo abordamos", "Un proceso, no un programa suelto",
            "No vendemos una herramienta y nos vamos. Acompañamos cada fase, y ustedes validan antes de construir.",
            ["Entendimiento", "Diseño", "Validación", "Construcción", "Pruebas", "Acompañamiento"],
            [{"h": "En paralelo, sin frenar la operación", "p": "Lo nuevo corre al lado y solo se migra cuando está probado."},
             {"h": "Ustedes aprueban cada etapa", "p": "Nada avanza sin su visto bueno; el diseño se valida antes de construir."},
             {"h": "Primero, victorias rápidas", "p": "Empezamos por una o dos soluciones de impacto inmediato."}]),
        slide_nextsteps("Siguiente", "Próximos pasos",
            ["Revisar juntos este diagnóstico y ajustarlo con lo que ustedes sepan que nos falta.",
             "Conocer la operación de cerca antes de proponer cambios.",
             "Mapear, persona por persona, las tareas que más tiempo roban.",
             "Elegir una o dos soluciones para arrancar."],
            "Este es un primer análisis. Con una sola conversación no se entiende una empresa entera; estos pasos nos sirven para construir sobre bases sólidas."),
        slide_close(["contacto@nexostrat.com", "nexostrat.com"],
                    qr_links=[("nexostrat.com", "https://nexostrat.com"),
                              ("Tus documentos", "https://nexostrat.com/empresa-demo")]),
    ]
    deck = build_deck("Empresa Demo — Diagnóstico Inicial | Nexostrat", slides)

    cheat = build_cheatsheet(
        "Cheat Sheet &middot; Reunión Empresa Demo", "Empresa Demo &mdash; Ciclo 1, Diagnóstico",
        "Reunión corta. Construir confianza, escuchar y, de forma sutil, leer cuánto estarían dispuestos a invertir. El deck no lleva precios.",
        [("Relación", "Influenciador/a; hizo el contacto inicial."),
         ("Rol clave", "Su opinión pesa con la dirección."),
         ("Conoce el tema", "Ya familiarizado con parte del diagnóstico."),
         ("Su dolor propio", "Pasa datos a mano entre sistemas — caso testigo de 'liberar al equipo'.")],
        [{"bad": 'Nunca "robot" ni "bot".', "good": 'di "asistente", "sistema" o "secretario digital".'},
         {"bad": 'No digas "problema".', "good": 'di "oportunidad" o "lo que se puede mejorar".'},
         {"bad": "No afirmes que conocemos su competencia ni su estructura interna.", "good": 'habla de "lo que vimos y conversamos". Si preguntan por competidores, no improvises.'},
         {"bad": "No des precios.", "good": '"lo aterrizamos en la propuesta, depende del alcance".'},
         {"bad": "No prometas plazos cerrados.", "good": '"primero victorias rápidas, en paralelo y sin frenar la operación".'}],
        [{"h": "Portada", "p": 'Abre las gracias en persona. Marco: "te queríamos mostrar lo que entendimos y escuchar tu opinión".'},
         {"h": "Esto entendemos hoy", "p": "Insiste: es una lectura inicial que afinamos con ellos."},
         {"h": "El reto en números", "p": "Son datos de ellos, no nuestros. Sirve para validar o corregir."},
         {"h": "Dónde vemos oportunidad", "p": 'Al llegar a "liberar al equipo" menciona su caso. Remata: "no reemplazamos a nadie".'},
         {"h": "Cómo lo abordamos", "p": "Consultoría, no un programa suelto. En paralelo, aprueban cada etapa."},
         {"h": "Próximos pasos", "p": "Honestidad: es un primer análisis."},
         {"h": "Cierre", "p": "Datos de contacto + QR. Invita a que opine y diga qué faltó."}],
        [{"lbl": "Dolor", "q": "¿Qué es lo que más tiempo le roba al equipo en el día a día?"},
         {"lbl": "Prioridad", "q": "Si pudieras arreglar una sola cosa del flujo de información, ¿cuál sería?"},
         {"lbl": "Presupuesto (sutil)", "q": "Para dimensionar bien lo que propongamos, ¿qué inversión estarían cómodos explorando?"}],
        [{"ask": '"¿Esto reemplaza a mi gente?"', "ans": "No. Libera tiempo de lo repetitivo para enfocarse en lo importante."},
         {"ask": '"¿Tenemos que aprender un software nuevo?"', "ans": "No. Construimos alrededor de lo que ya usan."},
         {"ask": '"¿Cuánto cuesta?"', "ans": "Depende del alcance; lo aterrizamos en la propuesta. Se puede arrancar pequeño."}],
        [("Tablero maestro", "hoja consolidada y viva donde se ve toda la información al instante."),
         ("Tracking", "seguimiento del pedido de punta a punta."),
         ("Carta porte", "documento fiscal del traslado de mercancía."),
         ("Quick win", "solución de impacto inmediato para arrancar.")])

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "deck_example.html").write_text(deck, encoding="utf-8")
    (outdir / "cheatsheet_example.html").write_text(cheat, encoding="utf-8")
    print("OK ->", outdir)
    print("  deck_example.html      ", len(deck), "bytes")
    print("  cheatsheet_example.html", len(cheat), "bytes")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    _sample(out)
