# CHECKPOINT — trixx-logistics (Client-Owner)

**Updated:** 2026-05-26 (session 20 — reunión formal DONE + transcripciones triple-engine + Claude curados)
**By:** ricardo (via Claude Code at /srv/Nexostrat/, ricardo-desktop)
**Persona:** Client-Owner (cross-persona desde sesión Founder per Strict Rule 1 operator-driven)

## Update 2026-05-26 (session 20, PM) — Reunión formal ocurrió, artifacts archivados, transición de phase

**Disparador.** Ricardo subió `drive-download-20260527T020829Z-3-001.zip` con 2 audios + 2 transcripts Apple de la **reunión formal 3-personas + Luis** que ocurrió en la mañana del 2026-05-26 (sesión 10:10 AM ~113 min principal + sesión 12:05 PM ~31 min de deep-dive). Encargo: organizar los 4 PDFs del Desktop (output de skills re-corridos en session 19) + el contenido del zip en su carpeta profesional, luego generar **3 transcripciones independientes** (WhisperX = "el sistema que tenemos", Gemini, Claude) y comparar resultados.

**Phase transition aplicado.** `state.json` phase: `prospect` → `discovery` con timestamp 2026-05-26T20:00:00-07:00. Justificación: la reunión formal de descubrimiento ocurrió y produjo intel suficiente para Skill 05.

**Layout final del meeting folder** (en `pipeline/clients/trixx-logistics/transcripts/2026-05-26_formal-meeting/`):

```
README.md                                  ← comparación triple-engine + metodología
1010_main-meeting_transcript_final.md      ← ⭐ TRANSCRIPCIÓN CANÓNICA 10:10 (91 KB, lectura humana)
1205_second-session_transcript_final.md    ← ⭐ TRANSCRIPCIÓN CANÓNICA 12:05 (32 KB, lectura humana)
audio/                                     ← 2 .m4a originales (plaintext, sin vault per override Ricardo)
apple/                                     ← Apple Voice Memos baseline (32 KB + 7 KB)
whisperx/                                  ← WhisperX large-v3 + pyannote diarization (100 KB + 33 KB)
  ├── 1010_main-meeting.{txt,srt,json,tsv,vtt}
  ├── 1205_second-session.{txt,srt,json,tsv,vtt}
  └── logs/                                ← incluye log del OOM en primer intento
gemini/                                    ← INCOMPLETO (ver § Gemini failure abajo)
  ├── 1010_main-meeting.HALLUCINATION.md   (artefacto fabricado, marcado)
  └── 1010_main-meeting_SAMPLE_first5min.md (muestra de 5 min — calidad demostrada)
claude/                                    ← Síntesis estructurada multi-fuente (28 KB + 16 KB)
  ├── 1010_main-meeting.md                 (narrativa 9 bloques + datos accionables + 11 citas highlights)
  └── 1205_second-session.md               (narrativa 6 bloques + propuesta de pricing capturada)
```

**Pipeline de la transcripción final (session 20 continuación, post-correcciones de Ricardo):** Script `/tmp/transcript_final_builder.py` (Python) parsea `whisperx/*.srt`, mapea `SPEAKER_NN → nombres reales`, aplica correcciones (María Helena no Marilena, Tracking Premium, Monday.com, McKinney, Vernon, acentos ES), filtra artefactos WhisperX (hotword-spill — 9 filtrados en 10:10), agrupa turnos consecutivos del mismo hablante (gap ≤2.5s) y emite markdown con marcas de tiempo cada minuto. Output: `*_transcript_final.md` en root del meeting folder. Idempotente — re-ejecutable si surgen más correcciones.

