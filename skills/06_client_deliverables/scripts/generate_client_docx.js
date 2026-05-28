#!/usr/bin/env node
// generate_client_docx.js — Nexostrat Client Deliverables
// Usage: node generate_client_docx.js data_empresa.json [output_dir]
// Requires: npm install -g docx

const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
        PageNumber, Header, Footer, LevelFormat, VerticalAlign, PageBreak } = require('docx');
const fs = require('fs');
const path = require('path');

const dataFile = process.argv[2];
const outputDir = process.argv[3] || '.';
if (!dataFile) { console.error('Usage: node generate_client_docx.js data_empresa.json [output_dir]'); process.exit(1); }

const d = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const { metadata: M, empresa_hoy: E, situacion_por_area: AREAS, problemas: PROB,
        oportunidades: OPS, quick_wins: QW, roadmap_fases: FASES, propuesta: PROP, sobre_nexostrat: SOBRE } = d;

const empresa = M.empresa || 'Empresa';
const slug = M.empresa_slug || empresa.replace(/\s+/g, '');
const dateStr = M.fecha_iso ? M.fecha_iso.replace(/-/g,'') : new Date().toISOString().slice(0,10).replace(/-/g,'');
const outFile = path.join(outputDir, `${slug}_Diagnostico_Documento_${dateStr}.docx`);

// ── Brand
const NAVY = '0C1A2E', GREEN = '10B981', AMBER = 'F59E0B', LGRAY = 'F5F5F5', MGRAY = '6B7280', BGRAY = 'D1D5DB';
// Solid-color box backgrounds (docx lib requires 6-digit hex, no alpha)
const GREEN_BOX  = 'ECFDF5';   // light green box bg
const NAVY_BOX   = 'F0FBFF';   // light navy/blue box bg
const AMBER_BOX  = 'FFFBEB';   // light amber box bg

function fmt(n) { return n ? `USD ${n.toLocaleString('en-US')}` : ''; }
function fmtRange(o) {
  if (!o) return '';
  if (o.precio_usd_max) return `USD ${o.precio_usd_min.toLocaleString('en-US')} – ${o.precio_usd_max.toLocaleString('en-US')}`;
  return `USD ${o.precio_usd_min.toLocaleString('en-US')}`;
}

// ── Paragraph helpers
function P(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text: text || '', font: 'Inter', size: opts.size || 22, bold: opts.bold, color: opts.color, italics: opts.italic })],
    alignment: opts.align || AlignmentType.LEFT,
    spacing: { before: opts.spE0F2FEore ?? 120, after: opts.spaceAfter ?? 80 },
    heading: opts.heading,
    pageBreakBefore: opts.pageBreak,
    ...opts.paraOpts,
  });
}
function H1(text) { return P(text, { heading: HeadingLevel.HEADING_1, size: 32, bold: true, color: NAVY, spE0F2FEore: 280, spaceAfter: 140 }); }
function H2(text) { return P(text, { heading: HeadingLevel.HEADING_2, size: 26, bold: true, color: NAVY, spE0F2FEore: 200, spaceAfter: 100 }); }
function H3(text) { return P(text, { heading: HeadingLevel.HEADING_3, size: 24, bold: true, color: '0D4A6B', spE0F2FEore: 160, spaceAfter: 80 }); }
function Body(text, opts = {}) { return P(text, { size: 22, color: '1F2937', spE0F2FEore: 80, spaceAfter: 80, ...opts }); }
function Muted(text) { return P(text, { size: 20, color: MGRAY, italic: true, spE0F2FEore: 60, spaceAfter: 60 }); }
function space(pt = 200) { return new Paragraph({ spacing: { before: 0, after: pt } }); }

function divider() {
  return new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BGRAY, space: 1 } }, spacing: { before: 120, after: 120 } });
}

