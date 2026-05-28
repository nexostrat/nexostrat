#!/usr/bin/env node
// generate_pptx.js — Nexostrat Client Deliverables
// Usage: node generate_pptx.js data_empresa.json [output_dir]
// Requires: npm install -g pptxgenjs

const PptxGenJS = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const dataFile = process.argv[2];
const outputDir = process.argv[3] || '.';
if (!dataFile) { console.error('Usage: node generate_pptx.js data_empresa.json [output_dir]'); process.exit(1); }

const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const { metadata: M, empresa_hoy: E, problemas: PROB, oportunidades: OPS, quick_wins: QW,
        roadmap_fases: FASES, propuesta: PROP, persuasion: PER } = d;

// ── Brand colors
const NAVY   = '0C1A2E';
const GREEN  = '10B981';
const AMBER  = 'F59E0B';
const WHITE  = 'FFFFFF';
const LGRAY  = 'F5F5F5';
const DGRAY  = '1F2937';
const MGRAY  = '6B7280';
const BGRAY  = 'D1D5DB';
const RED    = 'DC2626';
// Solid tint alternatives — pptxgenjs ignores alpha (8-digit hex); use these solid equivalents instead
const NAVY_PALE  = 'F0FBFF';  // replaces ${NAVY}12/15/20 — very light navy bg
const NAVY_TINT  = 'E0F2FE';  // replaces ${NAVY}30 — slightly more visible navy border/bg
const GREEN_PALE = 'ECFDF5';  // replaces ${GREEN}0D/15 — very light green bg
const AMBER_PALE = 'FFFBEB';  // replaces ${AMBER}18 — very light amber bg
const AMBER_DARK = 'B45309';  // dark amber for text on light bg
const RED_PALE   = 'FEF2F2';  // light red bg

// ── Helpers
const fecha = M.fecha_display || M.fecha_iso || '';
const empresa = M.empresa || 'Empresa';
const slug = M.empresa_slug || empresa.replace(/\s+/g, '');
const dateStr = M.fecha_iso ? M.fecha_iso.replace(/-/g, '') : new Date().toISOString().slice(0,10).replace(/-/g,'');
const outFile = path.join(outputDir, `${slug}_Diagnostico_Presentacion_${dateStr}.pptx`);

function qwOps() { return QW.map(id => OPS.find(o => o.id === id)).filter(Boolean); }
function allOps() { return OPS; }
function fmt(n) { return n ? `USD ${n.toLocaleString('en-US')}` : ''; }
function fmtRange(o) {
  if (!o) return '';
  if (o.precio_usd_max) return `USD ${o.precio_usd_min.toLocaleString('en-US')} – ${o.precio_usd_max.toLocaleString('en-US')}`;
  return `USD ${o.precio_usd_min.toLocaleString('en-US')}`;
}

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE'; // 13.33" x 7.5"
const W = 13.33, H = 7.5;

// ── Shared elements
function addHeader(slide, title, subtitle) {
  // Navy top bar
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: 0.55, fill: { color: NAVY } });
  // Nexostrat brand in bar
  slide.addText('NEXOSTRAT', { x: 0.3, y: 0, w: 3, h: 0.55, fontSize: 11, bold: true, color: WHITE, valign: 'middle' });
  // Slide title
  if (title) slide.addText(title, { x: 0.45, y: 0.7, w: W - 0.9, h: 0.65, fontSize: 28, bold: true, color: NAVY, fontFace: 'Inter' });
  // Subtitle
  if (subtitle) slide.addText(subtitle, { x: 0.45, y: 1.35, w: W - 0.9, h: 0.35, fontSize: 13, color: MGRAY, fontFace: 'Inter' });
  // Light footer bar
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: H - 0.35, w: W, h: 0.35, fill: { color: BGRAY } });
  slide.addText(`${empresa} · ${fecha}`, { x: 0.3, y: H - 0.35, w: 6, h: 0.35, fontSize: 9, color: MGRAY, valign: 'middle' });
  slide.addText('nexostrat.co', { x: W - 3, y: H - 0.35, w: 2.7, h: 0.35, fontSize: 9, color: MGRAY, align: 'right', valign: 'middle' });
}

