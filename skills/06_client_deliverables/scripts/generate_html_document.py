#!/usr/bin/env python3
"""
generate_html_document.py — Nexostrat Client Document (HTML version)
Usage: python generate_html_document.py data_empresa.json [output_dir]

Generates a self-contained HTML file that mirrors the 10-section client DOCX.
No Office license required to view.
"""

import json
import sys
import os
from datetime import datetime
from html import escape as esc

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def slugify(s):
    return s.replace(' ', '-').replace('/', '-').lower()

NAV_SECTIONS = [
    ("resumen",          "Resumen"),
    ("metodologia",      "Metodología"),
    ("empresa-hoy",      "Tu empresa hoy"),
    ("problemas",        "Problemas"),
    ("oportunidades",    "Oportunidades"),
    ("roadmap",          "Roadmap"),
    ("propuesta",        "Propuesta"),
    ("proximos-pasos",   "Próximos pasos"),
    ("sobre-nexostrat",  "Sobre Nexostrat"),
    ("contacto",         "Contacto"),
]

CATS = {"pequeno": "Pequeño", "mediano": "Mediano", "grande": "Grande"}
CAT_COLOR = {"pequeno": "#10B981", "mediano": "#0C1A2E", "grande": "#7C3D12"}

IMPACT_LABELS = {1: "Bajo", 2: "Bajo-Medio", 3: "Medio", 4: "Medio-Alto", 5: "Alto"}
EFFORT_LABELS = {1: "Muy bajo", 2: "Bajo", 3: "Medio", 4: "Alto", 5: "Muy alto"}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px;
  line-height: 1.65;
  color: #1F2937;
  background: #F0FBFF;
}

/* ── Top bar ── */
header {
  background: #0C1A2E;
  color: #fff;
  padding: 18px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,.25);
}
header .brand { font-size: 20px; font-weight: 700; letter-spacing: .5px; }
header .empresa { font-size: 13px; opacity: .75; margin-top: 2px; }
header .date { font-size: 12px; opacity: .65; white-space: nowrap; }

/* ── Side nav ── */
nav {
  position: fixed;
  top: 66px;
  left: 0;
  width: 200px;
  height: calc(100vh - 66px);
  background: #0C1A2E;
  padding: 20px 0;
  overflow-y: auto;
  z-index: 90;
}
nav a {
  display: block;
  color: rgba(255,255,255,.7);
  text-decoration: none;
  font-size: 12.5px;
  padding: 9px 20px;
  border-left: 3px solid transparent;
  transition: all .15s;
}
nav a:hover, nav a.active {
  color: #fff;
  border-left-color: #10B981;
  background: rgba(255,255,255,.06);
}

/* ── Main content ── */
main {
  margin-left: 200px;
  padding: 32px 40px 80px;
  max-width: 960px;
}

