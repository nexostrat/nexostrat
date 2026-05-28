#!/usr/bin/env node
// generate_internal_docx.js — Nexostrat Internal Briefing for Ricardo
// Usage: node generate_internal_docx.js data_empresa.json [output_dir]
// Requires: npm install -g docx

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType, LevelFormat, PageBreak } = require('docx');
const fs = require('fs');
const path = require('path');

const dataFile = process.argv[2];
const outputDir = process.argv[3] || '.';
if (!dataFile) { console.error('Usage: node generate_internal_docx.js data_empresa.json [output_dir]'); process.exit(1); }

const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const { metadata: M, oportunidades: OPS, quick_wins: QW, propuesta: PROP, persuasion: PER } = d;

const empresa = M.empresa || 'Empresa';
const slug = M.empresa_slug || empresa.replace(/\s+/g, '');
const dateStr = M.fecha_iso ? M.fecha_iso.replace(/-/g,'') : new Date().toISOString().slice(0,10).replace(/-/g,'');
const outFile = path.join(outputDir, `Ricardo_BriefingInterno_${slug}_${dateStr}.docx`);

function fmt(n) { return n ? `USD ${n.toLocaleString('en-US')}` : ''; }
function fmtRange(o) {
  if (!o) return '';
  if (o.precio_usd_max) return `USD ${o.precio_usd_min.toLocaleString('en-US')} – ${o.precio_usd_max.toLocaleString('en-US')}`;
  return `USD ${o.precio_usd_min.toLocaleString('en-US')}`;
}

const NAVY = '0C1A2E', GREEN = '10B981', AMBER = 'F59E0B', LGRAY = 'F5F5F5', MGRAY = '6B7280', BGRAY = 'D1D5DB', RED = 'DC2626';
// Solid-color alternatives for sections (docx lib requires 6-digit hex, no alpha)
const NAVY_DARK = '0C1A2E';   // dark navy for "Cita" header
const AMBER_LIGHT = 'FEF3C7'; // light amber bg
const GREEN_LIGHT = 'ECFDF5'; // light green bg
const RED_LIGHT = 'FEF2F2';   // light red bg

function sectionHeader(emoji, title, bgColor, textColor) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [new TableCell({
      shading: { fill: bgColor, type: ShadingType.CLEAR },
      borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
      margins: { top: 120, bottom: 120, left: 180, right: 180 },
      children: [new Paragraph({ children: [new TextRun({ text: `${emoji}  ${title}`, font: 'Inter', size: 24, bold: true, color: textColor })] })],
    })]})],
  });
}

function bodyRow(label, value, valueColor = '1F2937', valueBold = false) {
  return new Paragraph({
    children: [
      ...(label ? [new TextRun({ text: `${label}  `, font: 'Inter', size: 21, bold: true, color: MGRAY })] : []),
      new TextRun({ text: value || '', font: 'Inter', size: 21, color: valueColor, bold: valueBold }),
    ],
    spacing: { before: 80, after: 80 },
  });
}

function indent(text, color = '1F2937') {
  return new Paragraph({
    children: [new TextRun({ text: text || '', font: 'Inter', size: 21, color })],
    numbering: { reference: 'bullets', level: 0 },
    spacing: { before: 60, after: 60 },
  });
}

function space(pt = 160) { return new Paragraph({ spacing: { before: 0, after: pt } }); }

// ── Quick Win entry
const ganchoOp = OPS.find(o => o.id === PER?.quick_win_gancho_id) || (QW.length > 0 ? OPS.find(o => o.id === QW[0]) : OPS[0]);
const segundoOp = QW.length > 1 ? OPS.find(o => o.id === QW[1]) : OPS.find(o => !QW.includes(o.id));

const children = [];

// Title
children.push(new Paragraph({
  children: [new TextRun({ text: `BRIEFING PRE-REUNIÓN`, font: 'Inter', size: 28, bold: true, color: NAVY })],
  spacing: { before: 0, after: 80 },
}));
children.push(new Paragraph({
  children: [new TextRun({ text: `${empresa}  ·  ${M.fecha_display || M.fecha_iso || ''}`, font: 'Inter', size: 22, color: MGRAY })],
  spacing: { before: 0, after: 200 },
}));
children.push(new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 1 } }, spacing: { before: 0, after: 240 } }));