function labelValue(label, value) {
  return new Paragraph({
    children: [
      new TextRun({ text: `${label}: `, font: 'Inter', size: 22, bold: true, color: NAVY }),
      new TextRun({ text: value || '', font: 'Inter', size: 22, color: '1F2937' }),
    ],
    spacing: { before: 60, after: 60 },
  });
}

function bullet(text, color = NAVY) {
  return new Paragraph({
    children: [new TextRun({ text: text || '', font: 'Inter', size: 22, color: '1F2937' })],
    numbering: { reference: 'bullets', level: 0 },
    spacing: { before: 60, after: 60 },
  });
}

function colorBox(text, bgColor, borderColor, labelText) {
  const cell = new TableCell({
    borders: { top: { style: BorderStyle.SINGLE, size: 6, color: borderColor },
                bottom: { style: BorderStyle.SINGLE, size: 2, color: borderColor },
                left: { style: BorderStyle.SINGLE, size: 8, color: borderColor },
                right: { style: BorderStyle.SINGLE, size: 2, color: borderColor } },
    shading: { fill: bgColor, type: ShadingType.CLEAR },
    margins: { top: 120, bottom: 120, left: 160, right: 160 },
    width: { size: 9360, type: WidthType.DXA },
    children: [
      ...(labelText ? [new Paragraph({ children: [new TextRun({ text: labelText, font: 'Inter', size: 18, bold: true, color: borderColor })], spacing: { before: 0, after: 60 } })] : []),
      new Paragraph({ children: [new TextRun({ text: text || '', font: 'Inter', size: 21, color: '1F2937', italics: !labelText })], spacing: { before: 0, after: 0 } }),
    ],
  });
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({ children: [cell] })],
  });
}

// ── Priority table (opportunities)
function priorityTable() {
  const hCell = (text, w) => new TableCell({
    borders: { bottom: { style: BorderStyle.SINGLE, size: 4, color: NAVY } },
    shading: { fill: NAVY, type: ShadingType.CLEAR },
    width: { size: w, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    children: [new Paragraph({ children: [new TextRun({ text, font: 'Inter', size: 20, bold: true, color: 'FFFFFF' })] })],
  });
  const dCell = (text, w, bold = false, color = '1F2937') => new TableCell({
    width: { size: w, type: WidthType.DXA },
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    borders: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BGRAY } },
    children: [new Paragraph({ children: [new TextRun({ text: text || '', font: 'Inter', size: 20, bold, color })] })],
  });

  const colW = [3200, 1200, 900, 2000, 2060];
  const header = new TableRow({ children: [hCell('Iniciativa', colW[0]), hCell('Área', colW[1]), hCell('Complejidad', colW[2]), hCell('Inversión', colW[3]), hCell('Impacto', colW[4])] });
  const rows = OPS.map(op => new TableRow({ children: [
    dCell((QW.includes(op.id) ? '⚡ ' : '') + (op.titulo || ''), colW[0], QW.includes(op.id)),
    dCell(op.area || '', colW[1]),
    dCell(op.categoria || '', colW[2]),
    dCell(fmtRange(op), colW[3], true, GREEN),
    dCell('★'.repeat(op.impacto_score || 3) + '☆'.repeat(5 - (op.impacto_score || 3)), colW[4], false, AMBER),
  ]}));

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: colW,
    rows: [header, ...rows],
  });
}

// ─────────────────────────────────────────────
// BUILD DOCUMENT
// ─────────────────────────────────────────────
const children = [];

// ── COVER PAGE
children.push(
  space(1440),
  new Paragraph({ children: [new TextRun({ text: 'NEXOSTRAT', font: 'Inter', size: 36, bold: true, color: MGRAY })], spacing: { before: 0, after: 200 } }),
  new Paragraph({ children: [new TextRun({ text: 'Diagnóstico de Oportunidades de IA', font: 'Inter', size: 48, bold: true, color: NAVY })], spacing: { before: 0, after: 160 } }),
  new Paragraph({ children: [new TextRun({ text: empresa, font: 'Inter', size: 36, bold: true, color: GREEN })], spacing: { before: 0, after: 200 } }),
  divider(),
  labelValue('Preparado por', M.consultor || 'Nexostrat'),
  labelValue('Fecha', M.fecha_display || M.fecha_iso || ''),
  ...(M.consultor_email ? [labelValue('Contacto', [M.consultor_email, M.consultor_whatsapp].filter(Boolean).join('  ·  '))] : []),
  space(1440),
  new Paragraph({ children: [new PageBreak()] }),
);