**Transcripción WhisperX — éxito.**
- 12:05 (~31 min): completó en ~5 min con batch=4 float16. 4 voces detectadas, mapping confirmado (00=Ricardo, 01=Hector, 02=María Helena, 03=Andrea).
- 10:10 (~113 min): **primer intento OOM al final** con batch=4 float16 (8 GB VRAM insuficiente para diarización a esa duración). Reintento con `batch=2 + int8` exitoso en ~6 min. 6 voces detectadas (mapping: 00=Ricardo, 02=Hector, 03=Andrea, 04=Luis, 05=María Helena primaria, 01=María Helena variante diarización).
- Hotwords cargadas sesgaron correctamente reconocimiento de nombres propios (María Helena, Sofía, Damián, Carlos Muñoz, Leonisa, etc.).

**Transcripción Gemini — FALLÓ a escala. Patrón crítico descubierto:**

1. **Hallucination con archivos >20 MB.** Gemini CLI 0.42.0 rechaza adjuntos audio sobre 20 MB pero **NO falla cleanly** — fabrica una "transcripción" plausible a partir del prompt + hotwords. Generó una reunión imaginaria con Luis en LA, María Helena en Bogotá, Andrea en San Diego (la real fue presencial Tijuana), con discusión técnica detallada sobre Reforma Aduanera + Nuvocargo + Flexport — TODOS temas plantados por mis hotwords. Preservado como `1010_main-meeting.HALLUCINATION.md` para evidencia.

2. **AUDIO_NOT_LOADED no-determinístico con archivos ≤7 MB.** Chunkeé audio en 30 segmentos de 5 min (1.2 MB c/u). Smoke test con 30 seg + 5 min sample funcionaron perfecto. Lanzamiento batch de los 30 segmentos: **1 de 30 completó en 25 min**. Tasa efectiva <5%. Error subyacente: `NumericalClassifierStrategy failed: API returned invalid content after all retries` — bug del routing interno del CLI, no rate limit documentado.

**Veredicto comparativo (en README detallado):** WhisperX es la fuente primaria confiable. Gemini CLI 0.42.0 **NO es production-ready** para transcripción directa de audios largos vía batch — el riesgo de hallucination silenciosa lo hace peligroso. El sistema canónico Nexostrat `~/bin/summarize-meeting.sh` sigue siendo OK porque usa Gemini en el paso de SUMMARY (no transcripción), recibiendo ya el texto WhisperX como input.

**Claude curado — síntesis estructurada.** No es transcripción cruda (Claude no procesa audio directamente); es **documento de trabajo** que toma WhisperX como fuente primaria + contexto de cliente y produce narrativa por bloques temáticos con datos accionables. Diseñado como feed directo a Skill 05.

**Datos críticos NUEVOS revelados en la reunión (vs. session 19):**