// Section 1: Gancho
children.push(sectionHeader('▶', 'GANCHO PRINCIPAL — Quick Win para abrir con', NAVY, 'FFFFFF'));
children.push(space(80));
if (ganchoOp) {
  children.push(bodyRow('Iniciativa:', ganchoOp.titulo, GREEN, true));
  children.push(bodyRow('Precio:', fmtRange(ganchoOp), GREEN, true));
  children.push(bodyRow('Por qué este primero:', PER?.quick_win_gancho_razon || 'Mayor impacto / menor fricción de implementación para este cliente.', '1F2937'));
}
children.push(space(160));

// Section 2: Cita
children.push(sectionHeader('💬', 'CITA DEL CLIENTE A USAR', NAVY_DARK, 'FFFFFF'));
children.push(space(80));
if (PER?.cita_principal) {
  children.push(new Paragraph({
    children: [new TextRun({ text: `"${PER.cita_principal}"`, font: 'Inter', size: 22, italics: true, color: NAVY })],
    spacing: { before: 80, after: 60 },
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 10, color: NAVY, space: 5 } },
  }));
}
children.push(space(160));

// Section 3: Objeción
children.push(sectionHeader('⚠️', 'OBJECIÓN MÁS PROBABLE', AMBER_LIGHT, '7C3700'));
children.push(space(80));
children.push(bodyRow('Objeción:', PER?.objecion_probable || 'Presupuesto o tiempo.', RED));
children.push(space(60));
children.push(bodyRow('Respuesta sugerida:', PER?.respuesta_objecion || 'Empezar con el Quick Win de menor inversión para demostrar ROI antes de comprometerse con el roadmap completo.', '1F2937'));
children.push(space(160));

// Section 4: CTA
children.push(sectionHeader('🎯', 'CTA SUGERIDO PARA EL CIERRE', GREEN_LIGHT, '064E3B'));
children.push(space(80));
children.push(new Paragraph({
  children: [new TextRun({ text: PER?.cta_sugerido || `"¿Quieres que avancemos con ${ganchoOp?.titulo || 'el Quick Win'}? Puedo enviarte la propuesta formal hoy mismo."`, font: 'Inter', size: 22, italics: true, color: GREEN, bold: true })],
  spacing: { before: 80, after: 80 },
  indent: { left: 360 },
}));
children.push(space(160));

// Section 5: Prices
children.push(sectionHeader('💰', 'RESUMEN DE PRECIOS', `${LGRAY}`, NAVY));
children.push(space(80));
children.push(bodyRow('Total roadmap:', `${fmt(PROP?.total_roadmap_usd)}  (${OPS.length} iniciativas)`, NAVY, true));
children.push(space(60));
if (ganchoOp) children.push(bodyRow('Iniciativa de entrada:', `${ganchoOp.titulo} — ${fmtRange(ganchoOp)}${ganchoOp.requiere_infraestructura && ganchoOp.fee_mensual_usd ? ` + USD ${ganchoOp.fee_mensual_usd}/mes` : ''}`, GREEN, true));
if (segundoOp) children.push(bodyRow('Siguiente natural:', `${segundoOp.titulo} — ${fmtRange(segundoOp)}`, MGRAY));
children.push(space(80));
children.push(bodyRow('Estructura:', `${PROP?.upfront_porcentaje || 50}% upfront al confirmar + ${100 - (PROP?.upfront_porcentaje || 50)}% a la entrega final`, '1F2937'));
children.push(space(160));

// Section 6: Positive signals
if (PER?.senales_positivas?.length) {
  children.push(sectionHeader('✅', 'SEÑALES POSITIVAS DEL CLIENTE', GREEN_LIGHT, '064E3B'));
  children.push(space(80));
  PER.senales_positivas.forEach(s => children.push(indent(s, GREEN)));
  children.push(space(160));
}

// Section 7: Flags
if (PER?.banderas_atencion?.length) {
  children.push(sectionHeader('🚩', 'BANDERAS DE ATENCIÓN', RED_LIGHT, '7F1D1D'));
  children.push(space(80));
  PER.banderas_atencion.forEach(f => children.push(indent(f, RED)));
  children.push(space(120));
}

// Footer note
children.push(new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 4, color: BGRAY, space: 1 } }, spacing: { before: 200, after: 60 } }));
children.push(new Paragraph({
  children: [new TextRun({ text: 'Documento de uso interno — Nexostrat. No compartir con el cliente.', font: 'Inter', size: 18, color: MGRAY, italics: true })],
  alignment: AlignmentType.CENTER,
}));

const doc = new Document({
  numbering: {
    config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 } } },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outFile, buf);
  console.log(`✓ DOCX interno (Ricardo): ${outFile}`);
}).catch(err => { console.error('Error:', err); process.exit(1); });
