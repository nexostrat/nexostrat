#!/usr/bin/env python3
"""generate_html_presentation.py — Nexostrat HTML Presentation (PPTX equivalent)
Usage: python generate_html_presentation.py data_empresa.json [output_dir]
"""
import json, sys, os, re
from datetime import datetime

data_file = sys.argv[1] if len(sys.argv) > 1 else None
output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
if not data_file:
    print("Usage: python generate_html_presentation.py data_empresa.json [output_dir]")
    sys.exit(1)

with open(data_file, 'r', encoding='utf-8') as f:
    d = json.load(f)

M = d.get('metadata', {}); E = d.get('empresa_hoy', {})
PROB = d.get('problemas', []); OPS = d.get('oportunidades', [])
QW = d.get('quick_wins', []); FASES = d.get('roadmap_fases', [])
PROP = d.get('propuesta', {}); PER = d.get('persuasion', {})

empresa = M.get('empresa', 'Empresa')
slug = M.get('empresa_slug', empresa.replace(' ', ''))
fecha = M.get('fecha_display', M.get('fecha_iso', ''))
date_str = (M.get('fecha_iso', '') or datetime.now().strftime('%Y-%m-%d')).replace('-', '')
out_file = os.path.join(output_dir, f"{slug}_Diagnostico_Presentacion_{date_str}.html")

def fmt(n): return f"USD {n:,.0f}" if n else ''
def fmt_range(op):
    if not op: return ''
    if op.get('precio_usd_max'): return f"USD {op['precio_usd_min']:,.0f} – {op['precio_usd_max']:,.0f}"
    return f"USD {op.get('precio_usd_min', 0):,.0f}"