| Categoría | Nueva info |
|---|---|
| **Estructura societaria** | Inversor **Jan** (chino-venezolano) entrará con **USD 1,050,000 vía visa EB-5** — Jan será el nuevo dueño formal de Trixx para facilitar su residencia + ciudadanía USA. Hector planea retirarse de la operativa en 2026 post-inversión. María Helena queda con más peso operativo. |
| **Flota actualizada** | 120+ vehículos. 22+ camiones (+10 nuevos comprados recientemente). 70+ cajas (+30 nuevas, VINs en trámite). 40 cajas rentadas a McKinney. 5 sedes operativas + bodega LA (Vernon) sub-arrendada (muy pequeña). |
| **Stack tecnológico real** | **Tracking Premium** (SaaS principal, paquetes/tarifas, riesgo pérdida datos si se descontinúa) + **Samsara** (GPS+cámaras+audio camiones, audio recién activado) + **McKinney** (plataforma cajas rentadas) + **Monday.com** (cliente chino, usado por Graciela — María Helena lo quiere replicar para Trixx en general) + **AnyDesk** (impresión remota Vernon) + **GoDaddy** → migrando a **Microsoft 365**. Hector reconoce stack-sprawl: *"tenemos parchecitos"*. |
| **Personal clave** | **Beto** = encargado bodega LA, perdedor de clientes por trato déspota, sin estudios, manda reportes a mano por WhatsApp — Hector lo mantiene por miedo a robo interno. **Silvia** = capturista, cliente con escalamiento 5→80 contenedores inminente. **Graciela** = operadora del Monday.com cliente chino. **Damián** = broker USA, factura 135 contenedores/mes a María Helena que ella concilia manualmente con chats WhatsApp (busca número OMC). **Carlos Muñoz** = otro broker, pagos en efectivo, accounting reconciliation issues. **Carlos** (otro) = hosting/web provider no-responsivo, hostage situation IT. **Miguel, Eduardo, Rosy** = operativos. |
| **Pain quantificados** | 600 correos acumulados en bandeja cada finde. 135 contenedores/mes para reconciliar con Damián. $60K MXN perdidos en una negociación policial mal manejada (chofer con cortinas cerradas). $7K USD una guía. |
| **Métricas de éxito de los decisores** | **Hector:** tiempo de respuesta a incidentes (NO ahorro de costos). *"Yo no me quiero ahorrar 100 dólares, lo que quiero es tener las respuestas en el momento."* **María Helena:** información buscable en ≤3 minutos. *"Yo le digo mucho arriba: la información tiene que estar en tres minutos."* |
| **Quick-wins explícitos identificados durante la reunión** | (1) **Filtrado IA de correos por carpeta** (María Helena lo pidió textual — *"¿cómo podemos filtrar los 600 correos del lunes?"*). (2) **Replicar Monday.com de Graciela para todo Trixx**. (3) **Hoja de vida digital** de camiones (vencimientos, mantenimientos, inspecciones) + personal (contratos, choferes mex vs ame). (4) **Bot WhatsApp** para reconciliar Damián. (5) **Migración email + hosting** (sacarlo de control de Carlos). |
| **Visita LA pactada** | Jueves 2026-05-28 (María Helena + Andrea + posiblemente Hector + Ricardo). Cruce frontera por definir (moto + rent-a-car, o todos en un solo carro). Hector explícitamente pidió ir a campo: *"las decisiones que se toman de escritorio para mí nunca han sido las... tenemos que ir a ver el comportamiento, el flujo del trabajo"*. |

**Discrepancia con directiva pre-reunión:**
- ✅ **NO se mencionó Nuvocargo** en ningún momento.
- ✅ **NO se hicieron defectos del sitio**.
- ✅ **SÍ se ancló al legado de Hector** (Colombia, Leonisa, 25 años).
- ⚠️ **Ricardo SÍ presentó estructura de pricing en la sesión 12:05** — iniciado por María Helena con *"¿Cómo son tus honorarios?"*. Dos caminos: A (in-house, fee único) o B (fee inicial + fee mensual gestionado). Sin números cerrados. Disclosure honesta: *"ustedes son nuestro primer cliente, la verdad."* No transgresión sustantiva — vino de iniciativa del cliente, no propuesta proactiva.

**Memorias guardadas en esta sesión:**
- `feedback_no_vault_for_client_material.md` — override de Ricardo: material de cliente activo queda plano, no se encripta a vault.

**Estado del cliente al cierre de session 20:** phase `discovery`, todos los artefactos de la reunión formal archivados, Claude curados listos como feed de Skill 05, visita LA pactada para 2026-05-28. **Pendiente operacional:** corregir referencias en `01_company_analysis/runs/2026-05-26_mode-a/final_report.md` con los datos nuevos (María Helena no "María Helena" como nombre principal, inversión EB-5 vía Jan no inversión genérica, métricas de éxito específicas, etc.) — defer para próxima sesión o tras la visita LA.

---

## Update 2026-05-26 (session 19) — Pipeline re-corrida tras conversación informal del día

## Update 2026-05-26 (session 19) — Pipeline re-corrida tras conversación informal del día

**Disparador.** Ricardo abrió session 19 pidiendo un "test run" del pipeline completo Skills 01-04 sobre Trixx, validando que la toolchain estuviera operacional en `ricardo-desktop`. Después aportó intel adicional de una conversación informal Andrea ↔ Ricardo del mismo día (2026-05-26). El re-run no fue ceremonia — la nueva intel cambió el panorama en 6 dimensiones materiales.

**Lo nuevo desde la conversación 2026-05-26 (vs. estado de session 5):**