function contentTop() { return 1.85; }

// ─────────────────────────────────────────────
// SLIDE 1 — PORTADA
// ─────────────────────────────────────────────
const s1 = pptx.addSlide();
s1.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: NAVY } });
// Green accent left bar
s1.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.25, h: H, fill: { color: GREEN } });
// Company name (amber, large)
s1.addText(empresa.toUpperCase(), { x: 0.6, y: 1.5, w: W - 1.2, h: 0.8, fontSize: 32, bold: true, color: AMBER, fontFace: 'Inter' });
// Main title
s1.addText('Diagnóstico de\nOportunidades de IA', { x: 0.6, y: 2.4, w: W - 1.2, h: 1.6, fontSize: 42, bold: true, color: WHITE, fontFace: 'Inter', lineSpacingMultiple: 1.2 });
// Divider
s1.addShape(pptx.ShapeType.rect, { x: 0.6, y: 4.15, w: 2.5, h: 0.04, fill: { color: GREEN } });
// Subtitle
s1.addText('Ciclo 1 — Resultados del Diagnóstico', { x: 0.6, y: 4.25, w: W - 1.2, h: 0.4, fontSize: 14, color: LGRAY, fontFace: 'Inter' });
// Date + consultant
s1.addText(`Preparado por ${M.consultor || 'Nexostrat'} · ${fecha}`, { x: 0.6, y: 4.75, w: W - 1.2, h: 0.35, fontSize: 12, color: MGRAY, fontFace: 'Inter' });
// Contact
const contactLine = [M.consultor_email, M.consultor_whatsapp].filter(Boolean).join('  ·  ');
if (contactLine) s1.addText(contactLine, { x: 0.6, y: 5.15, w: W - 1.2, h: 0.3, fontSize: 11, color: MGRAY, fontFace: 'Inter' });

// ─────────────────────────────────────────────
// SLIDE 2 — METODOLOGÍA
// ─────────────────────────────────────────────
const s2 = pptx.addSlide();
addHeader(s2, 'Cómo llegamos a estas conclusiones', 'Metodología del diagnóstico');

const steps = [
  { num: '1', title: 'Análisis de empresa', desc: 'Perfil, financieros, tecnología actual, posición en el mercado' },
  { num: '2', title: 'Análisis de industria', desc: 'Tendencias del sector, adopción de IA, benchmarks y oportunidades' },
  { num: '3', title: 'Análisis competitivo', desc: 'Qué están haciendo los competidores, brechas y diferenciadores' },
  { num: '4', title: 'Llamada de descubrimiento', desc: 'Conversación directa para entender dolores, operación y visión' },
];

const stepW = (W - 1.0) / 4;
steps.forEach((st, i) => {
  const x = 0.5 + i * (stepW + 0.0);
  const y = contentTop();
  // Card background
  s2.addShape(pptx.ShapeType.rect, { x, y, w: stepW - 0.1, h: 3.5, fill: { color: LGRAY }, line: { color: BGRAY, width: 1 } });
  // Number circle
  s2.addShape(pptx.ShapeType.ellipse, { x: x + (stepW - 0.1) / 2 - 0.3, y: y + 0.25, w: 0.6, h: 0.6, fill: { color: NAVY } });
  s2.addText(st.num, { x: x + (stepW - 0.1) / 2 - 0.3, y: y + 0.25, w: 0.6, h: 0.6, fontSize: 16, bold: true, color: WHITE, align: 'center', valign: 'middle' });
  // Title
  s2.addText(st.title, { x: x + 0.15, y: y + 1.05, w: stepW - 0.35, h: 0.55, fontSize: 13, bold: true, color: NAVY, align: 'center', wrap: true });
  // Desc
  s2.addText(st.desc, { x: x + 0.15, y: y + 1.65, w: stepW - 0.35, h: 1.6, fontSize: 10.5, color: DGRAY, align: 'center', wrap: true, valign: 'top' });
  // Arrow between steps
  if (i < 3) {
    s2.addText('→', { x: x + stepW - 0.18, y: y + 1.5, w: 0.25, h: 0.4, fontSize: 18, color: GREEN, align: 'center', bold: true });
  }
});