/* ── Section ── */
.section {
  background: #fff;
  border-radius: 10px;
  margin-bottom: 32px;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
  overflow: hidden;
}
.section-header {
  background: #0C1A2E;
  color: #fff;
  padding: 16px 24px;
  font-size: 17px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-header.green  { background: #10B981; }
.section-header.amber  { background: #92400E; }
.section-header.light  { background: #F5F5F5; color: #0C1A2E; border-bottom: 2px solid #D1D5DB; }
.section-body { padding: 24px; }

/* ── Cover ── */
.cover {
  background: linear-gradient(135deg, #0C1A2E 0%, #0C1A2E 100%);
  color: #fff;
  border-radius: 10px;
  padding: 48px 40px;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,.2);
}
.cover .tag {
  display: inline-block;
  background: rgba(255,255,255,.15);
  border: 1px solid rgba(255,255,255,.3);
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 16px;
}
.cover h1 { font-size: 32px; font-weight: 800; margin-bottom: 8px; }
.cover .sub { font-size: 15px; opacity: .75; margin-bottom: 28px; }
.cover .divider { border: none; border-top: 1px solid rgba(255,255,255,.2); margin: 24px 0; }
.cover .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 24px; font-size: 13px; }
.cover .meta-item label { opacity: .6; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .5px; }
.cover .meta-item span { font-weight: 600; }

/* ── Methodology steps ── */
.method-steps { display: flex; flex-direction: column; gap: 16px; }
.method-step {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.method-step .num {
  flex-shrink: 0;
  width: 36px; height: 36px;
  background: #0C1A2E;
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}
.method-step .content h4 { font-size: 14px; color: #0C1A2E; margin-bottom: 3px; }
.method-step .content p  { font-size: 13px; color: #6B7280; }

/* ── Kpi bar ── */
.kpi-bar { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 20px; }
.kpi { background: #F0FBFF; border: 1px solid #E0F2FE; border-radius: 8px; padding: 10px 16px; font-size: 13px; color: #0C1A2E; }
.kpi strong { display: block; font-size: 15px; }

/* ── Area table ── */
.area-table { width: 100%; border-collapse: collapse; font-size: 13.5px; margin-top: 16px; }
.area-table th { background: #F0FBFF; color: #0C1A2E; text-align: left; padding: 10px 14px; font-size: 12px; text-transform: uppercase; letter-spacing: .4px; }
.area-table td { padding: 10px 14px; border-bottom: 1px solid #F0FBFF; vertical-align: top; }
.area-table tr:last-child td { border-bottom: none; }
.area-table .area-name { font-weight: 700; color: #10B981; white-space: nowrap; }

/* ── Problem card ── */
.problem-card { border: 1px solid #D1D5DB; border-radius: 8px; margin-bottom: 20px; overflow: hidden; }
.problem-card .pc-head {
  background: #0C1A2E;
  color: #fff;
  padding: 12px 18px;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}
.problem-card .pc-num {
  background: rgba(255,255,255,.2);
  width: 26px; height: 26px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800;
  flex-shrink: 0;
}
.problem-card .pc-body { padding: 16px 18px; }
.problem-card .pc-desc { font-size: 13.5px; color: #0D4A6B; margin-bottom: 12px; line-height: 1.6; }
.cita-box {
  background: #F0FBFF;
  border-left: 4px solid #0C1A2E;
  padding: 10px 14px;
  font-style: italic;
  font-size: 13px;
  color: #0C1A2E;
  border-radius: 0 6px 6px 0;
  margin-bottom: 12px;
}
.cita-label { font-style: normal; font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: .4px; margin-bottom: 4px; }
.inaccion-box {
  background: #FFF7ED;
  border: 1px solid #FED7AA;
  border-radius: 6px;
  padding: 10px 14px;
}
.inaccion-box .ic-label { font-size: 11px; font-weight: 700; color: #92400E; text-transform: uppercase; letter-spacing: .4px; margin-bottom: 4px; }
.inaccion-box .ic-value { font-size: 13px; color: #7C3D12; font-weight: 600; }
.inaccion-box .ic-calc { font-size: 12px; color: #92400E; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }
.tag-estimado { font-size: 10px; background: #FED7AA; color: #92400E; padding: 2px 7px; border-radius: 10px; font-style: normal; margin-left: 6px; }

/* ── Opportunity card ── */
.opp-card { border: 1px solid #D1D5DB; border-radius: 8px; margin-bottom: 20px; overflow: hidden; }
.opp-card .oc-head {
  background: #F5F5F5;
  border-bottom: 1px solid #D1D5DB;
  padding: 12px 18px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
}
.opp-card .oc-title { font-size: 14px; font-weight: 700; color: #0C1A2E; }
.opp-card .oc-price { font-size: 13px; font-weight: 700; color: #10B981; white-space: nowrap; }
.opp-card .oc-body { padding: 14px 18px; }
.opp-card .oc-desc { font-size: 13.5px; color: #0D4A6B; margin-bottom: 10px; line-height: 1.6; }
.opp-card .oc-benefit {
  background: #F0FDF4;
  border-left: 4px solid #10B981;
  padding: 8px 12px;
  font-size: 13px;
  color: #065F46;
  border-radius: 0 6px 6px 0;
  margin-bottom: 10px;
}
.opp-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}
.badge-cat    { background: #E0F2FE; color: #0EA5E9; }
.badge-qw     { background: #D1FAE5; color: #065F46; }
.badge-area   { background: #F3F4F6; color: #0D4A6B; }
.badge-infra  { background: #FEF3C7; color: #92400E; }
.score-bar { display: flex; gap: 4px; align-items: center; font-size: 12px; color: #6B7280; }
.score-dot { width: 10px; height: 10px; border-radius: 50%; background: #D1D5DB; }
.score-dot.filled { background: #10B981; }
.score-dot.filled.impact { background: #0C1A2E; }

/* ── Priority table ── */
.priority-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.priority-table th {
  background: #0C1A2E; color: #fff;
  padding: 10px 12px; text-align: left; font-size: 11.5px;
}
.priority-table td { padding: 10px 12px; border-bottom: 1px solid #F0FBFF; vertical-align: middle; }
.priority-table tr:last-child td { border-bottom: none; }
.priority-table tr:nth-child(even) td { background: #F5F5F5; }

/* ── Roadmap ── */
.roadmap-phase { margin-bottom: 28px; }
.roadmap-phase .rp-header {
  display: flex; align-items: center; gap: 12px; margin-bottom: 14px;
}
.rp-badge {
  background: #0C1A2E; color: #fff;
  padding: 6px 16px; border-radius: 20px;
  font-size: 13px; font-weight: 700; white-space: nowrap;
}
.rp-badge.ph2 { background: #10B981; }
.rp-badge.ph3 { background: #92400E; }
.rp-desc { font-size: 13px; color: #6B7280; }
.rp-items { display: flex; flex-wrap: wrap; gap: 10px; }
.rp-item {
  background: #F0FBFF; border: 1px solid #E0F2FE;
  border-radius: 6px; padding: 8px 14px;
  font-size: 13px; color: #0C1A2E;
}
.rp-item.ph2 { background: #F0FDF4; border-color: #A7F3D0; color: #065F46; }
.rp-item.ph3 { background: #FFF7ED; border-color: #FED7AA; color: #92400E; }

/* ── Proposal ── */
.total-box {
  background: #0C1A2E; color: #fff;
  border-radius: 10px; padding: 24px 28px;
  margin-bottom: 24px; text-align: center;
}
.total-box .tb-label { font-size: 12px; opacity: .7; text-transform: uppercase; letter-spacing: .5px; }
.total-box .tb-value { font-size: 42px; font-weight: 800; margin: 6px 0; color: #F59E0B; }
.total-box .tb-sub { font-size: 13px; opacity: .75; }

.entry-box {
  background: #F0FDF4; border: 2px solid #10B981;
  border-radius: 10px; padding: 20px 24px; margin-bottom: 20px;
}
.entry-box .eb-label { font-size: 11px; font-weight: 700; color: #065F46; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; }
.entry-box .eb-title { font-size: 18px; font-weight: 700; color: #10B981; margin-bottom: 4px; }
.entry-box .eb-price { font-size: 22px; font-weight: 800; color: #065F46; }
.entry-box .eb-fee { font-size: 12px; color: #065F46; margin-top: 4px; }

.payment-box {
  background: #F5F5F5; border: 1px solid #D1D5DB;
  border-radius: 8px; padding: 16px 20px; margin-bottom: 20px;
}
.payment-box h4 { font-size: 13px; color: #0C1A2E; font-weight: 700; margin-bottom: 10px; }
.payment-split { display: flex; gap: 12px; }
.pay-part {
  flex: 1; background: #fff; border: 1px solid #D1D5DB;
  border-radius: 6px; padding: 12px; text-align: center;
}
.pay-part .pp-pct { font-size: 28px; font-weight: 800; color: #0C1A2E; }
.pay-part .pp-label { font-size: 12px; color: #6B7280; margin-top: 2px; }

.guarantee-box {
  background: #F0FBFF; border: 1px solid #E0F2FE;
  border-radius: 8px; padding: 14px 18px;
  font-size: 13px; color: #0C1A2E;
}
.guarantee-box strong { display: block; margin-bottom: 4px; }

/* ── Next steps ── */
.step-list { display: flex; flex-direction: column; gap: 12px; }
.step-item { display: flex; gap: 14px; align-items: flex-start; }
.step-num {
  flex-shrink: 0; width: 32px; height: 32px;
  background: #10B981; color: #fff; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 13px;
}
.step-item .si-content h4 { font-size: 14px; color: #10B981; margin-bottom: 3px; }
.step-item .si-content p  { font-size: 13px; color: #0D4A6B; }

/* ── Sobre Nexostrat ── */
.nexostrat-box {
  background: #0C1A2E; color: #fff;
  border-radius: 10px; padding: 28px 32px;
}
.nexostrat-box h3 { font-size: 18px; font-weight: 700; color: #F59E0B; margin-bottom: 14px; }
.nexostrat-box p  { font-size: 14px; line-height: 1.75; opacity: .9; }

/* ── Contact ── */
.contact-card {
  background: linear-gradient(135deg, #10B981 0%, #065F46 100%);
  color: #fff; border-radius: 10px; padding: 32px;
  text-align: center;
}
.contact-card .cc-name { font-size: 22px; font-weight: 800; margin-bottom: 4px; }
.contact-card .cc-role { font-size: 14px; opacity: .8; margin-bottom: 20px; }
.contact-card .cc-items { display: flex; justify-content: center; flex-wrap: wrap; gap: 16px; }
.contact-card .cc-item {
  background: rgba(255,255,255,.15);
  border-radius: 8px; padding: 10px 18px;
  font-size: 13px; font-weight: 600;
}

/* ── Footer ── */
footer {
  margin-left: 200px;
  background: #0C1A2E; color: rgba(255,255,255,.6);
  text-align: center; padding: 14px;
  font-size: 12px;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  nav { display: none; }
  main, footer { margin-left: 0; }
  .payment-split { flex-direction: column; }
}
"""

NEXT_STEPS = [
    ("Confirmación de avance",
     "Ricardo envía propuesta formal. El cliente confirma las iniciativas a implementar y firma el acuerdo de trabajo."),
    ("Kick-off y accesos",
     "Reunión de arranque. Se definen responsables por área en el cliente, se comparten accesos y se establece el canal de comunicación."),
    ("Implementación Fase 1",
     "Nexostrat construye e itera cada solución con el equipo del cliente. Entrega con capacitación incluida."),
    ("Revisión de resultados",
     "A las 4-6 semanas se mide el impacto real vs. proyectado y se documentan aprendizajes."),
    ("Planificación Fase 2",
     "Con los Quick Wins funcionando, se agenda la planificación de las siguientes iniciativas del roadmap."),
]

METHODOLOGY_STEPS = [
    ("Entendimiento", "Análisis profundo del negocio, sus procesos y sus datos. Sin atajos."),
    ("Diagnóstico", "Identificamos los problemas de mayor impacto y los convertimos en oportunidades concretas de IA."),
    ("Diseño", "Diseñamos la solución técnica adaptada al contexto del cliente, no una plantilla genérica."),
    ("Validación", "Antes de construir, validamos la lógica con el equipo del cliente para garantizar el fit."),
    ("Construcción", "Desarrollamos e integramos la solución en los sistemas existentes del cliente."),
    ("Entrega y soporte", "Capacitación al equipo, garantía de 1 mes y acompañamiento post-implementación."),
]

def fmt_price(op):
    lo = op.get('precio_usd_min')
    hi = op.get('precio_usd_max')
    if not lo:
        return ''
    if hi:
        return f"USD {lo:,} – {hi:,}"
    return f"USD {lo:,}"

def dots(filled, total=5, cls_filled="filled"):
    html = '<span class="score-bar">'
    for i in range(total):
        c = f"score-dot {cls_filled}" if i < filled else "score-dot"
        html += f'<span class="{c}"></span>'
    html += '</span>'
    return html

def build_html(d):
    M = d.get('metadata', {})
    EH = d.get('empresa_hoy', {})
    AREAS = d.get('situacion_por_area', [])
    PROBS = d.get('problemas', [])
    OPS = d.get('oportunidades', [])
    QW = d.get('quick_wins', [])
    FASES = d.get('roadmap_fases', [])
    PROP = d.get('propuesta', {})
    # Content caps — mirrors DOCX page-count control
    PROBS_DOC = PROBS[:5]
    OPS_DOC   = OPS[:6]
    empresa = esc(M.get('empresa', 'Empresa'))
    fecha = esc(M.get('fecha_display', M.get('fecha_iso', '')))
    consultor = esc(M.get('consultor', 'Ricardo'))
    consultor_email = esc(M.get('consultor_email', ''))
    consultor_wa = esc(M.get('consultor_whatsapp', ''))
    sobre = d.get('sobre_nexostrat', '')
    ops_by_id = {o['id']: o for o in OPS}
    entrada_op = ops_by_id.get(PROP.get('iniciativa_entrada_id')) or (OPS[0] if OPS else None)
    upfront = PROP.get('upfront_porcentaje', 50)

    parts = []

    # ── HTML head ──
    parts.append(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diagnóstico de IA — {empresa}</title>
<style>{CSS}</style>
<script>
window.addEventListener('scroll', function() {{
  const sections = document.querySelectorAll('.section[id], .cover[id]');
  const navLinks = document.querySelectorAll('nav a');
  let current = '';
  sections.forEach(s => {{
    if (window.scrollY >= s.offsetTop - 100) current = s.id;
  }});
  navLinks.forEach(a => {{
    a.classList.remove('active');
    if (a.getAttribute('href') === '#' + current) a.classList.add('active');
  }});
}});
</script>
</head>
<body>
""")

    # ── Header ──
    parts.append(f"""
<header>
  <div>
    <div class="brand">Nexostrat</div>
    <div class="empresa">Diagnóstico de IA · {empresa}</div>
  </div>
  <div class="date">{fecha}</div>
</header>
""")

    # ── Nav ──
    nav_html = '<nav>\n'
    for anchor, label in NAV_SECTIONS:
        nav_html += f'  <a href="#{anchor}">{esc(label)}</a>\n'
    nav_html += '</nav>\n'
    parts.append(nav_html)

    # ── Main ──
    parts.append('<main>\n')

    # ── Cover ──
    parts.append(f"""
<div class="cover" id="cover">
  <div class="tag">Diagnóstico de IA</div>
  <h1>{empresa}</h1>
  <div class="sub">Informe de Oportunidades y Hoja de Ruta de Implementación</div>
  <hr class="divider">
  <div class="meta-grid">
    <div class="meta-item"><label>Sector</label><span>{esc(M.get('sector',''))}</span></div>
    <div class="meta-item"><label>Ciudad</label><span>{esc(M.get('ciudad',''))}</span></div>
    <div class="meta-item"><label>Fecha</label><span>{fecha}</span></div>
    <div class="meta-item"><label>Consultor</label><span>{consultor}</span></div>
  </div>
</div>
""")

    # ── Resumen Ejecutivo ──
    qw_items_html = ''
    for qw_id in QW:
        op = ops_by_id.get(qw_id)
        if op:
            qw_items_html += f'<div class="qw-item">⚡ <strong>{esc(op["titulo"])}</strong> — {esc(fmt_price(op))}</div>'
    if not qw_items_html:
        qw_items_html = '<div class="qw-item">Sin quick wins definidos en este diagnóstico.</div>'

    hallazgos_rows = ''
    hallazgos_rows += f'<tr><td>Problemas críticos identificados</td><td style="font-weight:700;color:#B45309;">{len(PROBS_DOC)}</td></tr>'
    hallazgos_rows += f'<tr><td>Oportunidades de IA priorizadas</td><td style="font-weight:700;color:#10B981;">{len(OPS_DOC)}</td></tr>'
    hallazgos_rows += f'<tr><td>Quick Wins recomendados (alta prioridad)</td><td style="font-weight:700;color:#7C3D12;">{len(QW)}</td></tr>'
    hallazgos_rows += f'<tr><td>Iniciativas en el roadmap completo</td><td style="font-weight:700;color:#0C1A2E;">{len(OPS)}</td></tr>'
    total_inv = PROP.get("total_roadmap_usd", 0)
    hallazgos_rows += f'<tr><td>Inversión total estimada (roadmap completo)</td><td style="font-weight:700;color:#0C1A2E;">USD {total_inv:,}</td></tr>'

    sector = esc(M.get('sector', 'su sector'))
    ciudad = esc(M.get('ciudad', ''))
    madurez = esc(EH.get('madurez_digital', ''))
    n_ops = len(OPS_DOC)
    n_qw = len(QW)

    parts.append(f"""
<div class="section" id="resumen">
  <div class="section-header">📄 Resumen ejecutivo</div>
  <div class="section-body">
    <p style="font-size:14px;color:#0D4A6B;line-height:1.8;margin-bottom:20px;">
      Este informe es el resultado del proceso de diagnóstico de Nexostrat aplicado a <strong>{empresa}</strong>,
      una empresa del sector <strong>{sector}</strong>{(' con operaciones en ' + ciudad) if ciudad else ''}.
      Durante el diagnóstico analizamos en profundidad la operación, los procesos internos y el estado digital actual de la organización,
      identificando los puntos de mayor fricción y las oportunidades concretas donde la inteligencia artificial puede generar
      impacto medible en eficiencia, costos o ingresos.
      A lo largo de este documento encontrarás <strong>{len(PROBS_DOC)} problemas críticos</strong> documentados,
      <strong>{n_ops} oportunidades de IA priorizadas</strong> y una hoja de ruta de implementación diseñada
      para que las primeras victorias sean visibles en semanas, no en meses.
    </p>

    <h3 style="font-size:15px;font-weight:700;color:#0C1A2E;margin-bottom:12px;">📊 Hallazgos principales</h3>
    <table class="priority-table" style="margin-bottom:20px;">
      <thead><tr><th>Indicador</th><th>Resultado</th></tr></thead>
      <tbody>{hallazgos_rows}</tbody>
    </table>

    <div class="guarantee-box" style="background:#FFFBEB;border-color:#F59E0B;">
      <strong>⚡ Quick Wins recomendados para empezar</strong>
      <div style="margin-top:10px;">{qw_items_html if qw_items_html else '<em>Ver sección Oportunidades para iniciativas recomendadas.</em>'}</div>
    </div>

    <p style="font-size:13px;color:#6B7280;margin-top:16px;line-height:1.7;">
      Las secciones que siguen detallan cada hallazgo con evidencia específica y estimaciones de impacto.
      Si quieres ir directamente a las recomendaciones, salta a <em>Oportunidades de IA identificadas</em> o al <em>Roadmap de implementación</em>.
    </p>
  </div>
</div>
""")

    # ── Metodología ──
    steps_html = ''
    for i, (title, desc) in enumerate(METHODOLOGY_STEPS, 1):
        steps_html += f"""
    <div class="method-step">
      <div class="num">{i}</div>
      <div class="content">
        <h4>{esc(title)}</h4>
        <p>{esc(desc)}</p>
      </div>
    </div>"""
    parts.append(f"""
<div class="section" id="metodologia">
  <div class="section-header">📋 Metodología del diagnóstico</div>
  <div class="section-body">
    <p style="font-size:13.5px;color:#6B7280;margin-bottom:20px;">
      Nuestro proceso garantiza que cada recomendación esté anclada en la realidad de tu negocio —
      no en tendencias de industria ni soluciones genéricas.
    </p>
    <div class="method-steps">{steps_html}
    </div>
  </div>
</div>
""")

    # ── Empresa hoy ──
    kpis_html = ''.join(f'<div class="kpi">{esc(k)}</div>' for k in EH.get('metricas_clave', []))
    areas_cards_html = ''
    for area in AREAS:
        areas_cards_html += f"""
  <div style="margin-bottom:16px;padding:14px 16px;background:#F5F5F5;border-radius:8px;border:1px solid #D1D5DB;">
    <div style="font-size:12px;font-weight:700;color:#0C1A2E;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;">{esc(area.get('area',''))}</div>
    <p style="font-size:13.5px;color:#0D4A6B;line-height:1.65;margin-bottom:8px;">{esc(area.get('situacion_actual',''))}</p>
    <div style="background:#ECFDF5;border-left:3px solid #10B981;padding:8px 12px;border-radius:0 6px 6px 0;font-size:13px;color:#065F46;">
      <strong style="color:#10B981;">→ Oportunidades identificadas en esta área:</strong> {esc(area.get('oportunidades',''))}
    </div>
  </div>"""

    madurez_label = EH.get('madurez_digital', '')
    parts.append(f"""
<div class="section" id="empresa-hoy">
  <div class="section-header">🏢 Tu empresa hoy</div>
  <div class="section-body">
    <div class="kpi-bar">{kpis_html}</div>
    <p style="font-size:13.5px;color:#0D4A6B;line-height:1.7;margin-bottom:20px;">{esc(EH.get('descripcion',''))}</p>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px;">
      <div style="flex:1;min-width:200px;">
        <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">Madurez digital</div>
        <div style="font-size:15px;font-weight:700;color:#0C1A2E;">{esc(madurez_label)}</div>
        <div style="font-size:12.5px;color:#6B7280;margin-top:2px;">{esc(EH.get('madurez_digital_descripcion',''))}</div>
      </div>
      <div style="flex:1;min-width:200px;">
        <div style="font-size:11px;font-weight:700;color:#6B7280;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px;">Posición competitiva</div>
        <div style="font-size:13.5px;color:#0D4A6B;">{esc(EH.get('posicion_competitiva',''))}</div>
      </div>
    </div>
    <p style="font-size:13px;color:#6B7280;line-height:1.7;margin-bottom:20px;padding:12px 16px;background:#F0FBFF;border-radius:8px;border-left:3px solid #0C1A2E;">
      El nivel de madurez digital{(' "' + esc(madurez_label) + '"') if madurez_label else ' actual'} es el punto de partida para
      cualquier iniciativa de IA. No es un juicio —
      es la línea base desde la que construimos. Las oportunidades identificadas en este diagnóstico están diseñadas
      específicamente para el estado actual de la organización, no para un estado ideal futuro.
    </p>
    <h3 style="font-size:15px;font-weight:700;color:#0C1A2E;margin-bottom:12px;">Situación por área</h3>
    {areas_cards_html}
  </div>
</div>
""")

    # ── Problemas ──
    probs_html = ''
    for p in PROBS_DOC:
        ci = p.get('costo_inaccion', {})
        inaccion_html = ''
        if ci:
            est_tag = '<span class="tag-estimado">estimado</span>' if ci.get('es_estimado') else ''
            inaccion_html = f"""
      <div class="inaccion-box">
        <div class="ic-label">⏱ Costo de no actuar</div>
        <div class="ic-value">{esc(ci.get('descripcion',''))}{est_tag}</div>
        {"<div class='ic-calc'>" + esc(ci.get('calculo','')) + "</div>" if ci.get('calculo') else ''}
      </div>"""
        cita_html = ''
        if p.get('cita_cliente'):
            cita_html = f"""
      <div class="cita-box">
        <div class="cita-label">En tus propias palabras</div>
        "{esc(p['cita_cliente'])}"
      </div>"""
        probs_html += f"""
  <div class="problem-card">
    <div class="pc-head">
      <div class="pc-num">{p.get('id','')}</div>
      {esc(p.get('titulo',''))}
    </div>
    <div class="pc-body">
      <div class="pc-desc">{esc(p.get('descripcion',''))}</div>
      {cita_html}
      {inaccion_html}
    </div>
  </div>"""
    n_probs_shown = len(PROBS_DOC)
    parts.append(f"""
<div class="section" id="problemas">
  <div class="section-header amber">⚠️ Problemas identificados</div>
  <div class="section-body">
    <p style="font-size:13.5px;color:#0D4A6B;line-height:1.8;margin-bottom:20px;">
      Durante el diagnóstico identificamos <strong>{n_probs_shown} problemas operacionales críticos</strong> en <strong>{empresa}</strong>.
      Cada uno fue documentado a partir de la conversación contigo y del análisis de tu operación —
      no son suposiciones teóricas, son fricciones reales que tu equipo enfrenta hoy.
      Para cada problema calculamos el costo de la inacción: lo que te está costando mes a mes
      no tener una solución. En conjunto, estos {n_probs_shown} problemas representan la mayor oportunidad
      de mejora de la organización en el corto plazo.
    </p>
    {probs_html}
  </div>
</div>
""")

    # ── Oportunidades ──
    ops_html = ''
    for op in OPS_DOC:
        is_qw = op.get('id') in QW
        price_str = fmt_price(op)
        fee_html = ''
        if op.get('requiere_infraestructura') and op.get('fee_mensual_usd'):
            fee_html = f'<div style="font-size:12px;color:#6B7280;margin-top:4px;">+ USD {op["fee_mensual_usd"]:,}/mes infraestructura</div>'
        cat = op.get('categoria', 'mediano')
        imp = op.get('impacto_score', 3)
        eff = op.get('esfuerzo_score', 3)
        qw_badge = '<span class="badge badge-qw">⚡ Quick Win</span>' if is_qw else ''
        ops_html += f"""
  <div class="opp-card">
    <div class="oc-head">
      <div class="oc-title">{esc(op.get('titulo',''))}</div>
      <div class="oc-price">{esc(price_str)}</div>
    </div>
    <div class="oc-body">
      <div class="oc-desc">{esc(op.get('descripcion',''))}</div>
      <div class="oc-benefit">✅ {esc(op.get('beneficio_esperado',''))}</div>
      <div class="opp-meta">
        <span class="badge badge-cat">{CATS.get(cat, cat)}</span>
        <span class="badge badge-area">📂 {esc(op.get('area',''))}</span>
        {qw_badge}
        {"<span class='badge badge-infra'>🔧 Requiere infra</span>" if op.get('requiere_infraestructura') else ''}
      </div>
      <div style="display:flex;gap:20px;margin-top:10px;font-size:12px;color:#6B7280;">
        <div>Impacto: {dots(imp, cls_filled='filled impact')} {IMPACT_LABELS.get(imp,'')} </div>
        <div>Esfuerzo: {dots(eff)} {EFFORT_LABELS.get(eff,'')}</div>
      </div>
      {fee_html}
    </div>
  </div>"""

    # Priority table (same capped set, sorted by impact)
    table_rows = ''
    for op in sorted(OPS_DOC, key=lambda x: -x.get('impacto_score', 0)):
        is_qw = op.get('id') in QW
        qw_mark = ' ⚡' if is_qw else ''
        table_rows += f"""
      <tr>
        <td>{esc(op.get('titulo',''))}{qw_mark}</td>
        <td>{esc(op.get('area',''))}</td>
        <td style="font-weight:700;color:#10B981;">{esc(fmt_price(op))}</td>
        <td>{IMPACT_LABELS.get(op.get('impacto_score',3),'')}</td>
        <td>{EFFORT_LABELS.get(op.get('esfuerzo_score',3),'')}</td>
      </tr>"""
    n_ops_shown = len(OPS_DOC)
    n_qw_ops = len([o for o in OPS_DOC if o.get('id') in QW])
    parts.append(f"""
<div class="section" id="oportunidades">
  <div class="section-header green">💡 Oportunidades de IA identificadas</div>
  <div class="section-body">
    <p style="font-size:13.5px;color:#0D4A6B;line-height:1.8;margin-bottom:20px;">
      Identificamos <strong>{n_ops_shown} oportunidades concretas</strong> donde la inteligencia artificial puede
      transformar la operación de <strong>{empresa}</strong> de forma medible.
      Cada oportunidad está directamente vinculada a un problema documentado —
      no son ideas genéricas de IA, son soluciones diseñadas para la realidad específica de tu negocio.
      {('<strong>' + str(n_qw_ops) + ' de estas iniciativas son Quick Wins</strong>: soluciones de alto impacto y bajo esfuerzo de implementación que pueden estar funcionando en menos de 30 días. Son el punto de entrada recomendado para comenzar a construir cultura de IA en la organización.') if n_qw_ops > 0 else 'Para cada oportunidad estimamos el rango de inversión, el impacto esperado y el esfuerzo de implementación.'}
    </p>
    {ops_html}
    <h3 style="font-size:15px;color:#0C1A2E;margin:24px 0 12px;">Resumen comparativo de oportunidades</h3>
    <table class="priority-table">
      <thead>
        <tr><th>Iniciativa</th><th>Área</th><th>Inversión</th><th>Impacto</th><th>Esfuerzo</th></tr>
      </thead>
      <tbody>{table_rows}
      </tbody>
    </table>
  </div>
</div>
""")

    # ── Roadmap ──
    phase_classes = ['', 'ph2', 'ph3']
    fases_html = ''
    for i, fase in enumerate(FASES):
        ph_cls = phase_classes[i] if i < len(phase_classes) else ''
        items_html = ''.join(
            f'<div class="rp-item {ph_cls}">{esc(ops_by_id[oid]["titulo"])}</div>'
            for oid in fase.get('oportunidades_ids', [])
            if oid in ops_by_id
        )
        fases_html += f"""
  <div class="roadmap-phase">
    <div class="rp-header">
      <div class="rp-badge {ph_cls}">{esc(fase.get('fase',''))}</div>
    </div>
    <p style="font-size:13px;color:#6B7280;margin-bottom:10px;">{esc(fase.get('descripcion',''))}</p>
    <div class="rp-items">{items_html}</div>
  </div>"""
    parts.append(f"""
<div class="section" id="roadmap">
  <div class="section-header">🗺 Roadmap de implementación</div>
  <div class="section-body">
    <p style="font-size:13.5px;color:#6B7280;margin-bottom:24px;">
      El roadmap está diseñado para generar victorias rápidas primero y construir sobre ellas.
      No es una secuencia rígida — se adapta según los resultados de cada fase.
    </p>
    {fases_html}
  </div>
</div>
""")

    # ── Propuesta ──
    total = PROP.get('total_roadmap_usd', 0)
    entrada_title = esc(entrada_op['titulo']) if entrada_op else ''
    entrada_price = esc(fmt_price(entrada_op)) if entrada_op else ''
    entrada_fee_html = ''
    if entrada_op and entrada_op.get('requiere_infraestructura') and entrada_op.get('fee_mensual_usd'):
        entrada_fee_html = f'<div class="eb-fee">+ USD {entrada_op["fee_mensual_usd"]:,}/mes infraestructura</div>'

    parts.append(f"""
<div class="section" id="propuesta">
  <div class="section-header">💰 Propuesta económica</div>
  <div class="section-body">
    <div class="total-box">
      <div class="tb-label">Valor total del roadmap completo ({len(OPS)} iniciativas)</div>
      <div class="tb-value">USD {total:,}</div>
      <div class="tb-sub">{esc(PROP.get('descripcion_total',''))}</div>
    </div>

    <div class="entry-box">
      <div class="eb-label">✅ Iniciativa de entrada recomendada</div>
      <div class="eb-title">{entrada_title}</div>
      <div class="eb-price">{entrada_price}</div>
      {entrada_fee_html}
    </div>

    <div class="payment-box">
      <h4>Estructura de pago</h4>
      <div class="payment-split">
        <div class="pay-part">
          <div class="pp-pct">{upfront}%</div>
          <div class="pp-label">Al confirmar</div>
        </div>
        <div class="pay-part">
          <div class="pp-pct">{100-upfront}%</div>
          <div class="pp-label">A la entrega final</div>
        </div>
      </div>
      <p style="font-size:12.5px;color:#6B7280;margin-top:12px;">{esc(PROP.get('estructura_pago_descripcion',''))}</p>
    </div>

    <div class="guarantee-box">
      <strong>🛡 Garantía post-implementación</strong>
      {esc(PROP.get('garantia_descripcion',''))}
    </div>
  </div>
</div>
""")

    # ── Próximos pasos ──
    steps_html2 = ''
    for i, (title, desc) in enumerate(NEXT_STEPS, 1):
        steps_html2 += f"""
    <div class="step-item">
      <div class="step-num">{i}</div>
      <div class="si-content">
        <h4>{esc(title)}</h4>
        <p>{esc(desc)}</p>
      </div>
    </div>"""
    entrada_next = esc(entrada_op['titulo']) if entrada_op else 'la iniciativa de entrada'
    upfront_pct = PROP.get('upfront_porcentaje', 50)
    parts.append(f"""
<div class="section" id="proximos-pasos">
  <div class="section-header green">🚀 Próximos pasos</div>
  <div class="section-body">
    <p style="font-size:13.5px;color:#0D4A6B;line-height:1.8;margin-bottom:20px;">
      Si después de leer este reporte quieres avanzar con la implementación, el proceso es simple:
      (1) Confirmas cuál iniciativa quieres iniciar primero — la recomendada es <strong>{entrada_next}</strong>.
      (2) Firmamos el acuerdo de trabajo y procesas el primer pago ({upfront_pct}% upfront).
      (3) Iniciamos el Ciclo 2 — implementación — en los siguientes 3-5 días hábiles.
      No hay reuniones innecesarias ni procesos complicados: {consultor} queda disponible para resolver
      cualquier duda antes de que tomes la decisión.
    </p>
    <div class="step-list">{steps_html2}
    </div>
    <div style="margin-top:20px;padding:14px 16px;background:#F0FBFF;border-radius:8px;font-size:13px;color:#0C1A2E;border-left:3px solid #0C1A2E;">
      <strong>Contacto directo:</strong>
      {('<span style="margin-left:8px;">📧 ' + consultor_email + '</span>') if consultor_email else ''}
      {('<span style="margin-left:8px;">💬 WhatsApp: ' + consultor_wa + '</span>') if consultor_wa else ''}
    </div>
  </div>
</div>
""")

    # ── Sobre Nexostrat ──
    parts.append(f"""
<div class="section" id="sobre-nexostrat">
  <div class="section-header light">🏛 Sobre Nexostrat</div>
  <div class="section-body">
    <div class="nexostrat-box">
      <h3>Por qué Nexostrat</h3>
      <p>{esc(sobre)}</p>
    </div>
  </div>
</div>
""")

    # ── Contacto ──
    parts.append(f"""
<div class="section" id="contacto">
  <div class="section-header light">📞 Contacto</div>
  <div class="section-body">
    <div class="contact-card">
      <div class="cc-name">{consultor}</div>
      <div class="cc-role">Consultor Senior · Nexostrat</div>
      <div class="cc-items">
        {"<div class='cc-item'>📧 " + consultor_email + "</div>" if consultor_email else ''}
        {"<div class='cc-item'>💬 WhatsApp: " + consultor_wa + "</div>" if consultor_wa else ''}
        <div class='cc-item'>🌐 nexostrat.co</div>
      </div>
    </div>
  </div>
</div>
""")

    parts.append('</main>\n')

    # ── Footer ──
    parts.append(f"""
<footer>
  Diagnóstico de IA · {empresa} · {fecha} · Preparado por Nexostrat
</footer>
</body>
</html>
""")

    return ''.join(parts)


def main():
    if len(sys.argv) < 2:
        print('Usage: python generate_html_document.py data_empresa.json [output_dir]')
        sys.exit(1)
    data_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    d = load_data(data_file)
    M = d.get('metadata', {})
    slug = M.get('empresa_slug', M.get('empresa', 'Empresa').replace(' ', ''))
    date_str = (M.get('fecha_iso', datetime.today().strftime('%Y-%m-%d'))).replace('-', '')
    out_file = os.path.join(output_dir, f"{slug}_Diagnostico_DocumentoCliente_{date_str}.html")
    html = build_html(d)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ HTML documento cliente: {out_file}")

if __name__ == '__main__':
    main()