| Dimensión | Estado session 5 (2026-05-19) | Estado session 19 (2026-05-26) |
|---|---|---|
| **Decisor real** | Hector Leyva (asumido) | **REFUTADA** — **María Helena** (mano derecha de Héctor y madre de Andrea, cada vez más involucrada operativamente). Hector = fundador presente, NO decisor. NOTA: María Helena NO es esposa de Héctor ni co-propietaria; es empleada de máxima confianza. |
| **Estructura de control** | Andrea = influenciadora; Hector firma | Andrea filtra → madre decide → Hector valida. 3 voces, 3 criterios. |
| **Señal de presupuesto** | MEDIO (USD 15-40K pilot inferido) | **MEDIO-ALTO** (USD 30-80K pilot + USD 5-15K/mo retainer). Fundamento: USD 1M+ inversión china reciente para 10 trucks. |
| **Madurez digital** | 2/5 (basado en presencia exterior) | **1.5/5** (Andrea mostró pantalla — operativo interno casi 100% manual). |
| **Awakening event** | Hipótesis: Reforma 2026 + presión competitiva | **Confirmado**: el **esposo de Andrea trabaja en empresa de logística automatizada en San Diego**. Andrea ve el contraste a diario. Ancla aspiracional pre-existente. |
| **Pain point #1** | Hipotético (back-office aduanal) | **CONFIRMADO en pantalla**: Excel → PDF imprimible para CBP, exacto al segundo. Anchor visible + cuantificable + alto stakes. |

**Reunión formal 3-personas pendiente.** La reunión 2026-05-25 originalmente planeada NO ocurrió en esa fecha. En su lugar, hubo una conversación informal corta (Andrea ↔ Ricardo) que entregó la intel. La **reunión formal** con los 3 asistentes (Andrea + madre + Hector) sigue **PENDIENTE** — sin fecha confirmada aún. Ricardo agenda con Andrea (probablemente WhatsApp).

**Re-corrida pipeline ejecutada (paths a outputs):**

- `00_intake/research_input.md` — actualizado con sección "Update 2026-05-26 (post-conversación con Andrea)" supersediendo estimaciones previas.
- `00_intake/our_hypotheses.md` — actualizado con sección "Update 2026-05-26 (revisiones post-conversación)" supersediendo decisor / presupuesto / tono / hipótesis.
- `01_company_analysis/runs/2026-05-26_mode-a/` — Skill 01 **full re-run**. `final_report.md` (12 secciones, ~5000 palabras, integra los 6 cambios materiales) + `Trixx_AnalisisCompania_20260526.docx` (83 KB).
- `02_industry_analysis/runs/2026-05-26_mode-a/` — Skill 02 **refresh** con update note (sector sin cambios materiales en 8 días). `LogisticaCrossBorder_MX_20260526.md` + `.docx` (85 KB).
- `03_competitor_analysis/runs/2026-05-26_mode-a/` — Skill 03 **refresh** con update note (competidores sin cambios; husband-SD-company añadido como benchmark aspiracional NO competidor). `Trixx_Competencia_MX_20260526.md` + `.docx` (80 KB).
- `04_prep_llamada/runs/2026-05-26_mode-a/` — Skill 04 **completamente nuevo PrepLlamada** calibrado a 3-audience dynamic + 9-eslabón process map + no-solution-today directive. `Trixx_PrepLlamada_20260526.md` (~6500 palabras) + `.docx` (84 KB).

**4 PDFs renderizados en `/home/ricardo/Desktop/`:**
- `Trixx_AnalisisCompania_20260526.pdf` (355 KB)
- `LogisticaCrossBorder_MX_20260526.pdf` (434 KB)
- `Trixx_Competencia_MX_20260526.pdf` (357 KB)
- **`Trixx_PrepLlamada_20260526.pdf` (389 KB) ← deliverable primario para la reunión formal**