// Bottom note
s2.addText('Estos cuatro pasos nos permiten llegar con el contexto necesario para hacer recomendaciones específicas para tu empresa — no genéricas.',
  { x: 0.5, y: contentTop() + 3.65, w: W - 1.0, h: 0.4, fontSize: 10, color: MGRAY, italic: true });

// ─────────────────────────────────────────────
// SLIDE 3 — TU EMPRESA HOY
// ─────────────────────────────────────────────
const s3 = pptx.addSlide();
addHeader(s3, 'Tu empresa hoy', empresa);

// Left column: description
const leftW = (W - 1.2) * 0.55;
const rightW = (W - 1.2) * 0.42;
const leftX = 0.45, rightX = leftX + leftW + 0.15;
const topY = contentTop();

s3.addText(E.descripcion || '', { x: leftX, y: topY, w: leftW, h: 2.8, fontSize: 11.5, color: DGRAY, wrap: true, valign: 'top', fontFace: 'Inter' });

// Right column: key metrics cards
const metrics = E.metricas_clave || [];
metrics.slice(0, 5).forEach((m, i) => {
  const cardY = topY + i * 0.56;
  s3.addShape(pptx.ShapeType.rect, { x: rightX, y: cardY, w: rightW, h: 0.48, fill: { color: LGRAY }, line: { color: BGRAY, width: 1 } });
  s3.addShape(pptx.ShapeType.rect, { x: rightX, y: cardY, w: 0.04, h: 0.48, fill: { color: GREEN } });
  s3.addText(m, { x: rightX + 0.12, y: cardY, w: rightW - 0.15, h: 0.48, fontSize: 11, color: DGRAY, valign: 'middle', wrap: true });
});

// Digital maturity row
const matY = topY + 2.95;
s3.addShape(pptx.ShapeType.rect, { x: leftX, y: matY, w: leftW + rightW + 0.15, h: 0.55, fill: { color: NAVY_PALE }, line: { color: NAVY_TINT, width: 1 } });
s3.addText('Madurez digital:', { x: leftX + 0.15, y: matY, w: 1.6, h: 0.55, fontSize: 11, bold: true, color: NAVY, valign: 'middle' });
s3.addText(E.madurez_digital || '', { x: leftX + 1.75, y: matY, w: 1.2, h: 0.55, fontSize: 11, bold: true, color: GREEN, valign: 'middle' });
s3.addText(`  ${E.madurez_digital_descripcion || ''}`, { x: leftX + 2.9, y: matY, w: leftW + rightW - 2.6, h: 0.55, fontSize: 10.5, color: MGRAY, valign: 'middle', wrap: true });

// Competitive position
const posY = matY + 0.65;
s3.addText('Posición competitiva: ', { x: leftX, y: posY, w: 2.2, h: 0.4, fontSize: 11, bold: true, color: NAVY, valign: 'top' });
s3.addText(E.posicion_competitiva || '', { x: leftX + 2.2, y: posY, w: W - leftX - 2.5, h: 0.4, fontSize: 11, color: DGRAY, valign: 'top', wrap: true });

// ─────────────────────────────────────────────
// SLIDE 4 — PROBLEMAS
// ─────────────────────────────────────────────
const s4 = pptx.addSlide();
addHeader(s4, 'Los problemas que encontramos', 'Lo que identificamos en el análisis y confirmamos en nuestra conversación');

const topY4 = contentTop();
const probsToShow = PROB.slice(0, 4);
const probW = (W - 1.0) / Math.min(probsToShow.length, 4);