// ── SECTION 1: RESUMEN EJECUTIVO
children.push(H1('1. Resumen Ejecutivo'));
children.push(Body(
  `El presente reporte documenta los resultados del diagnóstico de oportunidades de inteligencia artificial realizado para ${empresa}. ` +
  `En el proceso analizamos la empresa en su contexto de industria, estudiamos a sus competidores directos y, lo más importante, ` +
  `conversamos directamente con el equipo para entender los dolores operativos desde adentro. ` +
  `Lo que encontramos no son oportunidades genéricas de "adoptar IA" — son iniciativas específicas, ` +
  `vinculadas a problemas concretos que ${empresa} enfrenta hoy, con beneficios cuantificables y un punto de entrada claro.`
));
children.push(space(120));
children.push(H2('Hallazgos principales'));
const PROB_DISPLAY = PROB.slice(0, 5);
PROB_DISPLAY.forEach(p => {
  children.push(bullet(`${p.titulo}: ${p.descripcion?.substring(0, 140) || ''}`));
});
children.push(space(120));
const qwList = QW.map(id => OPS.find(o => o.id === id)).filter(Boolean);
if (qwList.length > 0) {
  children.push(colorBox(
    `Quick Wins identificados: ${qwList.map(q => q.titulo).join(' y ')}. Impacto alto, implementación en semanas. ` +
    `Estas iniciativas están diseñadas para generar resultados visibles en las primeras 4-6 semanas de implementación.`,
    GREEN_BOX, GREEN, '✅ Punto de entrada recomendado'
  ));
}
children.push(space(80));
// Summary table: key numbers
const sumRows = [
  ['Problemas críticos identificados', String(PROB.length)],
  ['Oportunidades de IA priorizadas', String(OPS.length)],
  ['Iniciativas Quick Win', String(QW.length)],
  ['Valor total del roadmap', fmt(PROP.total_roadmap_usd)],
  ['Iniciativa de entrada sugerida', (OPS.find(o => o.id === PROP.iniciativa_entrada_id) || qwList[0] || OPS[0])?.titulo || ''],
];
const mkSumCell = (text, w, bold = false, color = '1F2937') => new TableCell({
  width: { size: w, type: WidthType.DXA },
  margins: { top: 80, bottom: 80, left: 120, right: 120 },
  borders: { bottom: { style: BorderStyle.SINGLE, size: 1, color: BGRAY } },
  children: [new Paragraph({ children: [new TextRun({ text: text || '', font: 'Inter', size: 21, bold, color })] })],
});
children.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [5000, 4360],
  rows: [
    new TableRow({ children: [
      new TableCell({ shading: { fill: NAVY, type: ShadingType.CLEAR }, width: { size: 5000, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
        borders: {}, children: [new Paragraph({ children: [new TextRun({ text: 'Indicador', font: 'Inter', size: 20, bold: true, color: 'FFFFFF' })] })] }),
      new TableCell({ shading: { fill: NAVY, type: ShadingType.CLEAR }, width: { size: 4360, type: WidthType.DXA }, margins: { top: 80, bottom: 80, left: 120, right: 120 },
        borders: {}, children: [new Paragraph({ children: [new TextRun({ text: 'Resultado', font: 'Inter', size: 20, bold: true, color: 'FFFFFF' })] })] }),
    ]}),
    ...sumRows.map(([label, val]) => new TableRow({ children: [mkSumCell(label, 5000, false, MGRAY), mkSumCell(val, 4360, true, NAVY)] })),
  ],
}));
children.push(space(80));
children.push(Body(
  `Este reporte está organizado en diez secciones. Las secciones 5 y 6 son el corazón del diagnóstico: los problemas con su costo de inacción ` +
  `y las oportunidades con su beneficio esperado. La sección 8 presenta la hoja de ruta completa y la sección 9 la propuesta comercial para iniciar el Ciclo 2.`,
  { italic: true }
));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 2: METODOLOGÍA
children.push(H1('2. Metodología del Diagnóstico'));
children.push(Body('Para llegar a las recomendaciones de este reporte ejecutamos un proceso de análisis en cuatro pasos:'));
children.push(space(80));
[
  ['1. Análisis de la empresa', 'Estudiamos el perfil de ' + empresa + ': su modelo de negocio, tecnología actual, estructura y posición en el mercado.'],
  ['2. Análisis de la industria', 'Analizamos las tendencias del sector, el nivel de adopción de IA entre empresas similares y los benchmarks de eficiencia disponibles.'],
  ['3. Análisis competitivo', 'Identificamos qué están haciendo los competidores directos en materia de digitalización e IA, y dónde existen brechas que se pueden capitalizar.'],
  ['4. Llamada de descubrimiento', 'Conversación directa con el equipo de ' + empresa + ' para entender los dolores operativos, las prioridades y la visión de futuro desde adentro.'],
].forEach(([label, desc]) => {
  children.push(labelValue(label, desc));
  children.push(space(60));
});
children.push(Body('Este proceso nos permite hacer recomendaciones específicas para esta empresa, no genéricas. Cada oportunidad identificada en este reporte tiene evidencia directa en uno o más de los cuatro pasos anteriores.', { italic: true }));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 3: TU EMPRESA HOY
children.push(H1('3. Tu Empresa Hoy'));
children.push(Body(E.descripcion || ''));
children.push(space(100));
if (E.metricas_clave?.length) {
  children.push(H2('Indicadores clave'));
  E.metricas_clave.forEach(m => children.push(bullet(m)));
  children.push(space(80));
}
children.push(H2('Madurez digital y posición competitiva'));
children.push(labelValue('Nivel de madurez digital', `${E.madurez_digital || ''} — ${E.madurez_digital_descripcion || ''}`));
children.push(labelValue('Posición competitiva', E.posicion_competitiva || ''));
children.push(space(80));
children.push(Body(
  `El nivel de madurez digital ${E.madurez_digital ? '"' + E.madurez_digital + '"' : 'actual'} es el punto de partida para dimensionar correctamente las oportunidades. ` +
  `Las empresas en este nivel tienen un margen significativo de mejora en eficiencia operativa mediante herramientas de automatización e inteligencia artificial. ` +
  `Las iniciativas identificadas en este diagnóstico están calibradas para esta realidad: ` +
  `no asumen infraestructura tecnológica sofisticada ni equipos de tecnología especializados, ` +
  `sino que parten de las herramientas que la empresa ya usa y las potencian.`
));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 4: SITUACIÓN POR ÁREA
children.push(H1('4. Situación Actual por Área'));
children.push(Body(
  `A continuación presentamos el análisis de la situación tecnológica y operativa de cada área de ${empresa}. ` +
  `Este análisis es la base sobre la que se construyeron las oportunidades de IA de la sección siguiente: ` +
  `cada área tiene sus propios cuellos de botella y sus propias oportunidades de mejora.`
));
children.push(space(100));
const AREAS_DISPLAY = (AREAS || []);
AREAS_DISPLAY.forEach(area => {
  children.push(H2(area.area || ''));
  children.push(Body(area.situacion_actual || ''));
  children.push(space(60));
  children.push(colorBox(
    area.oportunidades || '',
    GREEN_BOX, GREEN, '→ Oportunidades identificadas en esta área'
  ));
  children.push(space(120));
});
if (!AREAS_DISPLAY.length) {
  children.push(Body('El análisis detallado por área está integrado en las secciones de problemas y oportunidades.'));
}
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 5: PROBLEMAS IDENTIFICADOS
const PROB_DOC = PROB.slice(0, 5); // cap at 5 to prevent exceeding page budget
children.push(H1('5. Problemas Identificados'));
children.push(Body(
  `Identificamos ${PROB.length} problema${PROB.length === 1 ? '' : 's'} crítico${PROB.length === 1 ? '' : 's'} en la operación de ${empresa}. ` +
  `Para cada uno incluimos: la descripción del impacto en el negocio, ` +
  `la cita directa de la conversación que da evidencia del problema, ` +
  `y una estimación del costo de no actuar — ya sea en ventas perdidas, capital inmovilizado u horas desperdiciadas. ` +
  `Estos números son importantes: la IA no es un gasto, es una respuesta a un costo que ya existe.`
));
children.push(space(120));