**PrepLlamada 2026-05-26 — estructura nueva:**
- §0 Contexto operativo (3-audience matrix + tactical do's/don'ts + estado factual ultra-rápido)
- §1-3 Empresa / sector / posición competitiva (refresh 5-min)
- §4 Guía de preguntas (4.0 apertura relacional → 4.1 mapeo cadena 9 eslabones [cotización → booking → docs CBP → dispatching → cruce → recepción → última milla → facturación → comms] → 4.2 deep dive Excel→PDF CBP → 4.3 catálogo otros procesos manuales → 4.4 stack tecnológico → 4.5 estructura decisión + horizonte → 4.6 inversión china + expansión flota → 4.7 Reforma 2026 awareness)
- §5 Game-changers (5 preguntas, usar 2-3)
- §6 Checklist final (operativo + estratégico + emocional)
- §7 Red flags + respuestas calibradas
- §8 Quick-win probes (mental para Ricardo, NO surfacing al cliente hoy)
- §9 Cierre + next steps + materiales

**Toolchain validado operacional en `ricardo-desktop`:** 5/5 SKILL.md present + 5/5 en `.claude/skills/` + 5/5 en available-skills + DOCX renderers funcionando (skills/0[1-5]_*/scripts/generate_docx.py) + libreoffice DOCX→PDF pipeline funcionando.

**Calibración explícita para la reunión formal:**
- Information-gathering ONLY (no proponer solución hoy — directiva explícita Ricardo: *"I will not propose to them any solution today, I need to gather as much information as possible"*).
- 3 audiencias simultáneas con criterios distintos.
- NO mencionar Nuvocargo a menos que ellos lo nombren.
- NO mencionar defectos del sitio.
- NO comparar nosotros primero con husband-SD-company; si Andrea la trae, escuchar + profundizar + capturar nombre.
- SÍ anclar inicio en el legado de Hector (24 años, integración vertical hecha en casa).
- SÍ profundizar Excel→PDF CBP (Andrea ya lo abrió voluntariamente).

**Estado del cliente al cierre de session 19:** intake actualizado + pipeline re-corrida + 4 PDFs nuevos en Desktop + toolchain validado. Reunión formal 3-personas pendiente agendar. Próxima sesión: Ricardo subirá artifacts (recording + notas) post-reunión formal para alimentar Skill 05 (internal-report).

---

## Update 2026-05-19 (session 5) — Pre-meeting critical path CERRADO

**`our_hypotheses.md` llenado conjunto** (7 dimensiones ADR-027 slice 3). Frontmatter: `filled: 2026-05-19`, `filled_by: ricardo + claude`. Decisiones de juicio locked:
- **Decisor final:** Hector Leyva. Andrea es influenciadora ("voz joven/digital" interna), no decisora.
- **Presupuesto estimado:** USD 15-40K piloto + USD 2-5K/mes retainer. Inferido de proxies operacionales (24 años + 5 sedes + flota USDOT + 571,370 millas/año).
- **Tono:** mixto cercano + estratégico. NUNCA técnico profundo en primera reunión.
- **5 zonas sensibles:** patente aduanal con framing neutro; NO asumir consanguineidad Andrea-Hector; NO mencionar defectos del sitio; NO comparar directo con Nuvocargo; NO empujar Hoja de Ruta de IA en primera reunión.
- **9 hipótesis a confirmar/refutar en reunión:** decisor único, no-consultor-IA-previo, "más" = back-office aduanero, no-awareness Nuvocargo, patente propia, Reforma 2026 preocupa, Andrea puede empujar adentro, volumen 150-350/mes northbound, mix 50/50 vs 80%+ chino.
- **Riesgos comerciales:** Hector "esto puede esperar" + Andrea pierde fuerza interna + competidor familiar tech + decisión postpuesta por temporada alta.

**Skill 04 (discovery-meeting) ejecutado.** Output en `04_prep_llamada/runs/2026-05-19_mode-a/`:
- `Trixx_PrepLlamada_20260519.md` (26 KB, ~6,500 palabras)
- `Trixx_PrepLlamada_20260519.docx` (75 KB, brand Aurora)