probsToShow.forEach((p, i) => {
  const x = 0.5 + i * probW;
  const y = topY4;
  const cw = probW - 0.12;

  // Card
  s4.addShape(pptx.ShapeType.rect, { x, y, w: cw, h: 3.7, fill: { color: WHITE }, line: { color: BGRAY, width: 1 } });
  // Red accent top
  s4.addShape(pptx.ShapeType.rect, { x, y, w: cw, h: 0.06, fill: { color: RED } });
  // Problem number
  s4.addText(`#${i + 1}`, { x: x + 0.12, y: y + 0.15, w: 0.4, h: 0.35, fontSize: 14, bold: true, color: RED });
  // Title
  s4.addText(p.titulo || '', { x: x + 0.12, y: y + 0.15, w: cw - 0.25, h: 0.5, fontSize: 12, bold: true, color: DGRAY, wrap: true, valign: 'top' });
  // Description
  s4.addText(p.descripcion || '', { x: x + 0.12, y: y + 0.72, w: cw - 0.25, h: 0.85, fontSize: 10, color: DGRAY, wrap: true, valign: 'top' });

  // Client quote box
  if (p.cita_cliente) {
    s4.addShape(pptx.ShapeType.rect, { x: x + 0.08, y: y + 1.65, w: cw - 0.17, h: 0.9, fill: { color: NAVY_PALE }, line: { color: NAVY_TINT, width: 1 } });
    s4.addText(`"${p.cita_cliente}"`, { x: x + 0.14, y: y + 1.68, w: cw - 0.28, h: 0.84, fontSize: 9.5, color: NAVY, italic: true, wrap: true, valign: 'middle' });
  }

  // Cost of inaction
  if (p.costo_inaccion) {
    s4.addShape(pptx.ShapeType.rect, { x: x + 0.08, y: y + 2.65, w: cw - 0.17, h: 0.75, fill: { color: AMBER_PALE }, line: { color: AMBER, width: 1 } });
    s4.addText('⏱ Costo de no actuar', { x: x + 0.14, y: y + 2.68, w: cw - 0.28, h: 0.22, fontSize: 8.5, bold: true, color: AMBER_DARK, wrap: false });
    s4.addText(p.costo_inaccion.descripcion || '', { x: x + 0.14, y: y + 2.9, w: cw - 0.28, h: 0.45, fontSize: 9, color: DGRAY, wrap: true, valign: 'top' });
  }
});

// ─────────────────────────────────────────────
// SLIDE 5 — OPORTUNIDADES DE IA
// ─────────────────────────────────────────────
const s5 = pptx.addSlide();
addHeader(s5, 'Las oportunidades de IA', `Identificamos ${OPS.length} oportunidades específicas para ${empresa}`);

const topY5 = contentTop();
const opsShow = OPS.slice(0, 6);
const cols = 3, rows = Math.ceil(opsShow.length / cols);
const opW = (W - 1.0) / cols;
const opH = (H - topY5 - 0.55) / rows;

opsShow.forEach((op, i) => {
  const col = i % cols, row = Math.floor(i / cols);
  const x = 0.5 + col * opW;
  const y = topY5 + row * opH;
  const cw = opW - 0.12, ch = opH - 0.1;
  const isQW = QW.includes(op.id);

  s5.addShape(pptx.ShapeType.rect, { x, y, w: cw, h: ch, fill: { color: isQW ? GREEN_PALE : LGRAY }, line: { color: isQW ? GREEN : BGRAY, width: isQW ? 2 : 1 } });
  // Colored left accent
  s5.addShape(pptx.ShapeType.rect, { x, y, w: 0.04, h: ch, fill: { color: isQW ? GREEN : NAVY } });
  // Quick Win badge
  if (isQW) s5.addText('⚡ Quick Win', { x: x + cw - 1.1, y: y + 0.08, w: 1.0, h: 0.22, fontSize: 8, bold: true, color: GREEN, align: 'right' });
  // Title
  s5.addText(op.titulo || '', { x: x + 0.12, y: y + 0.08, w: cw - (isQW ? 1.25 : 0.2), h: 0.35, fontSize: 11, bold: true, color: NAVY, wrap: true });
  // Area
  s5.addText(op.area || '', { x: x + 0.12, y: y + 0.42, w: cw - 0.2, h: 0.2, fontSize: 9, color: MGRAY });
  // Description
  s5.addText(op.descripcion || '', { x: x + 0.12, y: y + 0.62, w: cw - 0.2, h: ch - 1.05, fontSize: 9.5, color: DGRAY, wrap: true, valign: 'top' });
  // Price
  s5.addText(fmtRange(op), { x: x + 0.12, y: y + ch - 0.32, w: cw - 0.2, h: 0.28, fontSize: 9.5, bold: true, color: isQW ? GREEN : NAVY });
});