def esc(s): return str(s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

qw_ops = [next((o for o in OPS if o['id'] == qid), None) for qid in QW if any(o['id'] == qid for o in OPS)]
entrada_op = next((o for o in OPS if o['id'] == PROP.get('iniciativa_entrada_id')), qw_ops[0] if qw_ops else (OPS[0] if OPS else {}))

slides_html = []

# ── CSS
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #F0FBFF; color: #1F2937; }
nav { position: sticky; top: 0; background: #0C1A2E; z-index: 100; padding: 10px 24px; display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }
nav a { color: #D1D5DB; text-decoration: none; font-size: 12px; font-weight: bold; }
nav a:hover { color: #F59E0B; }
nav .brand { color: #FFFFFF; font-weight: bold; font-size: 14px; margin-right: 8px; }
.slide { max-width: 960px; margin: 32px auto; background: #FFFFFF; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 24px rgba(30,58,95,0.12); }
.slide-header { background: #0C1A2E; color: #FFFFFF; padding: 14px 28px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; }
.slide-header .brand { font-weight: bold; font-size: 13px; }
.slide-body { padding: 36px 44px 44px; }
.slide-title { font-size: 28px; font-weight: bold; color: #0C1A2E; margin-bottom: 6px; }
.slide-subtitle { font-size: 14px; color: #6B7280; margin-bottom: 28px; }
.slide-footer { background: #F5F5F5; border-top: 1px solid #D1D5DB; padding: 8px 28px; display: flex; justify-content: space-between; font-size: 11px; color: #6B7280; }
.green-accent { display: inline-block; width: 4px; background: #10B981; border-radius: 2px; margin-right: 12px; }
.badge { display: inline-block; background: #F0FBFF; color: #0C1A2E; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; border: 1px solid #E0F2FE; }
.badge-green { background: #ECFDF5; color: #065F46; border-color: #A7F3D0; }
.badge-amber { background: #FFFBEB; color: #92400E; border-color: #FDE68A; }
.step-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 16px 0; }
.step-card { background: #F5F5F5; border: 1px solid #D1D5DB; border-radius: 8px; padding: 20px 16px; text-align: center; }
.step-num { width: 40px; height: 40px; border-radius: 50%; background: #0C1A2E; color: #FFF; font-size: 18px; font-weight: bold; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; }
.step-title { font-weight: bold; color: #0C1A2E; font-size: 13px; margin-bottom: 8px; }
.step-desc { font-size: 11px; color: #6B7280; }
.metrics { display: flex; flex-direction: column; gap: 8px; }
.metric-item { display: flex; align-items: center; background: #F5F5F5; border: 1px solid #D1D5DB; border-radius: 6px; padding: 10px 14px; }
.metric-item::before { content:''; display:block; width:3px; height:100%; background:#10B981; border-radius:2px; margin-right:12px; flex-shrink:0; }
.problem-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
.problem-card { border: 1px solid #D1D5DB; border-radius: 8px; overflow: hidden; }
.problem-card-top { background: #DC2626; height: 4px; }
.problem-card-body { padding: 16px; }
.problem-num { font-size: 13px; font-weight: bold; color: #DC2626; margin-bottom: 6px; }
.problem-title { font-weight: bold; color: #1F2937; font-size: 13px; margin-bottom: 8px; }
.problem-desc { font-size: 11px; color: #0D4A6B; margin-bottom: 10px; }
.quote-box { background: rgba(30,58,95,0.06); border: 1px solid rgba(30,58,95,0.2); border-radius: 6px; padding: 10px 12px; font-size: 11px; font-style: italic; color: #0C1A2E; margin-bottom: 8px; }
.inaction-box { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.4); border-radius: 6px; padding: 8px 12px; }
.inaction-label { font-size: 9px; font-weight: bold; color: #92400E; margin-bottom: 3px; }
.inaction-text { font-size: 11px; color: #1F2937; }
.op-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.op-card { background: #F5F5F5; border: 1px solid #D1D5DB; border-radius: 8px; padding: 14px; position: relative; }
.op-card.qw { background: rgba(14,124,101,0.07); border-color: #10B981; border-width: 2px; }
.op-accent { position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: #0C1A2E; border-radius: 8px 0 0 8px; }
.op-card.qw .op-accent { background: #10B981; }
.op-title { font-weight: bold; font-size: 12px; color: #0C1A2E; margin-bottom: 4px; padding-left: 8px; }
.op-area { font-size: 10px; color: #6B7280; margin-bottom: 6px; padding-left: 8px; }
.op-desc { font-size: 10.5px; color: #0D4A6B; padding-left: 8px; }
.op-price { font-weight: bold; font-size: 11px; color: #10B981; margin-top: 8px; padding-left: 8px; }
.qw-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.qw-card { border: 2px solid #10B981; border-radius: 10px; overflow: hidden; }
.qw-header { background: #10B981; padding: 14px 18px; color: #FFF; font-weight: bold; font-size: 14px; }
.qw-body { padding: 18px; background: rgba(14,124,101,0.05); }
.qw-title { font-weight: bold; font-size: 15px; color: #0C1A2E; margin-bottom: 4px; }
.qw-area { font-size: 11px; color: #6B7280; margin-bottom: 10px; }
.qw-desc { font-size: 11.5px; color: #0D4A6B; margin-bottom: 12px; }
.benefit-box { background: #FFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; }
.benefit-label { font-size: 9px; font-weight: bold; color: #10B981; margin-bottom: 4px; }
.benefit-text { font-size: 11px; color: #0D4A6B; }
.price-box { background: #0C1A2E; border-radius: 6px; padding: 10px 14px; color: #FFF; }
.price-label { font-size: 10px; color: #6B7280; margin-bottom: 2px; }
.price-value { font-size: 18px; font-weight: bold; color: #F59E0B; }
.roadmap-grid { display: flex; gap: 12px; }
.fase-col { flex: 1; border-radius: 8px; overflow: hidden; }
.fase-header { padding: 12px 14px; font-weight: bold; font-size: 12px; color: #FFF; }
.fase-body { background: #F5F5F5; border: 1px solid #D1D5DB; padding: 14px; flex: 1; }
.fase-desc { font-size: 10px; color: #6B7280; font-style: italic; margin-bottom: 10px; }
.fase-op { background: #FFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 8px 10px; margin-bottom: 6px; font-size: 11px; }
.fase-op-title { font-weight: bold; color: #1F2937; }
.fase-op-price { color: #10B981; font-weight: bold; font-size: 10px; }
.propuesta-anchor { background: rgba(30,58,95,0.06); border: 1px solid rgba(30,58,95,0.2); border-radius: 8px; padding: 18px 24px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
.propuesta-anchor-label { font-size: 11px; color: #6B7280; margin-bottom: 4px; }
.propuesta-anchor-value { font-size: 24px; font-weight: bold; color: #0C1A2E; }
.arrow-down { text-align: center; font-size: 20px; color: #10B981; font-weight: bold; margin: 10px 0; }
.entry-grid { display: grid; grid-template-columns: 1fr auto; gap: 16px; align-items: stretch; }
.entry-card { background: rgba(14,124,101,0.08); border: 2px solid #10B981; border-radius: 8px; padding: 18px; }
.entry-title { font-weight: bold; font-size: 16px; color: #0C1A2E; margin-bottom: 6px; }
.entry-desc { font-size: 11.5px; color: #0D4A6B; }
.price-panel { background: #0C1A2E; border-radius: 8px; padding: 20px 24px; min-width: 180px; display: flex; flex-direction: column; justify-content: center; }
.payment-row { background: #F5F5F5; border: 1px solid #D1D5DB; border-radius: 6px; padding: 14px 18px; margin-top: 14px; font-size: 11.5px; color: #0D4A6B; }
.next-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.ns-card { background: #F5F5F5; border: 1px solid #D1D5DB; border-radius: 8px; padding: 18px 14px; text-align: center; position: relative; }
.ns-card-top { position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #10B981; border-radius: 8px 8px 0 0; }
.ns-badge { background: rgba(30,58,95,0.12); color: #0C1A2E; font-size: 10px; font-weight: bold; padding: 3px 10px; border-radius: 10px; display: inline-block; margin-bottom: 10px; }
.ns-icon { font-size: 24px; margin-bottom: 8px; }
.ns-title { font-weight: bold; font-size: 12px; color: #0C1A2E; margin-bottom: 6px; }
.ns-desc { font-size: 10.5px; color: #6B7280; }
.cta-bar { background: #0C1A2E; border-radius: 8px; padding: 18px 24px; margin-top: 20px; display: flex; justify-content: space-between; align-items: center; }
.cta-text { font-weight: bold; font-size: 13px; color: #FFF; }
.cta-contact { font-size: 11px; color: #6B7280; text-align: right; }
"""

def slide_wrapper(slide_num, title, subtitle, body):
    contact = ' · '.join(filter(None, [M.get('consultor_email'), M.get('consultor_whatsapp')]))
    return f"""
<div class="slide" id="slide-{slide_num}">
  <div class="slide-header">
    <span class="brand">NEXOSTRAT</span>
    <span>Slide {slide_num} / 9</span>
  </div>
  <div class="slide-body">
    <div class="slide-title">{esc(title)}</div>
    {'<div class="slide-subtitle">' + esc(subtitle) + '</div>' if subtitle else ''}
    {body}
  </div>
  <div class="slide-footer">
    <span>{esc(empresa)} · {esc(fecha)}</span>
    <span>nexostrat.co</span>
  </div>
</div>"""

# Slide 1: Portada
s1_body = f"""
<div style="background:#0C1A2E;border-radius:8px;padding:60px 48px;position:relative;overflow:hidden;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:6px;background:#10B981;"></div>
  <div style="font-size:28px;font-weight:bold;color:#F59E0B;margin-bottom:12px;">{esc(empresa.upper())}</div>
  <div style="font-size:40px;font-weight:bold;color:#FFFFFF;margin-bottom:20px;line-height:1.2;">Diagnóstico de<br>Oportunidades de IA</div>
  <div style="width:60px;height:3px;background:#10B981;margin-bottom:16px;"></div>
  <div style="font-size:14px;color:#D1D5DB;margin-bottom:8px;">Ciclo 1 — Resultados del Diagnóstico</div>
  <div style="font-size:13px;color:#6B7280;">Preparado por {esc(M.get('consultor','Nexostrat'))} · {esc(fecha)}</div>
  {'<div style="font-size:12px;color:#6B7280;margin-top:6px;">' + esc(' · '.join(filter(None,[M.get('consultor_email'),M.get('consultor_whatsapp')]))) + '</div>' if any([M.get('consultor_email'),M.get('consultor_whatsapp')]) else ''}
</div>"""
slides_html.append(slide_wrapper(1, '', '', s1_body))

# Slide 2: Metodología
steps = [
    ('1','Análisis de empresa','Perfil, financieros, tecnología actual, posición en el mercado'),
    ('2','Análisis de industria','Tendencias del sector, adopción de IA, benchmarks y oportunidades'),
    ('3','Análisis competitivo','Qué están haciendo los competidores, brechas y diferenciadores'),
    ('4','Llamada de descubrimiento','Conversación directa para entender dolores, operación y visión'),
]
steps_html = ''.join(f"""<div class="step-card">
  <div class="step-num">{s}</div>
  <div class="step-title">{t}</div>
  <div class="step-desc">{d}</div>
</div>""" for s,t,d in steps)
s2_body = f'<div class="step-cards">{steps_html}</div><p style="font-size:11px;color:#6B7280;font-style:italic;margin-top:16px;">Estos cuatro pasos nos permiten llegar con contexto suficiente para hacer recomendaciones específicas para tu empresa — no genéricas.</p>'
slides_html.append(slide_wrapper(2,'Cómo llegamos a estas conclusiones','Metodología del diagnóstico',s2_body))

# Slide 3: Tu empresa hoy
metrics_html = ''.join(f'<div class="metric-item">{esc(m)}</div>' for m in E.get('metricas_clave',[])[:5])
s3_body = f"""<div style="display:grid;grid-template-columns:1.6fr 1fr;gap:24px;">
<div>
  <p style="font-size:12px;color:#0D4A6B;line-height:1.6;">{esc(E.get('descripcion',''))}</p>
  <div style="margin-top:16px;background:rgba(30,58,95,0.06);border:1px solid rgba(30,58,95,0.15);border-radius:6px;padding:12px 16px;">
    <span style="font-size:11px;font-weight:bold;color:#0C1A2E;">Madurez digital: </span>
    <span style="font-size:11px;font-weight:bold;color:#10B981;">{esc(E.get('madurez_digital',''))}</span>
    <span style="font-size:11px;color:#6B7280;"> — {esc(E.get('madurez_digital_descripcion',''))}</span>
  </div>
  <p style="font-size:11px;color:#0D4A6B;margin-top:10px;"><strong style="color:#0C1A2E;">Posición competitiva:</strong> {esc(E.get('posicion_competitiva',''))}</p>
</div>
<div class="metrics">{metrics_html}</div>
</div>"""
slides_html.append(slide_wrapper(3,'Tu empresa hoy',esc(empresa),s3_body))

# Slide 4: Problemas
probs_html = ''.join(f"""<div class="problem-card">
  <div class="problem-card-top"></div>
  <div class="problem-card-body">
    <div class="problem-num">#{i+1}</div>
    <div class="problem-title">{esc(p.get('titulo',''))}</div>
    <div class="problem-desc">{esc(p.get('descripcion','')[:160])}</div>
    {'<div class="quote-box">"' + esc(p.get('cita_cliente','')) + '"</div>' if p.get('cita_cliente') else ''}
    {'<div class="inaction-box"><div class="inaction-label">⏱ Costo de no actuar</div><div class="inaction-text">' + esc(p.get('costo_inaccion',{}).get('descripcion','')) + '</div></div>' if p.get('costo_inaccion',{}).get('descripcion') else ''}
  </div>
</div>""" for i,p in enumerate(PROB[:4]))
s4_body = f'<div class="problem-grid">{probs_html}</div>'
slides_html.append(slide_wrapper(4,'Los problemas que encontramos','Lo que identificamos en el análisis y confirmamos en nuestra conversación',s4_body))

# Slide 5: Oportunidades
ops_html = ''.join(f"""<div class="op-card {'qw' if o['id'] in QW else ''}">
  <div class="op-accent"></div>
  {'<span style="position:absolute;top:8px;right:10px;font-size:9px;font-weight:bold;color:#10B981;">⚡ Quick Win</span>' if o['id'] in QW else ''}
  <div class="op-title">{esc(o.get('titulo',''))}</div>
  <div class="op-area">{esc(o.get('area',''))}</div>
  <div class="op-desc">{esc(o.get('descripcion','')[:120])}</div>
  <div class="op-price">{esc(fmt_range(o))}</div>
</div>""" for o in OPS[:6])
s5_body = f'<div class="op-grid">{ops_html}</div>'
slides_html.append(slide_wrapper(5,f'Las oportunidades de IA',f'Identificamos {len(OPS)} oportunidades específicas para {empresa}',s5_body))

# Slide 6: Quick Wins
qwcards_html = ''.join(f"""<div class="qw-card">
  <div class="qw-header">⚡ Quick Win {i+1}</div>
  <div class="qw-body">
    <div class="qw-title">{esc(q.get('titulo',''))}</div>
    <div class="qw-area">{esc(q.get('area',''))}</div>
    <div class="qw-desc">{esc(q.get('descripcion',''))}</div>
    <div class="benefit-box"><div class="benefit-label">✅ Beneficio esperado</div><div class="benefit-text">{esc(q.get('beneficio_esperado',''))}</div></div>
    <div class="price-box"><div class="price-label">Inversión</div><div class="price-value">{esc(fmt_range(q))}</div>
    {'<div style="font-size:10px;color:#6B7280;margin-top:2px;">+ USD ' + str(q.get('fee_mensual_usd','')) + '/mes infraestructura</div>' if q.get('requiere_infraestructura') and q.get('fee_mensual_usd') else ''}</div>
  </div>
</div>""" for i,q in enumerate(qw_ops[:2]))
s6_body = f'<div class="qw-grid">{qwcards_html}</div>'
slides_html.append(slide_wrapper(6,'Quick Wins','Por dónde empezar: alto impacto, baja fricción',s6_body))

# Slide 7: Hoja de ruta
fase_colors = ['#10B981','#0C1A2E','#F59E0B']
fases_html = ''
for i,fase in enumerate(FASES):
    col = fase_colors[i % len(fase_colors)]
    fops = [o for o in OPS if o['id'] in (fase.get('oportunidades_ids') or [])]
    fops_html = ''.join(f'<div class="fase-op"><div class="fase-op-title">{esc(o.get("titulo",""))}</div><div class="fase-op-price">{esc(fmt_range(o))}</div></div>' for o in fops)
    fases_html += f'<div class="fase-col"><div class="fase-header" style="background:{col};">{esc(fase.get("fase",""))}</div><div class="fase-body"><div class="fase-desc">{esc(fase.get("descripcion",""))}</div>{fops_html}</div></div>'
total_bar = f'<div style="background:#0C1A2E;border-radius:6px;padding:12px 20px;margin-top:14px;display:flex;justify-content:space-between;"><span style="font-weight:bold;font-size:14px;color:#FFF;">Valor total del roadmap: {esc(fmt(PROP.get("total_roadmap_usd")))}</span><span style="font-size:12px;color:#6B7280;">{len(OPS)} iniciativas · {len(FASES)} fases</span></div>'
s7_body = f'<div class="roadmap-grid">{fases_html}</div>{total_bar}'
slides_html.append(slide_wrapper(7,'Hoja de ruta — Ciclo 2','Diseño e implementación: de la oportunidad a la solución en producción',s7_body))

# Slide 8: Propuesta
entry_html = ''
if entrada_op:
    entry_html = f"""<div class="entry-grid">
  <div class="entry-card">
    <div class="entry-title">⚡ {esc(entrada_op.get('titulo',''))}</div>
    <div class="entry-desc">{esc(entrada_op.get('descripcion',''))}</div>
  </div>
  <div class="price-panel">
    <div style="font-size:10px;color:#6B7280;margin-bottom:4px;">Inversión</div>
    <div style="font-size:22px;font-weight:bold;color:#F59E0B;">{esc(fmt_range(entrada_op))}</div>
    {'<div style="font-size:10px;color:#6B7280;margin-top:4px;">+ USD ' + str(entrada_op.get('fee_mensual_usd','')) + '/mes infra.</div>' if entrada_op.get('requiere_infraestructura') and entrada_op.get('fee_mensual_usd') else ''}
    <div style="font-size:10px;color:#10B981;margin-top:8px;">✅ 1 mes de garantía</div>
  </div>
</div>
<div class="payment-row"><strong>Estructura de pago:</strong> Upfront al confirmar + saldo a la entrega final. Solo pagas el total cuando ves el resultado funcionando.</div>"""
s8_body = f"""
<div class="propuesta-anchor">
  <div><div class="propuesta-anchor-label">Valor total del roadmap completo (referencia)</div>
  <div class="propuesta-anchor-value">{esc(fmt(PROP.get('total_roadmap_usd')))}</div></div>
  <span class="badge">{len(OPS)} iniciativas · {len(FASES)} fases</span>
</div>
<div class="arrow-down">↓ Iniciativa de entrada sugerida</div>
{entry_html}"""
slides_html.append(slide_wrapper(8,'Propuesta comercial','Cómo avanzar juntos al Ciclo 2',s8_body))

# Slide 9: Próximos pasos
ns_items = [
    ('📄','Hoy','Recibes el documento completo','Te enviamos el PDF con todo el análisis para que puedas revisarlo y compartirlo con tu equipo.'),
    ('✅','Tú decides','Nos dices cómo seguir','Qué cambiarías, qué esperabas ver, qué iniciativas quieres perseguir.'),
    ('💳','Primer pago','Arrancamos el Ciclo 2','Entendimiento → Diseño → Validación → Construcción → Pruebas → Ajustes → Implementación → Garantía 1 mes.'),
    ('🚀','Resultado','Solución en producción','La solución queda funcionando en tu empresa. El saldo se paga a la entrega.'),
]
ns_html = ''.join(f"""<div class="ns-card">
  <div class="ns-card-top"></div>
  <div class="ns-badge">{label}</div>
  <div class="ns-icon">{icon}</div>
  <div class="ns-title">{title}</div>
  <div class="ns-desc">{desc}</div>
</div>""" for icon,label,title,desc in ns_items)
cta = PER.get('cta_sugerido', f'¿Cuándo hablamos para resolver tus preguntas sobre {empresa}?')
contact_str = ' · '.join(filter(None,[M.get('consultor'), M.get('consultor_email'), M.get('consultor_whatsapp')]))
s9_body = f"""<div class="next-steps">{ns_html}</div>
<div class="cta-bar">
  <div class="cta-text">{esc(cta)}</div>
  <div class="cta-contact">{esc(contact_str)}</div>
</div>"""
slides_html.append(slide_wrapper(9,'Próximos pasos','¿Cómo avanzamos?',s9_body))

# Navigation
nav_links = ''.join(f'<a href="#slide-{i+1}">{i+1}. {title}</a>' for i,(title) in enumerate(['Portada','Metodología','Empresa hoy','Problemas','Oportunidades','Quick Wins','Hoja de ruta','Propuesta','Próximos pasos']))

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Diagnóstico de Oportunidades de IA — {esc(empresa)}</title>
<style>{CSS}</style>
</head>
<body>
<nav>
  <span class="brand">NEXOSTRAT</span>
  {nav_links}
</nav>
{''.join(slides_html)}
<div style="text-align:center;padding:40px;color:#6B7280;font-size:12px;">Nexostrat · {esc(fecha)} · nexostrat.co</div>
</body>
</html>"""

with open(out_file, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✓ HTML presentación: {out_file}")