PROB_DOC.forEach((p, i) => {
  children.push(H2(`${i + 1}. ${p.titulo || ''}`));
  children.push(Body(p.descripcion || ''));
  if (p.cita_cliente) {
    children.push(space(80));
    children.push(colorBox(`En tus propias palabras: "${p.cita_cliente}"`, NAVY_BOX, NAVY, null));
    children.push(space(80));
  }
  if (p.costo_inaccion) {
    children.push(colorBox(
      `${p.costo_inaccion.descripcion || ''}${p.costo_inaccion.calculo ? `  (${p.costo_inaccion.calculo})` : ''}${p.costo_inaccion.es_estimado ? ' ⚠️ estimado' : ''}`,
      AMBER_BOX, AMBER, '⏱ Costo de no actuar'
    ));
  }
  children.push(space(160));
});
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 6: OPORTUNIDADES DE IA
const OPS_DOC = OPS.slice(0, 6); // cap at 6 to prevent exceeding page budget
children.push(H1('6. Oportunidades de IA'));
children.push(Body(
  `Identificamos ${OPS.length} oportunidad${OPS.length === 1 ? '' : 'es'} concretas para implementar IA en ${empresa}. ` +
  `Cada una está directamente vinculada a un problema identificado en la sección anterior, ` +
  `tiene un beneficio esperado cuantificable, una categoría de complejidad (pequeño, mediano o grande) ` +
  `y una estimación de inversión basada en el tiempo real de implementación. ` +
  `Las marcadas con ⚡ son Quick Wins: iniciativas de alta relación impacto/esfuerzo recomendadas como punto de entrada al Ciclo 2.`
));
children.push(space(120));