// ─────────────────────────────────────────────
// SLIDE 6 — QUICK WINS
// ─────────────────────────────────────────────
const s6 = pptx.addSlide();
addHeader(s6, 'Quick Wins', 'Por dónde empezar: alto impacto, baja fricción');

const qwList = qwOps();
const topY6 = contentTop();
const qwW = (W - 1.2) / 2;

qwList.slice(0, 2).forEach((qw, i) => {
  const x = 0.45 + i * (qwW + 0.1);
  const y = topY6;

  s6.addShape(pptx.ShapeType.rect, { x, y, w: qwW, h: 4.5, fill: { color: GREEN_PALE }, line: { color: GREEN, width: 2 } });
  // Header bar
  s6.addShape(pptx.ShapeType.rect, { x, y, w: qwW, h: 0.5, fill: { color: GREEN } });
  s6.addText(`⚡ Quick Win ${i + 1}`, { x: x + 0.15, y, w: qwW - 0.3, h: 0.5, fontSize: 13, bold: true, color: WHITE, valign: 'middle' });
  // Title
  s6.addText(qw.titulo || '', { x: x + 0.15, y: y + 0.6, w: qwW - 0.3, h: 0.55, fontSize: 15, bold: true, color: NAVY, wrap: true });
  // Area
  s6.addText(qw.area || '', { x: x + 0.15, y: y + 1.18, w: qwW - 0.3, h: 0.25, fontSize: 10, color: MGRAY });
  // Description
  s6.addText(qw.descripcion || '', { x: x + 0.15, y: y + 1.48, w: qwW - 0.3, h: 1.2, fontSize: 10.5, color: DGRAY, wrap: true, valign: 'top' });
  // Benefit
  s6.addShape(pptx.ShapeType.rect, { x: x + 0.12, y: y + 2.75, w: qwW - 0.24, h: 0.7, fill: { color: WHITE }, line: { color: BGRAY, width: 1 } });
  s6.addText('Beneficio esperado:', { x: x + 0.2, y: y + 2.78, w: qwW - 0.4, h: 0.22, fontSize: 9, bold: true, color: GREEN });
  s6.addText(qw.beneficio_esperado || '', { x: x + 0.2, y: y + 2.99, w: qwW - 0.4, h: 0.42, fontSize: 9.5, color: DGRAY, wrap: true });
  // Price
  s6.addShape(pptx.ShapeType.rect, { x: x + 0.12, y: y + 3.55, w: qwW - 0.24, h: 0.65, fill: { color: NAVY } });
  s6.addText('Inversión:', { x: x + 0.2, y: y + 3.58, w: 1.2, h: 0.28, fontSize: 9.5, bold: true, color: LGRAY });
  s6.addText(fmtRange(qw), { x: x + 0.2, y: y + 3.82, w: qwW - 0.4, h: 0.3, fontSize: 13, bold: true, color: AMBER });
  if (qw.requiere_infraestructura && qw.fee_mensual_usd) {
    s6.addText(`+ USD ${qw.fee_mensual_usd}/mes infraestructura`, { x: x + 0.2, y: y + 3.82, w: qwW - 0.4, h: 0.3, fontSize: 8.5, color: LGRAY, align: 'right' });
  }
});

