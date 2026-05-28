# Pipeline v2 — Spec oficial (DRAFT)

**Estado:** DRAFT (sesión 26)
**Supersedes:** `2026-05-27_skill6-pipeline-redesign.md` (spec v1 de sesión 21) en los puntos donde las decisiones de la reunión 2026-05-28 contradicen o refinan v1
**Fuentes:**
- v1 spec (sesión 21): `2026-05-27_skill6-pipeline-redesign.md`
- Pipeline visual JP (sesión 24): `2026-05-27_pipeline-v2-jp.html` + `2026-05-27_whiteboard-jp-pipeline-v2.jpg`
- Doc 14 preguntas (sesión 24): `2026-05-27_preguntas-jp-pipeline-v2.md` [cerrado parcialmente]
- Reunión JP 2026-05-28 07:05: `/srv/meetings/nexostrat/2026-05-28/2026-05-28_07-05_buyer-persona-trixx-logistic-pipeline/`

---

## 1. Resumen ejecutivo

El Pipeline v2 mantiene la columna vertebral del v1 (Skills 01-05 internos → Skill 06 entregables cliente, revisión humana entre pasos, modelo agente-co-piloto) y se refina con las decisiones de la reunión 2026-05-28: estructura concreta de entregables (10 slides + 10-15 páginas), precio baseline ($3,000 USD), garantía 1 mes acotada a bugs, lenguaje de posicionamiento ("sistemas de consolidación de información", no "bots"), modelo de tercerización con Neo para proyectos fuera del alcance ágil, y facturación internacional vía empresa de JP en Panamá. Quedan 9 puntos abiertos (CRM definitivo, capacidades catálogo, Ciclo 2 fases, captación canales, funnel etapas, seguimiento plantillas/canal/cut-off, Cowork nombre comercial); su resolución no bloquea construir el Skill 6 técnico, sí bloquea la operación end-to-end del pipeline a producción.

---

## 2. Decisiones locked

### 2.1 De sesión 24 (5 decisiones previas, vigentes)

1. **Skill 6 produce dos artefactos**: `.docx` editable + `.pptx`. No PDF puro (Ricardo overrules a JP del v1; preserva editabilidad).
2. **Estructura interna del .docx**: diagnóstico + hoja de ruta + propuesta, todo en un solo documento (versión JP del v1).
3. **Reglas de entrega como default no rígido**: PPTX en la reunión, .docx al cierre. Flexibilidad caso por caso.
4. **Skill 7 desaparece como entidad separada**. Toda hoja de ruta + propuesta vive en el .docx del Skill 6, gratis, pre-cierre.
5. **`brief_cliente.md` eliminado**. Revisión libre Ricardo + IA hasta consenso, sin template estructurado intermedio.

### 2.2 De reunión 2026-05-28 (decisiones nuevas, locked)

6. **Extensión de entregables**: PPTX máximo 10 slides + DOCX/HTML 10-15 páginas. Balance exhaustividad vs lectura digerible.
7. **Precio baseline**: $3,000 USD mínimo por proyecto. Sin cobro por horas. Refleja consultoría completa (entendimiento + diseño + validación + construcción + pruebas), no programación. Margen de maniobra ante solicitudes adicionales del cliente durante el proceso.
8. **Garantía 1 mes — alcance**: solo bugs + ajustes menores sobre lo entregado. Features nuevos o cambios sustanciales de alcance = proyecto independiente.
9. **Garantía 1 mes — precio**: incluida en el precio estándar del proyecto. No es retainer adicional.
10. **Posicionamiento + lenguaje**: evitar "bot", "robot", "agente". Usar **"sistemas de consolidación de información"** o **"secretarios digitales"** en outputs cliente. Refuerza la regla locked sesión 21 sobre bajar frecuencia de "AI" + decir QUÉ se puede hacer, NO QUÉ comprar.

### 2.3 Decisiones nuevas que no estaban en las 14 preguntas

11. **Modelo de tercerización con Neo**: si un cliente solicita desarrollos que excedan el modelo de soluciones ágiles con IA de Nexostrat (ej. plataforma a la medida desde cero), Nexostrat retiene el rol comercial/estratégico y deriva la ejecución técnica a Neo a cambio de una comisión. Garantiza que Nexostrat puede decir "sí" a cualquier alcance sin contradecir su modelo de operación interno.
12. **Facturación internacional en USD**: vía empresa de JP registrada en Panamá — **Consultores Butacos**. Resuelve la pregunta operativa de cómo facturar desde México sin visa de trabajo.
13. **Estrategia de contenido marketing**: grabar reuniones internas / podcast → IA extrae piezas (newsletter, LinkedIn, hilos en Twitter). Una sola fuente, múltiples salidas. Optimiza tiempo de creación de contenido.
14. **Handles de redes sociales**: reservar `nexostrat_` (con guion bajo) en Instagram, Twitter, TikTok antes del Stage 1 launch.
15. **Buyer Persona Don Carlos consolidado**: JP merge'ó las versiones Ricardo (formulario completo) + JP (formulario propio) usando IA + generó video explicativo (`Cerrar_a_Don_Carlos.mp4`, ya organizado a `operations/marketing/buyer_personas/`, gitignored). Don Carlos = empresario tradicional 46-55 años (logística, manufactura), no usuario activo de LinkedIn/TikTok, comunicación debe enfocarse en dolor operativo concreto (desorganización, exceso hojas de cálculo, pérdida de info), no en lenguaje técnico de vanguardia digital.

---

## 3. Lo que sigue abierto (9 puntos)

Ninguno bloquea construir el Skill 6 técnico; sí bloquean operación end-to-end a producción.