OPS_DOC.forEach((op, i) => {
  const isQW = QW.includes(op.id);
  children.push(H2(`${isQW ? '⚡ ' : ''}${op.titulo || ''}`));
  children.push(labelValue('Área', op.area || ''));
  children.push(labelValue('Problema que resuelve', PROB.find(pr => pr.id === op.problema_id)?.titulo || ''));
  children.push(Body(op.descripcion || ''));
  children.push(space(60));
  children.push(colorBox(op.beneficio_esperado || '', GREEN_BOX, GREEN, '✅ Beneficio esperado'));
  children.push(space(60));
  children.push(labelValue('Inversión estimada', fmtRange(op) + (op.precio_nota ? `  (${op.precio_nota})` : '')));
  if (op.requiere_infraestructura && op.fee_mensual_usd) {
    children.push(labelValue('Infraestructura mensual', `USD ${op.fee_mensual_usd}/mes`));
  }
  children.push(space(160));
});
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 7: MAPA DE PRIORIDADES
children.push(H1('7. Mapa de Prioridades'));
children.push(Body('La siguiente tabla muestra todas las iniciativas ordenadas por impacto y esfuerzo. Las marcadas con ⚡ son los Quick Wins recomendados como punto de entrada.'));
children.push(space(120));
children.push(priorityTable());
children.push(space(120));
children.push(Muted('⚡ Quick Win  ·  Impacto: ★ = bajo → ★★★★★ = alto  ·  Complejidad: pequeño / mediano / grande'));
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 8: HOJA DE RUTA
children.push(H1('8. Hoja de Ruta — Ciclo 2'));
children.push(Body(
  `El Ciclo 2 es la etapa de diseño e implementación. A diferencia de una consultora tradicional que entrega un informe, ` +
  `Nexostrat construye y entrega las soluciones funcionando en la operación del cliente. ` +
  `El proceso está dividido en ocho etapas secuenciales que garantizan cero sorpresas y un resultado final que el equipo adopta desde el primer día.`
));
children.push(space(80));
[
  ['1. Entendimiento', 'Análisis detallado del flujo actual, casos extremos, integraciones necesarias y requerimientos técnicos. El cliente revisa y aprueba el documento de entendimiento antes de continuar.'],
  ['2. Diseño', 'Diseño funcional de la solución: qué hace exactamente, cómo funciona, cómo se integra con los sistemas existentes, y qué datos necesita. Se entrega un documento de diseño detallado.'],
  ['3. Validación', 'El cliente revisa y aprueba el diseño antes de que se escriba una sola línea de código. Esta etapa es la que elimina el riesgo de construir algo que no era lo que se esperaba.'],
  ['4. Construcción', 'Desarrollo e integración de las soluciones según el diseño aprobado. Demos parciales durante el proceso para mantener al cliente informado.'],
  ['5. Pruebas', 'Validación funcional completa: pruebas de integración con los sistemas del cliente, pruebas de carga, y revisión con el equipo que va a usar la solución.'],
  ['6. Ajustes', 'Correcciones y refinamientos con base en los resultados de las pruebas y el feedback del equipo. Esta etapa está incluida en el precio — no es un extra.'],
  ['7. Implementación', 'Puesta en producción, capacitación del equipo y entrega formal. El saldo del proyecto se paga al llegar aquí.'],
  ['8. Garantía (1 mes)', 'Soporte técnico post-implementación durante el mes siguiente a la entrega. Si algo no funciona como se prometió, se corrige sin costo adicional.'],
].forEach(([fase, desc]) => {
  children.push(new Paragraph({
    children: [
      new TextRun({ text: `${fase}:  `, font: 'Inter', size: 22, bold: true, color: NAVY }),
      new TextRun({ text: desc, font: 'Inter', size: 22, color: '1F2937' }),
    ],
    spacing: { before: 80, after: 80 },
  }));
});
children.push(space(120));
FASES.forEach(fase => {
  children.push(H2(fase.fase || ''));
  children.push(Body(fase.descripcion || ''));
  const faseOps = (fase.oportunidades_ids || []).map(id => OPS.find(o => o.id === id)).filter(Boolean);
  faseOps.forEach(op => children.push(bullet(`${op.titulo} — ${fmtRange(op)}`)));
  children.push(space(80));
});
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 9: PROPUESTA COMERCIAL
children.push(H1('9. Propuesta Comercial'));
const entradaOp = OPS.find(o => o.id === PROP.iniciativa_entrada_id) || (qwList.length > 0 ? qwList[0] : OPS[0]);
children.push(colorBox(
  `El valor total del roadmap completo (${OPS.length} iniciativas) es de ${fmt(PROP.total_roadmap_usd)}`,
  NAVY_BOX, NAVY, 'Valor total del roadmap (referencia)'
));
children.push(space(120));
children.push(H2('Iniciativa de entrada sugerida'));
if (entradaOp) {
  children.push(Body(`${entradaOp.titulo || ''} — ${fmtRange(entradaOp)}`, { bold: true }));
  children.push(Body(entradaOp.descripcion || ''));
  if (entradaOp.requiere_infraestructura && entradaOp.fee_mensual_usd) {
    children.push(Body(`Fee mensual de infraestructura: USD ${entradaOp.fee_mensual_usd}/mes`));
  }
}
children.push(space(120));
children.push(H2('Estructura de pago'));
children.push(Body(PROP.estructura_pago_descripcion || 'Pago dividido: upfront al confirmar + saldo a la entrega final.'));
children.push(space(80));
children.push(colorBox(PROP.garantia_descripcion || '1 mes de garantía post-implementación incluido.', GREEN_BOX, GREEN, '✅ Garantía'));
children.push(space(120));
children.push(H2('¿Qué incluye el Ciclo 2?'));
['Análisis detallado de requerimientos y diseño de la solución', 'Construcción e integración completa', 'Pruebas y ajustes hasta entrega', 'Implementación en producción', '1 mes de garantía post-implementación', 'Soporte técnico durante el proyecto'].forEach(item => children.push(bullet(item)));
children.push(space(120));
children.push(H2('¿Qué no incluye?'));
['Licencias de software de terceros (si aplica)', 'Cambios de alcance una vez iniciado el diseño sin acuerdo previo'].forEach(item => children.push(bullet(item)));
children.push(space(120));
children.push(H2('Próximos pasos'));
children.push(Body(
  `Si después de leer este reporte quieres avanzar con el Ciclo 2, el proceso es simple: ` +
  `(1) Confirmas cuál iniciativa quieres iniciar primero — si no hay una preferencia clara, te recomendamos el Quick Win sugerido en este reporte. ` +
  `(2) Firmamos el acuerdo de trabajo y procesas el primer pago (${PROP?.upfront_porcentaje || 50}% upfront). ` +
  `(3) Iniciamos el Ciclo 2 en los siguientes 3-5 días hábiles con la etapa de Entendimiento. ` +
  `Si tienes preguntas sobre el alcance, los precios o la metodología antes de decidir, estamos disponibles para una llamada de revisión sin costo.`
));
children.push(space(80));
if (M.consultor_email || M.consultor_whatsapp) {
  children.push(labelValue('Para avanzar, contactar a', [M.consultor, M.consultor_email, M.consultor_whatsapp].filter(Boolean).join('  ·  ')));
}
children.push(new Paragraph({ children: [new PageBreak()] }));