// ─────────────────────────────────────────────
// SLIDE 7 — HOJA DE RUTA
// ─────────────────────────────────────────────
const s7 = pptx.addSlide();
addHeader(s7, 'Hoja de ruta — Ciclo 2', 'Diseño e implementación: de la oportunidad a la solución en producción');

const topY7 = contentTop();
const faseColors = [GREEN, NAVY, AMBER];
const faseW = (W - 1.0) / Math.max(FASES.length, 1);

FASES.forEach((fase, i) => {
  const x = 0.5 + i * faseW;
  const y = topY7;
  const cw = faseW - 0.12;
  const col = faseColors[i % faseColors.length];

  // Phase header
  s7.addShape(pptx.ShapeType.rect, { x, y, w: cw, h: 0.45, fill: { color: col } });
  s7.addText(fase.fase || `Fase ${i + 1}`, { x: x + 0.1, y, w: cw - 0.2, h: 0.45, fontSize: 11, bold: true, color: WHITE, valign: 'middle', wrap: true });
  // Card
  s7.addShape(pptx.ShapeType.rect, { x, y: y + 0.45, w: cw, h: 3.5, fill: { color: LGRAY }, line: { color: BGRAY, width: 1 } });
  // Description
  s7.addText(fase.descripcion || '', { x: x + 0.1, y: y + 0.55, w: cw - 0.2, h: 0.65, fontSize: 10, color: MGRAY, italic: true, wrap: true });
  // Initiatives
  const faseOps = (fase.oportunidades_ids || []).map(id => OPS.find(o => o.id === id)).filter(Boolean);
  faseOps.forEach((op, j) => {
    const oy = y + 1.3 + j * 0.6;
    s7.addShape(pptx.ShapeType.rect, { x: x + 0.1, y: oy, w: cw - 0.2, h: 0.52, fill: { color: WHITE }, line: { color: BGRAY, width: 1 } });
    s7.addShape(pptx.ShapeType.rect, { x: x + 0.1, y: oy, w: 0.04, h: 0.52, fill: { color: col } });
    s7.addText(op.titulo || '', { x: x + 0.2, y: oy + 0.03, w: cw - 0.35, h: 0.26, fontSize: 10, bold: true, color: DGRAY, wrap: false });
    s7.addText(fmtRange(op), { x: x + 0.2, y: oy + 0.28, w: cw - 0.35, h: 0.2, fontSize: 9, color: col, bold: true });
  });
  // Arrow
  if (i < FASES.length - 1) {
    s7.addText('→', { x: x + cw + 0.0, y: y + 1.8, w: 0.15, h: 0.4, fontSize: 18, bold: true, color: MGRAY, align: 'center' });
  }
});

// Total
s7.addShape(pptx.ShapeType.rect, { x: 0.5, y: topY7 + 4.1, w: W - 1.0, h: 0.45, fill: { color: NAVY } });
s7.addText(`Valor total del roadmap: ${fmt(PROP.total_roadmap_usd)}`, { x: 0.6, y: topY7 + 4.1, w: 6, h: 0.45, fontSize: 13, bold: true, color: WHITE, valign: 'middle' });
s7.addText(`${OPS.length} iniciativas · ${FASES.length} fases`, { x: W - 4.5, y: topY7 + 4.1, w: 4.0, h: 0.45, fontSize: 11, color: LGRAY, valign: 'middle', align: 'right' });

// ─────────────────────────────────────────────
// SLIDE 8 — PROPUESTA COMERCIAL
// ─────────────────────────────────────────────
const s8 = pptx.addSlide();
addHeader(s8, 'Propuesta comercial', 'Cómo avanzar juntos al Ciclo 2');

const topY8 = contentTop();
const entradaOp = OPS.find(o => o.id === PROP.iniciativa_entrada_id) || qwOps()[0];

