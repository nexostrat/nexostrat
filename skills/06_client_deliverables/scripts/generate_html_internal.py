#!/usr/bin/env python3
"""
generate_html_internal.py — Nexostrat Internal Briefing for Ricardo (HTML version)
Usage: python generate_html_internal.py data_empresa.json [output_dir]

Generates a self-contained HTML file that mirrors Ricardo's 1-page internal DOCX.
Confidential — do not share with client.
"""

import json
import sys
import os
from datetime import datetime
from html import escape as esc

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  font-size: 14.5px;
  line-height: 1.65;
  color: #1F2937;
  background: #0C1A2E;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px 48px;
}

.page {
  width: 100%;
  max-width: 720px;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,0,0,.5);
}

/* ── Page header ── */
.page-header {
  background: #0C1A2E;
  color: #fff;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.page-header .ph-left .brand { font-size: 18px; font-weight: 800; letter-spacing: .3px; }
.page-header .ph-left .tag {
  display: inline-block;
  background: rgba(255,255,255,.15);
  border: 1px solid rgba(255,255,255,.25);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 2px 10px;
  border-radius: 10px;
  margin-top: 4px;
}
.page-header .ph-right { text-align: right; }
.page-header .ph-right .empresa { font-size: 16px; font-weight: 700; }
.page-header .ph-right .date { font-size: 12px; opacity: .65; margin-top: 2px; }

/* ── Section block ── */
.block { border-bottom: 1px solid #F0FBFF; }
.block:last-child { border-bottom: none; }
.block-header {
  padding: 13px 24px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: .3px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.block-header.navy  { background: #0C1A2E; color: #fff; }
.block-header.green { background: #10B981; color: #fff; }
.block-header.amber { background: #FEF3C7; color: #7C3700; }
.block-header.red   { background: #FEE2E2; color: #7F1D1D; }
.block-header.blue  { background: rgba(30,58,95,.8); color: #fff; }
.block-header.lgray { background: #F5F5F5; color: #0C1A2E; border-bottom: 1px solid #D1D5DB; }
.block-body { padding: 16px 24px; }

/* ── Gancho ── */
.gancho-title {
  font-size: 20px; font-weight: 800; color: #10B981; margin-bottom: 4px;
}
.gancho-price {
  font-size: 16px; font-weight: 700; color: #10B981; margin-bottom: 10px;
}
.gancho-reason {
  font-size: 13px; color: #0D4A6B; line-height: 1.6;
}

/* ── Quote ── */
.quote-block {
  border-left: 5px solid #0C1A2E;
  padding: 12px 16px;
  background: #F0FBFF;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  font-size: 14px;
  color: #0C1A2E;
  line-height: 1.7;
}

/* ── Objection ── */
.obj-row { margin-bottom: 12px; }
.obj-row .or-label {
  font-size: 11px; font-weight: 700; color: #6B7280;
  text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px;
}
.obj-row .or-value { font-size: 13.5px; }
.obj-row .or-value.red { color: #DC2626; font-weight: 600; }

/* ── CTA ── */
.cta-text {
  font-size: 15px; font-style: italic; font-weight: 700;
  color: #10B981; line-height: 1.7;
  border-left: 5px solid #10B981;
  padding: 12px 16px;
  background: #F0FDF4;
  border-radius: 0 8px 8px 0;
}

/* ── Prices ── */
.price-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px; }
.price-card {
  background: #F5F5F5; border: 1px solid #D1D5DB;
  border-radius: 8px; padding: 12px 14px;
}
.price-card .pc-label { font-size: 10px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: .4px; margin-bottom: 3px; }
.price-card .pc-title { font-size: 13px; font-weight: 600; color: #1F2937; margin-bottom: 2px; }
.price-card .pc-amount { font-size: 18px; font-weight: 800; color: #10B981; }
.price-card.entry { border-color: #10B981; background: #F0FDF4; }
.price-card.entry .pc-amount { color: #065F46; }
.price-card.total .pc-amount { color: #0C1A2E; font-size: 20px; }
.price-card.total { border-color: #E0F2FE; background: #F0FBFF; grid-column: 1 / -1; }
.payment-row { font-size: 13px; color: #0D4A6B; margin-top: 10px; }
.payment-row strong { color: #0C1A2E; }

/* ── Signals & flags ── */
.signal-list { list-style: none; display: flex; flex-direction: column; gap: 6px; }
.signal-list li {
  font-size: 13.5px; padding: 7px 10px;
  border-radius: 6px; display: flex; align-items: flex-start; gap: 8px;
}
.signal-list li.positive { background: #F0FDF4; color: #065F46; }
.signal-list li.flag     { background: #FEF2F2; color: #7F1D1D; }
.signal-list li .bullet  { flex-shrink: 0; font-size: 14px; }

/* ── Confidential footer ── */
.conf-footer {
  background: #F5F5F5;
  border-top: 1px solid #D1D5DB;
  padding: 10px 24px;
  text-align: center;
  font-size: 11px;
  color: #6B7280;
  font-style: italic;
  letter-spacing: .2px;
}

/* ── Page wrapper label ── */
.doc-label {
  font-size: 11px; font-weight: 700; color: rgba(255,255,255,.4);
  text-transform: uppercase; letter-spacing: 1px;
  margin-bottom: 10px; text-align: center;
}
"""

def fmt_price(op):
    lo = op.get('precio_usd_min')
    hi = op.get('precio_usd_max')
    if not lo:
        return ''
    if hi:
        return f"USD {lo:,} – {hi:,}"
    return f"USD {lo:,}"

def build_html(d):
    M = d.get('metadata', {})
    OPS = d.get('oportunidades', [])
    QW = d.get('quick_wins', [])
    PROP = d.get('propuesta', {})
    PER = d.get('persuasion', {})

    empresa = esc(M.get('empresa', 'Empresa'))
    fecha = esc(M.get('fecha_display', M.get('fecha_iso', '')))

    ops_by_id = {o['id']: o for o in OPS}
    gancho_id = PER.get('quick_win_gancho_id')
    gancho_op = ops_by_id.get(gancho_id) or (
        ops_by_id.get(QW[0]) if QW else (OPS[0] if OPS else None)
    )
    segundo_id = QW[1] if len(QW) > 1 else None
    segundo_op = ops_by_id.get(segundo_id) if segundo_id else next(
        (o for o in OPS if o['id'] != (gancho_op['id'] if gancho_op else None)), None
    )

    entrada_op = ops_by_id.get(PROP.get('iniciativa_entrada_id')) or gancho_op
    total = PROP.get('total_roadmap_usd', 0)
    upfront = PROP.get('upfront_porcentaje', 50)

    parts = []

    parts.append(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Briefing Interno — {empresa}</title>
<style>{CSS}</style>
</head>
<body>
<div class="doc-label">Documento de uso interno · Nexostrat · No compartir con el cliente</div>
<div class="page">
""")

    # ── Page header ──
    parts.append(f"""
  <div class="page-header">
    <div class="ph-left">
      <div class="brand">Nexostrat</div>
      <div class="tag">Briefing Pre-Reunión</div>
    </div>
    <div class="ph-right">
      <div class="empresa">{empresa}</div>
      <div class="date">{fecha}</div>
    </div>
  </div>
""")

    # ── Block 1: Gancho principal ──
    if gancho_op:
        gancho_price = fmt_price(gancho_op)
        gancho_reason = esc(PER.get('quick_win_gancho_razon',
            'Mayor impacto / menor fricción de implementación para este cliente.'))
        parts.append(f"""
  <div class="block">
    <div class="block-header navy">▶ GANCHO PRINCIPAL — Quick Win para abrir con</div>
    <div class="block-body">
      <div class="gancho-title">{esc(gancho_op.get('titulo',''))}</div>
      <div class="gancho-price">{esc(gancho_price)}</div>
      <div class="gancho-reason"><strong>Por qué este primero:</strong> {gancho_reason}</div>
    </div>
  </div>
""")

    # ── Block 2: Cita del cliente ──
    cita = PER.get('cita_principal', '')
    if cita:
        parts.append(f"""
  <div class="block">
    <div class="block-header blue">💬 CITA DEL CLIENTE A USAR</div>
    <div class="block-body">
      <div class="quote-block">"{esc(cita)}"</div>
    </div>
  </div>
""")

    # ── Block 3: Objeción ──
    parts.append(f"""
  <div class="block">
    <div class="block-header amber">⚠️ OBJECIÓN MÁS PROBABLE</div>
    <div class="block-body">
      <div class="obj-row">
        <div class="or-label">Objeción</div>
        <div class="or-value red">{esc(PER.get('objecion_probable','Presupuesto o tiempo.'))}</div>
      </div>
      <div class="obj-row">
        <div class="or-label">Respuesta sugerida</div>
        <div class="or-value">{esc(PER.get('respuesta_objecion',
            'Empezar con el Quick Win de menor inversión para demostrar ROI antes de comprometerse con el roadmap completo.'))}</div>
      </div>
    </div>
  </div>
""")

    # ── Block 4: CTA ──
    cta = PER.get('cta_sugerido', '')
    if not cta and gancho_op:
        cta = f"¿Quieres que avancemos con {gancho_op.get('titulo','')}? Puedo enviarte la propuesta formal hoy mismo."
    parts.append(f"""
  <div class="block">
    <div class="block-header green">🎯 CTA SUGERIDO PARA EL CIERRE</div>
    <div class="block-body">
      <div class="cta-text">"{esc(cta)}"</div>
    </div>
  </div>
""")

    # ── Block 5: Precios ──
    entrada_title = esc(entrada_op.get('titulo','')) if entrada_op else ''
    entrada_price = esc(fmt_price(entrada_op)) if entrada_op else ''
    fee_line = ''
    if entrada_op and entrada_op.get('requiere_infraestructura') and entrada_op.get('fee_mensual_usd'):
        fee_line = f'<div style="font-size:11px;color:#065F46;margin-top:2px;">+ USD {entrada_op["fee_mensual_usd"]:,}/mes infra</div>'
    segundo_html = ''
    if segundo_op:
        parts_segundo = f"""
        <div class="price-card">
          <div class="pc-label">Siguiente natural</div>
          <div class="pc-title">{esc(segundo_op.get('titulo',''))}</div>
          <div class="pc-amount" style="color:#6B7280;">{esc(fmt_price(segundo_op))}</div>
        </div>"""
        segundo_html = parts_segundo

    parts.append(f"""
  <div class="block">
    <div class="block-header lgray">💰 RESUMEN DE PRECIOS</div>
    <div class="block-body">
      <div class="price-grid">
        <div class="price-card total">
          <div class="pc-label">Total roadmap ({len(OPS)} iniciativas)</div>
          <div class="pc-amount">USD {total:,}</div>
        </div>
        <div class="price-card entry">
          <div class="pc-label">Iniciativa de entrada</div>
          <div class="pc-title">{entrada_title}</div>
          <div class="pc-amount">{entrada_price}</div>
          {fee_line}
        </div>
        {segundo_html}
      </div>
      <div class="payment-row">
        <strong>Estructura:</strong> {upfront}% upfront al confirmar + {100-upfront}% a la entrega final
      </div>
    </div>
  </div>
""")

    # ── Block 6: Señales positivas ──
    signals = PER.get('senales_positivas', [])
    if signals:
        items_html = ''.join(
            f'<li class="positive"><span class="bullet">✅</span>{esc(s)}</li>'
            for s in signals
        )
        parts.append(f"""
  <div class="block">
    <div class="block-header green">✅ SEÑALES POSITIVAS DEL CLIENTE</div>
    <div class="block-body">
      <ul class="signal-list">{items_html}</ul>
    </div>
  </div>
""")

    # ── Block 7: Banderas ──
    flags = PER.get('banderas_atencion', [])
    if flags:
        items_html = ''.join(
            f'<li class="flag"><span class="bullet">🚩</span>{esc(f)}</li>'
            for f in flags
        )
        parts.append(f"""
  <div class="block">
    <div class="block-header red">🚩 BANDERAS DE ATENCIÓN</div>
    <div class="block-body">
      <ul class="signal-list">{items_html}</ul>
    </div>
  </div>
""")

    # ── Footer ──
    parts.append(f"""
  <div class="conf-footer">
    Documento de uso interno — Nexostrat. No compartir con el cliente.
  </div>
</div>
</body>
</html>
""")

    return ''.join(parts)


def main():
    if len(sys.argv) < 2:
        print('Usage: python generate_html_internal.py data_empresa.json [output_dir]')
        sys.exit(1)
    data_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    d = load_data(data_file)
    M = d.get('metadata', {})
    slug = M.get('empresa_slug', M.get('empresa', 'Empresa').replace(' ', ''))
    date_str = (M.get('fecha_iso', datetime.today().strftime('%Y-%m-%d'))).replace('-', '')
    out_file = os.path.join(output_dir, f"Ricardo_BriefingInterno_{slug}_{date_str}.html")
    html = build_html(d)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ HTML briefing interno (Ricardo): {out_file}")

if __name__ == '__main__':
    main()