| # | Pregunta | Decisión pendiente |
|---|---|---|
| (1) | CRM herramienta | Notion vs Odoo. Ricardo investiga Odoo (`t-012`, due TBD). |
| (4) | Catálogo capacidades | Pendiente desde sesión 17. Bloquea poner cifras exactas en propuesta sin ambigüedad. Se puede empezar con $3K baseline + iterar. |
| (5) | Ciclo 2 — 6 fases (skills vs humano vs mezcla) | Diferido hasta tener 1-2 pilotos reales. |
| (8) | Captación — canales | Mención lateral a estrategia de podcast/contenido; canales prospect-to-discovery sin decidir. |
| (9) | Funnel CRM etapas | Espera decisión CRM (Odoo vs Notion). |
| (10) | Plantillas seguimiento D+7..D+90 | Quién las escribe (Ricardo/JP/juntos). |
| (11) | Canal mensajes D+7..D+90 | WhatsApp vs email vs multi-canal. |
| (12) | Qué detiene la cadena | Cualquier respuesta vs solo "no me interesa". |
| (14) | "Cowork" nombre comercial vs etiqueta interna | Aplica solo a cómo se referencia la IA en outputs cliente; el lenguaje arriba (decisión #10) ya impone la regla principal. |

Pregunta (13) JP-en-el-flujo se redefine bajo decisión #11 (tercerización Neo) — la "participación opcional/obligatoria" de JP cambia de forma; queda pendiente cómo se aplica al Ciclo 1 cuando NO se tercerice.

---

## 4. Implicaciones constructivas para Skill 6

Con las decisiones de §2 ya se puede construir el skeleton del Skill 6:

- **Output 1 — PPTX**: 10 slides. Cover + 4 secciones espejo (Diagnóstico Operacional / Movimientos del Sector / Frentes de Oportunidad / Próximos Pasos) + slide propuesta-precio + slide cierre. Aurora brand. Formato: Inter + Aurora palette + 1 logo Arctic.
- **Output 2 — DOCX**: 10-15 páginas. Mismas 4 secciones espejo (más profundas) + sección 5 Propuesta con precio baseline $3K USD + alcance + garantía 1 mes (bugs y ajustes menores). Aurora brand via `skills/shared/brand.py`.
- **Lenguaje**: "sistemas de consolidación", "secretario digital", "menores disrupciones + mayor productividad". Cero "bot/robot/agente".
- **Section 5 propuesta — template**:
  - Alcance (qué se entrega, plazos)
  - Precio: $X USD (baseline $3,000+) — fee fijo, no por horas
  - Garantía: 1 mes incluida (bugs + ajustes menores; features nuevos = proyecto independiente)
  - Tercerización Neo cuando aplique (Nexostrat coordina; Neo ejecuta)
  - Facturación USD vía Consultores Butacos (Panamá)
- **Catálogo capacidades**: insumo desde el lado de JP (qué se entrega y a qué precio); por ahora se opera con el baseline $3K + Quick Wins específicos por cliente.

---

## 5. Roadmap implementación

| Fase | Qué se construye | Bloqueante hasta | Owner |
|---|---|---|---|
| F1 — Skill 6 skeleton | SKILL.md + scripts/generate_docx.py + .pptx renderer + Aurora brand wiring | — | JP (delivery) → Ricardo (wrap) |
| F2 — Skill 5 reprofile | Renombrar `05_opportunity_report` → `05_internal_report` (audiencia Nexostrat NO cliente) | F1 | Ricardo |
| F3 — Clients folder rename | `reporte_oportunidades` → `reporte_interno` en _template + slugs activos | F2 | Ricardo |
| F4 — Catálogo capacidades v0 | 1-pager con servicios + precios + timeline + "no entregable hoy" | — | Ricardo + JP juntos |
| F5 — Primer Skill 6 corrido (Trixx) | Validación end-to-end con cliente real | F1 + iteración Reporte de Oportunidades Trixx con notas Ricardo | Ricardo |
| F6 — CRM decisión | Notion vs Odoo (Ricardo investigación) | — | Ricardo |
| F7 — Captación + seguimiento | Canales, plantillas, funnel etapas | F6 | Ricardo + JP |
| F8 — Ciclo 2 detalle | 6 fases — skills vs humano | F5 (post-pilot) | Ricardo + JP |

F1 + F2 + F3 + F4 + F5 son la ruta crítica de Stage 1 (target 2026-06-30 a 2026-07-15).

---

## 6. Cross-references operativos

- Brand source: `skills/shared/brand.py` (Aurora palette + Inter + logos).
- Reporte Oportunidades Trixx (insumo Skill 6 primer corrida): `pipeline/clients/trixx-logistics/etapa_2_diagnostico/reporte_oportunidades/runs/2026-05-26_mode-a/Trixx_ReporteOportunidades_20260526.md` + notas Ricardo `transcripciones/2026-05-27_ricardo-notes/notas_curadas.md`.
- Skills inventory: `skills/00_META/inventory.md` (5 skills actuales 01-05).
- Calendario: `e-jp-pipeline-v2-meeting` cerrado 2026-05-28; sigue abierto `e-capabilities-catalog` due 2026-05-31.
- Tasks ledger: `t-skill6-jp-feedback-await` + `t-008` cerradas esta sesión; abiertas `t-010` a `t-015` + las 6 `t-skill6-*` previas que ahora se desbloquean para F1-F3.

---

## 7. Próximo paso

Sesión 27 (próxima): iteración del Reporte de Oportunidades Trixx con notas curadas de Ricardo (sesión dedicada por su nivel de detalle). Output: versión refinada del reporte lista para alimentar Skill 6 cuando JP entregue la versión ajustada.