// Anchor: total roadmap value
s8.addShape(pptx.ShapeType.rect, { x: 0.45, y: topY8, w: W - 0.9, h: 0.7, fill: { color: NAVY_PALE }, line: { color: NAVY_TINT, width: 1 } });
s8.addText('Valor total del roadmap completo (referencia):', { x: 0.6, y: topY8 + 0.05, w: 5.5, h: 0.3, fontSize: 10, color: MGRAY });
s8.addText(fmt(PROP.total_roadmap_usd), { x: 0.6, y: topY8 + 0.32, w: 4, h: 0.33, fontSize: 20, bold: true, color: NAVY });
s8.addText(`${OPS.length} iniciativas · ${FASES.length} fases`, { x: 4.8, y: topY8 + 0.38, w: 4, h: 0.25, fontSize: 10, color: MGRAY });

// Arrow down
s8.addText('↓ Iniciativa de entrada sugerida', { x: 0.45, y: topY8 + 0.78, w: W - 0.9, h: 0.3, fontSize: 11, color: GREEN, bold: true });

// Entry initiative highlight
if (entradaOp) {
  s8.addShape(pptx.ShapeType.rect, { x: 0.45, y: topY8 + 1.12, w: (W - 0.9) * 0.55, h: 1.5, fill: { color: GREEN_PALE }, line: { color: GREEN, width: 2 } });
  s8.addText('⚡ ' + (entradaOp.titulo || ''), { x: 0.6, y: topY8 + 1.18, w: (W - 0.9) * 0.55 - 0.25, h: 0.4, fontSize: 14, bold: true, color: NAVY, wrap: true });
  s8.addText(entradaOp.descripcion || '', { x: 0.6, y: topY8 + 1.62, w: (W - 0.9) * 0.55 - 0.25, h: 0.55, fontSize: 10, color: DGRAY, wrap: true });
  // Price
  const priceX = 0.45 + (W - 0.9) * 0.55 + 0.15;
  const priceW = (W - 0.9) * 0.42;
  s8.addShape(pptx.ShapeType.rect, { x: priceX, y: topY8 + 1.12, w: priceW, h: 1.5, fill: { color: NAVY } });
  s8.addText('Inversión', { x: priceX + 0.15, y: topY8 + 1.2, w: priceW - 0.3, h: 0.3, fontSize: 11, color: LGRAY, bold: true });
  s8.addText(fmtRange(entradaOp), { x: priceX + 0.15, y: topY8 + 1.52, w: priceW - 0.3, h: 0.45, fontSize: 20, bold: true, color: AMBER });
  if (entradaOp.requiere_infraestructura && entradaOp.fee_mensual_usd) {
    s8.addText(`+ USD ${entradaOp.fee_mensual_usd}/mes infraestructura`, { x: priceX + 0.15, y: topY8 + 1.97, w: priceW - 0.3, h: 0.25, fontSize: 9, color: LGRAY });
  }
  s8.addText('1 mes de garantía incluido', { x: priceX + 0.15, y: topY8 + 2.22, w: priceW - 0.3, h: 0.25, fontSize: 9, color: GREEN });
}

// Payment structure
s8.addShape(pptx.ShapeType.rect, { x: 0.45, y: topY8 + 2.75, w: W - 0.9, h: 0.6, fill: { color: LGRAY }, line: { color: BGRAY, width: 1 } });
s8.addText('Estructura de pago:', { x: 0.6, y: topY8 + 2.78, w: 2.2, h: 0.28, fontSize: 10.5, bold: true, color: NAVY });
s8.addText('Upfront al confirmar  +  Saldo a la entrega final.  Solo pagas el total cuando ves el resultado funcionando.', { x: 2.85, y: topY8 + 2.82, w: W - 3.3, h: 0.5, fontSize: 10.5, color: DGRAY, wrap: true });

// ─────────────────────────────────────────────
// SLIDE 9 — PRÓXIMOS PASOS
// ─────────────────────────────────────────────
const s9 = pptx.addSlide();
addHeader(s9, 'Próximos pasos', '¿Cómo avanzamos?');