**Estructura del documento:**
- Sección 1 — empresa en 5 min con tabla de números clave + 3 señales de alerta previas
- Sección 2 — sector en 3 min con 5 términos clave (TIGIE, Pedimento, Carta Porte 3.1, OEA, Responsabilidad solidaria 2026)
- Sección 3 — posición competitiva simplificada (Nuvocargo + Integración Aduanal + TCI; gap clave = portal cliente + IA adoptada + certificaciones)
- Sección 4 — **4.0 NUEVA: apertura relacional (primeros 5 min)** + 4.1 operación aduanal core + 4.2 comunicación cliente/tracking + 4.3 cotizaciones + 4.4 documentación + reforma 2026 + 4.5 marketing + 4.6 stack actual + 4.7 decisión
- Sección 5 — 5 game-changer emocionales (úsense 2-3 máx)
- Sección 6 — 10 objetivos checklist + lista de 9 hipótesis de `our_hypotheses.md` §6
- Sección 7 — red flags generales + 7 específicas a Trixx
- Notas operativas — tono, materiales, insumos Skill 05, tiempo 30 min, cierre sugerido

**Calibración explícita aplicada:** discovery relacional + relationship-building, NO auditoría técnica (per directiva session 4). Sección 4.0 nueva (apertura relacional con preguntas sobre cómo entró Andrea + narrativa del fundador Hector + evento detonante) ANTES de cualquier sondeo operativo. Patente aduanal preguntada con framing neutro. Comparación con Nuvocargo solo si ellos abren. Cierre sugerido sin empujar Hoja de Ruta.

**4 PDFs entregados al Desktop de Ricardo:**
- `/home/ricardo/Desktop/Trixx_AnalisisCompania_20260518.pdf` (368 KB)
- `/home/ricardo/Desktop/LogisticaCrossBorder_MX_20260518.pdf` (502 KB)
- `/home/ricardo/Desktop/Trixx_Competencia_MX_20260518.pdf` (410 KB)
- `/home/ricardo/Desktop/Trixx_PrepLlamada_20260519.pdf` (253 KB)

**Estado del cliente al cierre de session 5:** phase 0 del pipeline COMPLETA. Listos para la reunión 2026-05-25 1pm Tijuana. Pendiente: la reunión misma + grabación + post-reunión Skill 05.

---

## Sesión 4 (2026-05-18 PM) — narrativa original abajo

---

**Updated:** 2026-05-18 (PM, session 4)
**By:** ricardo (via Claude Code at /srv/Nexostrat/)
**Persona:** Client-Owner

## What just happened

Cliente scaffolded vía `infra/scripts/new-client.sh` con `pilot=true`. Intake llenado a partir del WhatsApp inicial de Andrea Chávez (referido vía Sofía Estavilo) + URL del sitio oficial enviada por la contacto. Comunicación inicial archivada en `communications/2026-05-18_initial-contact.md` con extracción de señales factuales + análisis del trade-off de pre-encuesta (decisión: no enviar formulario; alternativa = WhatsApp ligero a Andrea preguntando audiencia de la reunión).

**Estado factual locked:**
- Marca: Trixx Logistics (dos X — sitio oficial). LinkedIn corporativo usa una X (anomalía).
- País: México. Sede operativa de la contacto: Tijuana.
- +20 años de operación (cita verbal de la contacto).
- Auto-percepción: *"muy atrás en programas y tecnología"* (cita textual).
- Intención inicial: *"automatizaciones y más"*.
- Contacto principal: Andrea Chávez (+52 1 664 533 3512). Trabaja con su "tío" (dueño, en sentido tijuanense — relación familiar real por confirmar). Madre también trabaja en la compañía.
- Audiencia de reunión: no confirmada.

## In flight — concrete next action

**Skill 01 (company-analyst) COMPLETADO 2026-05-18 PM.** Outputs:
- `01_company_analysis/runs/2026-05-18_mode-a/final_report.md` (35 KB, 13 secciones completas con etiquetas ✅/⚠️/❓)
- `01_company_analysis/runs/2026-05-18_mode-a/Trixx_AnalisisCompania_20260518.docx` (80 KB)

