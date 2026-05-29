#!/usr/bin/env python3
"""
Constructor de los entregables de la reunion con Andrea (Grupo Trixx).
Genera dos HTML autonomos (logos embebidos en base64):
  - Trixx_Andrea_Presentacion.html  -> deck navegable on-brand (cliente, sin precios)
  - Trixx_Andrea_CheatSheet.html     -> hoja de apoyo para Ricardo (interno)

Marca: paleta Aurora, tipografia Inter (canal web), logos reales del repo.
Contenido: diagnostico refinado 2026-05-28 (calibrado: sin "robot", liberar no
reemplazar, sin "IA" en titulos, sin "problema", sin precios).
"""
import base64
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
LOGOS = REPO / "operations/marketing/brand/logos"
OUT = Path(__file__).resolve().parent


def datauri(p):
    b = Path(p).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode("ascii")


LOGO_DARK_BG = datauri(LOGOS / "Nexostrat_Logo_Fondo_Midnight_Transparente.png")   # logo claro, para fondos oscuros
LOGO_LIGHT_BG = datauri(LOGOS / "Nexostrat_Logo_Fondo_Arctic_Transparente.png")    # logo oscuro, para fondos claros

# ===========================================================================
#  DECK
# ===========================================================================
DECK = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trixx Logistics Corp — Diagnóstico Inicial | Nexostrat</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root{
    --midnight:#0C1A2E; --ocean:#0D4A6B; --sky:#0EA5E9; --emerald:#10B981;
    --amber:#F59E0B; --arctic:#F0FBFF; --grayL:#F5F5F5; --grayMid:#D1D5DB;
    --grayTxt:#6B7280; --darkTxt:#1F2937; --white:#fff;
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

  /* themes */
  .slide.light{background:var(--arctic);color:var(--darkTxt)}
  .slide.dark{background:radial-gradient(circle at 78% 18%,#15375b 0%,var(--midnight) 55%);color:var(--arctic)}
  .slide.ocean{background:linear-gradient(135deg,var(--ocean) 0%,var(--midnight) 100%);color:var(--arctic)}

  .eyebrow{font-size:clamp(.72rem,1vw,.85rem);font-weight:800;letter-spacing:.22em;text-transform:uppercase;
    color:var(--sky);margin-bottom:1.1rem;display:flex;align-items:center;gap:.7rem}
  .eyebrow::before{content:"";width:34px;height:2px;background:var(--sky);display:inline-block}
  .slide.dark .eyebrow,.slide.ocean .eyebrow{color:var(--sky)}

  h1{font-size:clamp(2.6rem,6vw,5rem);font-weight:900;line-height:1.02;letter-spacing:-.02em}
  h2{font-size:clamp(1.9rem,3.6vw,3.1rem);font-weight:800;line-height:1.07;letter-spacing:-.015em;color:var(--midnight)}
  .slide.dark h2,.slide.ocean h2{color:var(--arctic)}
  .lead{font-size:clamp(1.02rem,1.45vw,1.3rem);line-height:1.55;color:var(--grayTxt);max-width:60ch;margin-top:1.2rem}
  .slide.dark .lead,.slide.ocean .lead{color:#bcd3e6}

  /* cover */
  .cover-logo{width:clamp(230px,26vw,360px);margin-bottom:auto}
  .cover-foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;
    font-size:.9rem;color:#8fb0ca;letter-spacing:.04em}
  .cover h1{margin:.4rem 0 .2rem}
  .cover .sub{font-size:clamp(1.1rem,1.7vw,1.5rem);color:#cfe3f2;font-weight:500;max-width:46ch}
  .cover .kicker{font-size:clamp(1rem,1.3vw,1.15rem);color:var(--sky);font-weight:700;letter-spacing:.04em}

  /* card grids */
  .grid{display:grid;gap:clamp(1rem,1.6vw,1.6rem);margin-top:clamp(1.6rem,3vw,2.6rem)}
  .g3{grid-template-columns:repeat(3,1fr)}
  .g5{grid-template-columns:repeat(5,1fr)}
  .card{background:var(--white);border:1px solid var(--grayMid);border-radius:16px;
    padding:clamp(1.2rem,1.8vw,1.7rem);border-top:4px solid var(--sky);
    box-shadow:0 10px 30px -18px rgba(12,26,46,.4);display:flex;flex-direction:column}
  .card .tag{font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--ocean);margin-bottom:.5rem}
  .card h3{font-size:clamp(1.02rem,1.3vw,1.22rem);font-weight:800;color:var(--midnight);line-height:1.18;margin-bottom:.55rem}
  .card p{font-size:clamp(.85rem,1vw,.98rem);line-height:1.5;color:var(--grayTxt)}
  .card .num{width:34px;height:34px;border-radius:50%;background:var(--midnight);color:#fff;font-weight:800;
    display:flex;align-items:center;justify-content:center;font-size:.95rem;margin-bottom:.8rem}

  /* stats */
  .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(1.5rem,4vw,4rem);margin-top:clamp(2rem,4vw,3.5rem)}
  .stat .n{font-size:clamp(2.8rem,6vw,5rem);font-weight:900;color:var(--amber);line-height:1;letter-spacing:-.02em}
  .stat .l{font-size:clamp(.92rem,1.15vw,1.1rem);color:#cfe3f2;margin-top:.7rem;line-height:1.4;max-width:24ch}

  /* highlight strip */
  .strip{margin-top:clamp(1.5rem,2.5vw,2.2rem);background:rgba(16,185,129,.1);border-left:5px solid var(--emerald);
    border-radius:0 12px 12px 0;padding:1.1rem 1.4rem;font-size:clamp(1rem,1.3vw,1.25rem);font-weight:700;color:var(--midnight);max-width:75ch}

  /* stepper */
  .steps{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin-top:clamp(1.8rem,3vw,2.8rem)}
  .step{background:var(--white);border:1px solid var(--grayMid);border-radius:999px;padding:.65rem 1.25rem;
    font-weight:700;color:var(--ocean);font-size:clamp(.85rem,1vw,1.02rem)}
  .step.dark{background:var(--midnight);color:#fff;border-color:var(--midnight)}
  .arrow{color:var(--sky);font-weight:900;font-size:1.1rem}
  .principles{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-top:clamp(1.8rem,3vw,2.6rem)}
  .principle{border-top:3px solid var(--sky);padding-top:.9rem}
  .principle h4{font-size:clamp(.98rem,1.2vw,1.12rem);color:var(--midnight);font-weight:800;margin-bottom:.35rem}
  .principle p{font-size:clamp(.85rem,1vw,.96rem);color:var(--grayTxt);line-height:1.45}

  /* next steps */
  .nsteps{margin-top:clamp(1.8rem,3vw,2.6rem);display:flex;flex-direction:column;gap:1rem;max-width:80ch}
  .ns{display:flex;gap:1.1rem;align-items:flex-start}
  .ns .b{flex:none;width:38px;height:38px;border-radius:10px;background:var(--sky);color:#fff;font-weight:800;
    display:flex;align-items:center;justify-content:center;font-size:1.05rem}
  .ns p{font-size:clamp(.98rem,1.25vw,1.18rem);line-height:1.5;color:var(--darkTxt);padding-top:.35rem}
  .note{margin-top:clamp(1.6rem,2.5vw,2.2rem);font-size:clamp(.92rem,1.1vw,1.05rem);color:var(--grayTxt);
    font-style:italic;border-left:3px solid var(--grayMid);padding-left:1.1rem;max-width:78ch}

  /* closing */
  .close{align-items:flex-start}
  .close-logo{width:clamp(220px,24vw,330px);margin-bottom:2.2rem}
  .tagline{font-size:clamp(1.6rem,3vw,2.6rem);font-weight:800;color:var(--arctic);letter-spacing:-.01em;line-height:1.15;max-width:20ch}
  .tagline span{color:var(--sky)}
  .contact{margin-top:auto;display:flex;flex-wrap:wrap;gap:.6rem 2.2rem;font-size:clamp(.98rem,1.3vw,1.18rem);color:#cfe3f2;font-weight:500}
  .contact b{color:var(--arctic);font-weight:700}

  .pagefoot{position:absolute;bottom:clamp(1.4rem,2.5vw,2.4rem);left:clamp(2.5rem,7vw,8rem);
    font-size:.78rem;color:var(--grayTxt);letter-spacing:.05em;font-weight:600}
  .slide.dark .pagefoot,.slide.ocean .pagefoot{color:#6f93b0}

  /* nav */
  .nav{position:fixed;bottom:clamp(1.2rem,2.5vw,2.2rem);right:clamp(1.6rem,4vw,3rem);z-index:40;
    display:flex;align-items:center;gap:1rem}
  .dots{display:flex;gap:.5rem}
  .dot{width:9px;height:9px;border-radius:50%;background:rgba(120,150,175,.45);cursor:pointer;transition:.25s;border:none;padding:0}
  .dot.on{background:var(--sky);transform:scale(1.35)}
  .ctrl{display:flex;gap:.4rem}
  .btn{width:42px;height:42px;border-radius:50%;border:1px solid var(--grayMid);background:rgba(255,255,255,.9);
    color:var(--midnight);font-size:1.2rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s}
  .btn:hover{background:var(--sky);color:#fff;border-color:var(--sky)}
  .counter{font-size:.85rem;color:var(--grayTxt);font-weight:700;min-width:48px;text-align:right}
  .hint{position:fixed;bottom:clamp(1.2rem,2.5vw,2.2rem);left:clamp(1.6rem,4vw,3rem);z-index:40;
    font-size:.78rem;color:var(--grayTxt);opacity:.8}

  @media(max-width:860px){
    .g3,.g5,.stats,.principles{grid-template-columns:1fr 1fr}
    .slide{padding:2.2rem 1.6rem;justify-content:flex-start;padding-top:4.5rem;overflow-y:auto;height:auto;min-height:100vh}
    html,body{overflow:auto}
  }
</style>
</head>
<body>
<div class="progress" id="prog"></div>
<div class="deck">
  <div class="slides" id="slides">

    <!-- 1 COVER -->
    <section class="slide dark cover">
      <img class="cover-logo" src="__LOGO_DARK__" alt="Nexostrat">
      <div>
        <div class="kicker">DIAGNÓSTICO INICIAL</div>
        <h1>Trixx Logistics Corp</h1>
        <p class="sub">Lo que vimos y conversamos &mdash; y dónde vemos oportunidad.</p>
      </div>
      <div class="cover-foot">
        <span>Nexostrat &middot; Consultoría de IA para empresas</span>
        <span>Mayo 2026</span>
      </div>
    </section>

    <!-- 2 ENTENDEMOS -->
    <section class="slide light">
      <div class="eyebrow">Punto de partida</div>
      <h2>Esto entendemos de Trixx hoy</h2>
      <p class="lead">Una lectura inicial, a partir de la conversación con la dirección y de lo que se observa desde afuera. La afinamos con ustedes.</p>
      <div class="grid g3">
        <div class="card"><div class="tag">Pilar 1</div><h3>La información de los camiones</h3><p>Más de 120 unidades entre camiones y cajas, hoy sin un expediente por unidad. El crecimiento de la flota y la regulación hacen urgente tener el control de los activos a la mano.</p></div>
        <div class="card"><div class="tag">Pilar 2</div><h3>La información de los contenedores</h3><p>El seguimiento desde el puerto hasta la entrega: tiempos, costos cruzados, demoras. Hoy repartido entre el correo, WhatsApp y la memoria del equipo.</p></div>
        <div class="card"><div class="tag">Eje transversal</div><h3>La información del equipo</h3><p>Llega por muchos grupos de WhatsApp y hojas sueltas. Cuesta consolidarla y tenerla disponible justo cuando se necesita para decidir.</p></div>
      </div>
    </section>

    <!-- 3 STATS -->
    <section class="slide ocean">
      <div class="eyebrow">Lo que escuchamos</div>
      <h2>El reto, en números de ustedes</h2>
      <div class="stats">
        <div class="stat"><div class="n">3 min</div><div class="l">El estándar que pide la operación para tener la información a la mano.</div></div>
        <div class="stat"><div class="n">+120</div><div class="l">Unidades entre camiones y cajas por controlar y dar seguimiento.</div></div>
        <div class="stat"><div class="n">15-20+</div><div class="l">Grupos de WhatsApp por donde llega la información clave cada día.</div></div>
      </div>
    </section>

    <!-- 4 OPORTUNIDADES -->
    <section class="slide light">
      <div class="eyebrow">Oportunidades</div>
      <h2>Dónde vemos oportunidad</h2>
      <p class="lead">El objetivo no es cambiar cómo trabaja el equipo, sino que la información deje de perderse y liberar tiempo de lo repetitivo. Construimos alrededor de lo que ya usan.</p>
      <div class="grid g5">
        <div class="card"><div class="num">1</div><h3>Asistente de WhatsApp</h3><p>Un sistema que lee los grupos, separa lo importante y organiza la información &mdash; fotos, PDF, Excel y cuadros escritos a mano &mdash; sin que nadie cambie su forma de trabajar.</p></div>
        <div class="card"><div class="num">2</div><h3>Filtros vivos de correo</h3><p>Ordenan la bandeja, extraen lo accionable y avisan de vencimientos y demoras antes de que cuesten dinero.</p></div>
        <div class="card"><div class="num">3</div><h3>Tablero maestro vivo</h3><p>Cada quien sigue con su hoja; todo alimenta un tablero único donde se ve la información consolidada al instante.</p></div>
        <div class="card"><div class="num">4</div><h3>Expediente digital de camiones</h3><p>Una hoja de vida por unidad &mdash; mantenimientos, consumos, inspecciones, vencimientos &mdash; que se alimenta sola desde WhatsApp y Samsara.</p></div>
        <div class="card"><div class="num">5</div><h3>Liberar al equipo</h3><p>Sentarnos con cada persona para automatizar las tareas que les roban tiempo, como pasar datos a mano de un Excel a la carta porte.</p></div>
      </div>
      <div class="strip">No reemplazamos a nadie: liberamos al equipo para que dedique su tiempo a lo importante.</div>
    </section>

    <!-- 5 METODO -->
    <section class="slide light">
      <div class="eyebrow">Cómo lo abordamos</div>
      <h2>Un proceso, no un programa suelto</h2>
      <p class="lead">No vendemos una herramienta y nos vamos. Acompañamos cada fase, y ustedes validan antes de construir.</p>
      <div class="steps">
        <span class="step dark">Entendimiento</span><span class="arrow">&rarr;</span>
        <span class="step">Diseño</span><span class="arrow">&rarr;</span>
        <span class="step">Validación</span><span class="arrow">&rarr;</span>
        <span class="step">Construcción</span><span class="arrow">&rarr;</span>
        <span class="step">Pruebas</span><span class="arrow">&rarr;</span>
        <span class="step">Acompañamiento</span>
      </div>
      <div class="principles">
        <div class="principle"><h4>En paralelo, sin frenar la operación</h4><p>El equipo sigue trabajando igual; lo nuevo corre al lado y solo se migra cuando está probado.</p></div>
        <div class="principle"><h4>Ustedes aprueban cada etapa</h4><p>Nada avanza sin su visto bueno. El diseño se valida con ustedes antes de construir.</p></div>
        <div class="principle"><h4>Primero, victorias rápidas</h4><p>Empezamos por una o dos soluciones de impacto inmediato. Lo grande se muestra como horizonte.</p></div>
      </div>
    </section>

    <!-- 6 PROXIMOS PASOS -->
    <section class="slide light">
      <div class="eyebrow">Siguiente</div>
      <h2>Próximos pasos</h2>
      <div class="nsteps">
        <div class="ns"><div class="b">1</div><p>Revisar juntos este diagnóstico y ajustarlo con lo que ustedes sepan que nos falta.</p></div>
        <div class="ns"><div class="b">2</div><p>Visitar la bodega para ver el flujo real de cerca, antes de proponer cambios.</p></div>
        <div class="ns"><div class="b">3</div><p>Mapear, persona por persona, las tareas que más tiempo roban en el día a día.</p></div>
        <div class="ns"><div class="b">4</div><p>Elegir una o dos soluciones para arrancar.</p></div>
      </div>
      <p class="note">Este es un primer análisis. Con una sola conversación no se entiende una empresa entera; estos primeros pasos nos sirven para entenderla bien y construir sobre bases sólidas.</p>
    </section>

    <!-- 7 CIERRE -->
    <section class="slide dark close">
      <img class="close-logo" src="__LOGO_DARK__" alt="Nexostrat">
      <div class="tagline">Crece sin contratar. <span>Escala sin complicarte.</span></div>
      <div class="contact">
        <span><b>contacto@nexostrat.com</b></span>
        <span><b>+57 333 286 3963</b></span>
        <span><b>nexostrat.com</b></span>
      </div>
    </section>

  </div>
</div>

<div class="hint">Usa &larr; &rarr; o la barra espaciadora</div>
<div class="nav">
  <div class="dots" id="dots"></div>
  <span class="counter" id="counter">1 / 7</span>
  <div class="ctrl">
    <button class="btn" id="prev" aria-label="Anterior">&#8249;</button>
    <button class="btn" id="next" aria-label="Siguiente">&#8250;</button>
  </div>
</div>

<script>
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
</script>
</body>
</html>"""

# ===========================================================================
#  CHEAT SHEET  (interno, para Ricardo)
# ===========================================================================
CHEAT = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cheat Sheet — Reunión Andrea | Trixx</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
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
  header .meta{font-size:.82rem;color:#9fc0d8;text-align:right;font-weight:600}
  .badge{display:inline-block;background:rgba(245,158,11,.18);color:var(--amber);border:1px solid var(--amber);
    border-radius:999px;padding:.15rem .7rem;font-size:.72rem;font-weight:800;letter-spacing:.08em;margin-top:.5rem}

  section{background:#fff;border-radius:14px;padding:1.4rem 1.6rem;margin-top:1.1rem;box-shadow:0 6px 20px -14px rgba(12,26,46,.4)}
  h2{font-size:.78rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--sky);
    margin-bottom:.9rem;display:flex;align-items:center;gap:.6rem}
  h2::before{content:"";width:26px;height:2px;background:var(--sky)}
  .obj{font-size:1.05rem;font-weight:600;color:var(--midnight);line-height:1.5}
  .prof{display:grid;grid-template-columns:1fr 1fr;gap:.6rem 1.6rem;font-size:.95rem}
  .prof b{color:var(--ocean)}
  ul{list-style:none}
  li{padding:.4rem 0 .4rem 1.4rem;position:relative;font-size:.96rem}
  li::before{content:"";position:absolute;left:0;top:.78rem;width:7px;height:7px;border-radius:50%;background:var(--sky)}

  .warns li{padding-left:0}
  .warn{background:var(--warnbg);border-left:4px solid var(--warn);border-radius:0 8px 8px 0;
    padding:.7rem 1rem;margin-bottom:.6rem;font-size:.95rem}
  .warn b{color:var(--warn);font-weight:800}
  .warn .arrow{color:var(--emerald);font-weight:700}

  .guion{counter-reset:s}
  .guion .row{display:flex;gap:1rem;padding:.7rem 0;border-bottom:1px solid #eef1f4}
  .guion .row:last-child{border-bottom:none}
  .guion .s{flex:none;width:30px;height:30px;border-radius:8px;background:var(--midnight);color:#fff;
    font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.9rem}
  .guion .c h4{font-size:.98rem;color:var(--midnight);font-weight:800;margin-bottom:.15rem}
  .guion .c p{font-size:.92rem;color:var(--grayTxt)}

  .q{background:#F0FBFF;border:1px solid #cfe6f5;border-radius:10px;padding:.7rem 1rem;margin-bottom:.55rem;font-size:.96rem}
  .q.budget{background:rgba(16,185,129,.08);border-color:var(--emerald)}
  .q .lbl{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--ocean);display:block;margin-bottom:.2rem}
  .q.budget .lbl{color:var(--emerald)}

  .qa{margin-bottom:.7rem}
  .qa .ask{font-weight:800;color:var(--midnight);font-size:.96rem}
  .qa .ans{font-size:.94rem;color:var(--grayTxt);margin-top:.1rem}
  .gloss{display:grid;grid-template-columns:1fr 1fr;gap:.4rem 1.6rem;font-size:.92rem}
  .gloss b{color:var(--ocean)}
  footer{text-align:center;color:var(--grayTxt);font-size:.8rem;margin-top:1.6rem}
  @media(max-width:680px){.prof,.gloss{grid-template-columns:1fr}}
  @media print{body{background:#fff}section{box-shadow:none;border:1px solid #e5e7eb;break-inside:avoid}.wrap{padding:0}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="t">
      <h1>Cheat Sheet &middot; Reunión con Andrea</h1>
      <p>Trixx Logistics Corp &mdash; Ciclo 1, Diagnóstico</p>
      <span class="badge">USO INTERNO &middot; RICARDO</span>
    </div>
    <img src="__LOGO_DARK__" alt="Nexostrat">
  </header>

  <section>
    <h2>Objetivo de la reunión</h2>
    <p class="obj">Reunión corta. Construir confianza con Andrea, hacerla sentir parte y escuchar su opinión. De forma sutil, leer cuánto creen que estarían dispuestos a invertir. El deck no lleva precios.</p>
  </section>

  <section>
    <h2>Quién es Andrea</h2>
    <div class="prof">
      <div><b>Relación:</b> hija de María Helena (la decisora real). NO es hija de Héctor.</div>
      <div><b>Rol clave:</b> influenciadora e hizo el contacto inicial. Su opinión pesa con María Helena y Héctor.</div>
      <div><b>Conoce el tema:</b> ya está familiarizada con parte del diagnóstico.</div>
      <div><b>Su dolor propio:</b> pasa datos a mano de un Excel a la carta porte (caso testigo de "liberar al equipo").</div>
    </div>
  </section>

  <section>
    <h2>OJO &mdash; advertencias (leer antes de entrar)</h2>
    <div class="warns">
      <div class="warn"><b>Nunca "robot" ni "bot".</b> <span class="arrow">&rarr;</span> di "asistente", "sistema" o "secretario digital". Héctor creyó que veníamos a vender robots físicos para cargar cajas.</div>
      <div class="warn"><b>No digas "problema".</b> <span class="arrow">&rarr;</span> di "oportunidad" o "lo que se puede mejorar".</div>
      <div class="warn"><b>No afirmes que conocemos su competencia ni su estructura interna.</b> <span class="arrow">&rarr;</span> habla de "lo que vimos y conversamos". Si preguntan por competidores, no improvises.</div>
      <div class="warn"><b>No des precios.</b> <span class="arrow">&rarr;</span> "lo aterrizamos en la propuesta, depende de lo que elijan".</div>
      <div class="warn"><b>No prometas plazos cerrados.</b> <span class="arrow">&rarr;</span> "primero victorias rápidas, en paralelo y sin frenar la operación".</div>
    </div>
  </section>

  <section>
    <h2>Guion, en el orden del deck</h2>
    <div class="guion">
      <div class="row"><div class="s">1</div><div class="c"><h4>Portada</h4><p>Abre tú las gracias en persona. Marco: "te queríamos mostrar lo que entendimos y escuchar tu opinión".</p></div></div>
      <div class="row"><div class="s">2</div><div class="c"><h4>Esto entendemos de Trixx hoy</h4><p>Dos pilares (camiones y contenedores) + la información del equipo. Insiste: es una lectura inicial que afinamos con ellos.</p></div></div>
      <div class="row"><div class="s">3</div><div class="c"><h4>El reto en números</h4><p>Los 3 minutos los dijo María Helena. Son datos de ellos, no nuestros. Sirve para que Andrea valide o corrija.</p></div></div>
      <div class="row"><div class="s">4</div><div class="c"><h4>Dónde vemos oportunidad</h4><p>5 soluciones, sin precios. Al llegar a "liberar al equipo" menciona su caso (Excel a carta porte) &mdash; la hace sentir vista. Remata: "no reemplazamos a nadie".</p></div></div>
      <div class="row"><div class="s">5</div><div class="c"><h4>Cómo lo abordamos</h4><p>Somos consultoría, no un programa suelto. En paralelo, ellos aprueban cada etapa, primero victorias rápidas.</p></div></div>
      <div class="row"><div class="s">6</div><div class="c"><h4>Próximos pasos</h4><p>Visitar la bodega, inmersión por persona, elegir 1-2 soluciones. Honestidad: es un primer análisis.</p></div></div>
      <div class="row"><div class="s">7</div><div class="c"><h4>Cierre</h4><p>Datos de contacto. Invita a que ella opine y nos diga qué faltó.</p></div></div>
    </div>
  </section>

  <section>
    <h2>Preguntas para sacarle información</h2>
    <div class="q"><span class="lbl">Dolor</span>¿Qué es lo que más tiempo le roba al equipo en el día a día?</div>
    <div class="q"><span class="lbl">Prioridad</span>Si pudieras arreglar una sola cosa del flujo de información, ¿cuál sería?</div>
    <div class="q"><span class="lbl">Aspiración</span>¿Qué crees que haría sentir orgullosos a Héctor y a María Helena de mostrar de Trixx?</div>
    <div class="q budget"><span class="lbl">Presupuesto (sutil)</span>Para dimensionar bien lo que propongamos, ¿qué inversión crees que estarían cómodos explorando para algo así?</div>
    <div class="q budget"><span class="lbl">Presupuesto (indirecto)</span>¿Han invertido antes en software o tecnología? ¿Cómo les fue, qué se sintió caro o barato?</div>
  </section>

  <section>
    <h2>Si pregunta... (respuestas rápidas)</h2>
    <div class="qa"><div class="ask">"¿Esto reemplaza a mi gente?"</div><div class="ans">No. Libera tiempo de lo repetitivo para que el equipo se enfoque en lo importante.</div></div>
    <div class="qa"><div class="ask">"¿Tenemos que aprender un software nuevo?"</div><div class="ans">No. Construimos alrededor de lo que ya usan (WhatsApp, Excel). Nadie cambia su forma de trabajar.</div></div>
    <div class="qa"><div class="ask">"¿Cuánto cuesta?"</div><div class="ans">Depende del alcance; lo aterrizamos en la propuesta. Se puede arrancar pequeño.</div></div>
    <div class="qa"><div class="ask">"¿Cuánto se demora?"</div><div class="ans">Primero victorias rápidas. Corremos en paralelo sin frenar la operación.</div></div>
    <div class="qa"><div class="ask">"¿Y si pago una plataforma y mañana la dejo de pagar?"</div><div class="ans">Por eso no los amarramos a un proveedor: la información queda con ustedes, exportable.</div></div>
  </section>

  <section>
    <h2>Glosario rápido (por si surge)</h2>
    <div class="gloss">
      <div><b>Carta porte:</b> documento fiscal del traslado de mercancía (versión 3.1, reforma 2026).</div>
      <div><b>Demoras / almacenajes:</b> costo por días de más de un contenedor en puerto o terminal.</div>
      <div><b>Samsara:</b> el sistema de telemetría y cámaras que ya tienen en las unidades.</div>
      <div><b>Broker:</b> intermediario aduanal/logístico; genera relaciones que hoy se cruzan a mano.</div>
      <div><b>Tablero maestro:</b> hoja consolidada y viva donde se ve toda la información al instante.</div>
      <div><b>Tracking:</b> seguimiento del contenedor desde el puerto hasta la entrega.</div>
    </div>
  </section>

  <footer>Nexostrat &middot; documento interno &middot; no compartir con el cliente</footer>
</div>
</body>
</html>"""

deck = DECK.replace("__LOGO_DARK__", LOGO_DARK_BG).replace("__LOGO_LIGHT__", LOGO_LIGHT_BG)
cheat = CHEAT.replace("__LOGO_DARK__", LOGO_DARK_BG)

(OUT / "Trixx_Andrea_Presentacion.html").write_text(deck, encoding="utf-8")
(OUT / "Trixx_Andrea_CheatSheet.html").write_text(cheat, encoding="utf-8")
print("OK ->", OUT)
print("  Trixx_Andrea_Presentacion.html", len(deck), "bytes")
print("  Trixx_Andrea_CheatSheet.html  ", len(cheat), "bytes")