const topY9 = contentTop();
const steps9 = [
  { icon: '📄', label: 'Hoy', title: 'Recibes el documento completo', desc: 'Te enviamos el PDF con todo el análisis para que puedas revisarlo con calma, compartirlo con tu equipo y resolver cualquier pregunta.' },
  { icon: '✅', label: 'Tú decides', title: 'Nos dices cómo seguir', desc: 'Qué cambiarías, qué esperabas ver, qué iniciativas quieres perseguir. Una vez tomas tu decisión, nos informas.' },
  { icon: '💳', label: 'Primer pago', title: 'Arrancamos el Ciclo 2', desc: 'Con el upfront confirmado iniciamos: Entendimiento → Diseño → Validación → Construcción → Pruebas → Ajustes → Implementación → Garantía 1 mes.' },
  { icon: '🚀', label: 'Resultado', title: 'Solución en producción', desc: 'La solución queda funcionando en tu empresa. El equipo la usa desde el día uno. El saldo se paga a la entrega.' },
];

const stepW9 = (W - 1.0) / 4;
steps9.forEach((st, i) => {
  const x = 0.5 + i * stepW9;
  const y = topY9;
  const cw = stepW9 - 0.12;

  s9.addShape(pptx.ShapeType.rect, { x, y, w: cw, h: 3.6, fill: { color: LGRAY }, line: { color: BGRAY, width: 1 } });
  // Top colored bar
  s9.addShape(pptx.ShapeType.rect, { x, y, w: cw, h: 0.04, fill: { color: GREEN } });
  // Step label chip
  s9.addShape(pptx.ShapeType.rect, { x: x + 0.12, y: y + 0.15, w: 1.0, h: 0.27, fill: { color: NAVY_PALE }, line: { color: NAVY_TINT, width: 1 } });
  s9.addText(st.label, { x: x + 0.12, y: y + 0.15, w: 1.0, h: 0.27, fontSize: 9, bold: true, color: NAVY, align: 'center', valign: 'middle' });
  // Icon
  s9.addText(st.icon, { x: x + (cw - 0.55) / 2, y: y + 0.55, w: 0.55, h: 0.5, fontSize: 22, align: 'center' });
  // Title
  s9.addText(st.title, { x: x + 0.1, y: y + 1.15, w: cw - 0.2, h: 0.5, fontSize: 11.5, bold: true, color: NAVY, align: 'center', wrap: true });
  // Desc
  s9.addText(st.desc, { x: x + 0.1, y: y + 1.75, w: cw - 0.2, h: 1.65, fontSize: 10, color: DGRAY, wrap: true, align: 'center', valign: 'top' });
  // Arrow
  if (i < 3) s9.addText('→', { x: x + cw + 0.0, y: y + 1.8, w: 0.15, h: 0.4, fontSize: 18, bold: true, color: MGRAY, align: 'center' });
});

// CTA + contact
s9.addShape(pptx.ShapeType.rect, { x: 0.45, y: topY9 + 3.75, w: W - 0.9, h: 0.65, fill: { color: NAVY } });
const ctaText = PER.cta_sugerido || `¿Cuándo hablamos para resolver tus preguntas sobre ${empresa}?`;
s9.addText(ctaText, { x: 0.6, y: topY9 + 3.78, w: W - 3.2, h: 0.6, fontSize: 12, bold: true, color: WHITE, valign: 'middle', wrap: true });
const contactStr = [M.consultor, M.consultor_email, M.consultor_whatsapp].filter(Boolean).join('  ·  ');
s9.addText(contactStr, { x: W - 5.2, y: topY9 + 3.78, w: 4.75, h: 0.6, fontSize: 10, color: LGRAY, align: 'right', valign: 'middle' });

// ─────────────────────────────────────────────
// SAVE
// ─────────────────────────────────────────────
pptx.writeFile({ fileName: outFile })
  .then(() => console.log(`✓ PPTX: ${outFile}`))
  .catch(err => { console.error('Error:', err); process.exit(1); });