**Hallazgos de Skill 01 que cambian el mapa:**
- ⚠️ LinkedIn `linkedin.com/company/trix-logistics/` es de empresa UK distinta (Leicester, 4 empleados, paquetería). Trixx MX **no tiene página corporativa LinkedIn**.
- ✅ Fundación 2002 (24 años — coherente con +20 verbal de Andrea).
- ✅ 5 sedes (descubierta CDMX adicional a TJ/GDL/Vernon/SD).
- ✅ Dos entidades legales: Trix Importaciones Comerciales S. de R.L. de C.V. (MX) + Trixx Logistics Corp (US).
- ✅ Dueño identificado: Hector Leyva.
- ✅ USDOT 2045279 activo, flota 12 trucks + 9 drivers, 0 crashes 24m, OOS rates mejores que media nacional.
- ⚠️ Patente aduanal NO expuesta públicamente — señal a verificar.
- ⚠️ Sitio con bugs en producción ("0 Años" + fish-species placeholder en /home-logistic/).
- ✅ Madurez digital 2/5 confirmada (coherente con auto-evaluación de Andrea).

**Siguiente:** revisión humana de Ricardo del .md → si OK → Skill 02 (industry-analyst) sobre logística cross-border MX-USA / agencia aduanal.

**Update 2026-05-18 PM continuación:** Ricardo revisó Skill 01 .md, marcó 3 correcciones (contador "0 Años" es animado JS no bug, página /home-logistic/ no enlazada en nav principal, página /contacto/ sí tiene click-to-WhatsApp + iconos sociales). Correcciones aplicadas al .md + .docx regenerado. Memoria `feedback_animated_counters_not_bugs.md` guardada para evitar el patrón en futuros clientes. Task #6 abierta para Skill 04: calibrar nivel de preguntas (las de Skill 01 se sintieron muy técnicas para primera reunión — Ricardo prefiere discovery abierto + relationship-building, no auditoría técnica).

**Skill 02 COMPLETADO 2026-05-18 PM.** Outputs:
- `02_industry_analysis/runs/2026-05-18_mode-a/LogisticaCrossBorder_MX_20260518.md` (10 secciones, ~5,500 palabras, 40+ fuentes)
- `02_industry_analysis/runs/2026-05-18_mode-a/LogisticaCrossBorder_MX_20260518.docx` (83 KB)

**Hallazgos de Skill 02 que importan para la reunión:**
- Sector mexicano de autotransporte de carga = 3.8% PIB nacional, USD 92B mercado 2025 → USD 141B 2034 (CAGR 4.41%)
- Pero PIB sectorial estancado en 2025 (+0.02%); el nicho cross-border Tijuana sí está creciendo (+8% YoY freight)
- Reforma Ley Aduanera vigor 1-ene-2026: patentes ya no vitalicias, responsabilidad solidaria del agente, certificación cada 3 años
- Carta Porte 3.1 multas $850-$53,650 MXN + cárcel 3-6 años por contrabando presunto
- USMCA Review decisión 1-jul-2026
- IA aduanera mexicana ya tiene 5 players activos (AduanApp 95% precisión 7-13s, Taxer 56% ahorro tiempo, Moco AI, Camtom, Experta) — early-adopter window 18-30 meses
- **Competidor real de Trixx no son los agentes locales — es Nuvocargo** (USD 74M funding, US-MX foco, expandió 2024 a todos los crossings)
- Trixx = Arquetipo A (dueño-operador), no Arquetipo B (corporativo) — lenguaje matters

**Siguiente:** revisión humana Skill 02 → si OK → Skill 03 (competitor-analyst) profundizando contra Nuvocargo + agentes locales TJ + AduanApp ecosystem.

**Skill 03 COMPLETADO 2026-05-18 PM.** Outputs:
- `03_competitor_analysis/runs/2026-05-18_mode-a/Trixx_Competencia_MX_20260518.md` (8 secciones, ~5,200 palabras)
- `03_competitor_analysis/runs/2026-05-18_mode-a/Trixx_Competencia_MX_20260518.docx` (78 KB)