// ── SECTION 10: SOBRE NEXOSTRAT
children.push(H1('10. Sobre Nexostrat'));
children.push(Body(SOBRE || 'Nexostrat es una consultora especializada en implementación de IA para PYMEs colombianas y mexicanas. Nuestra metodología de entendimiento → diseño → validación → construcción garantiza que cada solución queda funcionando antes de cobrar el total. No vendemos software — implementamos soluciones que funcionan en tu operación específica.'));

// ─────────────────────────────────────────────
// ASSEMBLE & WRITE
// ─────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [{
      reference: 'bullets',
      levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
    }],
  },
  styles: {
    default: { document: { run: { font: 'Inter', size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true, font: 'Inter', color: NAVY },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: 'Inter', color: NAVY },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 24, bold: true, font: 'Inter', color: '0D4A6B' },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ],
  },
  sections: [{
    properties: {
      page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        children: [
          new TextRun({ text: 'NEXOSTRAT  ·  ', font: 'Inter', size: 18, bold: true, color: NAVY }),
          new TextRun({ text: `Diagnóstico de Oportunidades de IA — ${empresa}`, font: 'Inter', size: 18, color: MGRAY }),
        ],
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: BGRAY, space: 1 } },
        spacing: { after: 200 },
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        children: [
          new TextRun({ text: M.fecha_display || '', font: 'Inter', size: 18, color: MGRAY }),
          new TextRun({ text: '\t\t' }),
          new TextRun({ text: 'Pág. ', font: 'Inter', size: 18, color: MGRAY }),
          new TextRun({ children: [PageNumber.CURRENT], font: 'Inter', size: 18, color: MGRAY }),
        ],
        alignment: AlignmentType.RIGHT,
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: BGRAY, space: 1 } },
        spacing: { before: 200 },
      })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outFile, buf);
  console.log(`✓ DOCX cliente: ${outFile}`);
}).catch(err => { console.error('Error:', err); process.exit(1); });