**Hallazgos de Skill 03:**
- 5 competidores directos mapeados: Nuvocargo (USD 74M, AI-native, target 150-350 envíos/mes — EXACTO segmento Trixx), Flexport (e-commerce fulfillment dobló en 60 días post-tarifas 2025, AI auditor 0.2% error), TCI (+30 años, modelo espejo de Trixx sin tech), Integración Aduanal (OEA + ISO + patente 3743 visibles), Grupo Aduanal Arellano (chico, sin certs).
- 5 indirectos: Estafeta, DHL Supply Chain MX, Solistica, AduanApp (herramienta o competencia según ángulo), Aispuro Lavenant (sitio "en construcción" actualmente).
- Posición de Trixx en mapa: empata o gana contra locales (TCI, Arellano, Aispuro); pierde marcadamente contra tech-enabled (Nuvocargo, Flexport) en 5 dimensiones críticas (portal cliente, IA adoptada, madurez digital, certificaciones, funding).
- Las primeras 3 dimensiones son atacables en 6-12 meses con Nexostrat; las 2 últimas son estructurales.
- **5 talking points calibrados a primer encuentro** (sin profundidad técnica, basados en feedback de Ricardo sobre Skill 01): Nuvocargo como urgencia, diferenciadores ya en sitio (chino + multi-sede), trampa de responsabilidad solidaria 2026, gap silencioso de tracking, ventana de 18-30 meses.

**Siguiente:** revisión humana Skill 03 → si OK → Skill 04 (discovery-meeting / PrepLlamada). Antes de Skill 04, llenar `00_intake/our_hypotheses.md` (juicio: dolor, decisor, presupuesto, tono, capability-fit). PrepLlamada es el primer skill que SÍ lee our_hypotheses.md per ADR-027.

## Blocked on

Ninguno crítico para Skill 01. Pendientes paralelos:
- Sección 6 de research_input.md (audiencia de la reunión) — se cierra cuando Andrea confirme vía WhatsApp.
- `our_hypotheses.md` — sin tocar; se llena antes de Skill 04.

## Open questions

1. Spelling: Skill 01 confirma si LinkedIn `trix-logistics` (una X) es la grafía corporativa real o un artefacto del handle. El sitio oficial usa dos X.
2. Identidad del "tío" dueño de la compañía — Skill 01 puede mapearlo desde LinkedIn / DENUE.
3. RFC, año exacto de fundación, certificaciones (C-TPAT / OEA esperables en logística cross-border) — todas a investigar por Skill 01.

## Files modified but not yet committed

- `state.json` (NEW — vía scaffold)
- `checkpoint.md` (este archivo)
- `README.md` (NEW — stub per-cliente del scaffolder)
- `00_intake/research_input.md` (NEW + llenado con datos de primera mano del WhatsApp)
- `00_intake/our_hypotheses.md` (NEW — sin llenar todavía, sellado hasta Skill 04)
- `communications/2026-05-18_initial-contact.md` (NEW — transcripción + análisis)
- `01_company_analysis/.gitkeep` y demás stages (NEW — vía scaffold)

## Estimated time to finish

- Skill 01 + revisión humana: ~30-45 min.
- Skill 02 + revisión: ~30 min.
- Skill 03 + revisión: ~30 min.
- our_hypotheses.md (operador): ~15-20 min.
- Skill 04 (PrepLlamada): ~20 min + revisión.
- **Total a Monday 2026-05-25:** ~2.5-3h de sesión efectiva, distribuible entre hoy y el lunes en la mañana.

## After this, what's next

Reunión 2026-05-25 1pm Tijuana en oficina de Andrea. Llevar PrepLlamada (Skill 04 output) como guía. Grabar reunión. Post-reunión → Skill 05 (Opportunity Report) → revisión obligatoria Ricardo+JP (Fase 5) → entrega manual (Fase 6).
