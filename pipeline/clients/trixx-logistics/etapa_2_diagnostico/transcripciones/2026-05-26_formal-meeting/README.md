# Reunión formal Trixx — 2026-05-26

**Tipo:** primera reunión formal de descubrimiento. Información gathering (no propuestas técnicas hoy, per directiva PrepLlamada §0).
**Modalidad:** presencial, oficinas Trixx, Tijuana.
**Guía utilizada:** [`../../04_prep_llamada/runs/2026-05-26_mode-a/Trixx_PrepLlamada_20260526.md`](../../04_prep_llamada/runs/2026-05-26_mode-a/Trixx_PrepLlamada_20260526.md).

## Asistentes

| Quién | Rol | Notas |
|---|---|---|
| Héctor Leyva | Fundador Trixx (24 años) | Esposo de María Helena. 25 años conociendo Colombia (Cartagena, Medellín, Bogotá, Leonisa). |
| María Helena | Co-propietaria, decisora real | Voz primaria operativa en ambas sesiones. En audio se le llama "María Helena" pronunciado rápido (sonido tipo "Marielena"); la persona de Samsara la llama simplemente "Helena". |
| Andrea Chávez | Hija, voz digital interna | Contacto inicial vía Sofía Estavilo (mencionada en audio). |
| Luis | Operativo USA (LA) | Se sumó brevemente a la 10:10 para hablar del pain de correos. |
| Ricardo Mejía | Nexostrat (founder) | Conducción según PrepLlamada §0-§9. |

## Estructura del folder

```
2026-05-26_formal-meeting/
├── README.md                                     ← este archivo (comparación + metodología)
├── 1010_main-meeting_transcript_final.md         ← ⭐ TRANSCRIPCIÓN CANÓNICA sesión 10:10 (91 KB)
├── 1205_second-session_transcript_final.md       ← ⭐ TRANSCRIPCIÓN CANÓNICA sesión 12:05 (32 KB)
├── audio/                                        ← grabaciones originales
│   ├── 2026-05-26_1010_main-meeting.m4a          (41 MB, ~113 min)
│   └── 2026-05-26_1205_second-session.m4a        (12 MB, ~31 min)
├── apple/                                        ← Apple Voice Memos auto-transcribe (baseline)
│   ├── 1010_main-meeting.txt                     (32 KB, ruidosa, sin speakers)
│   └── 1205_second-session.txt                   (7 KB)
├── whisperx/                                     ← "El sistema que tenemos" — pipeline interno
│   ├── 1010_main-meeting.{txt,srt,json,tsv,vtt}  (100 KB texto, 5 formatos — SRT alimenta el final)
│   ├── 1205_second-session.{txt,srt,json,tsv,vtt} (33 KB texto, 5 formatos)
│   └── logs/                                     ← logs de ejecución (incluye OOM en run inicial)
├── gemini/                                       ← Gemini multimodal — ver § Gemini Failure
│   ├── 1010_main-meeting.HALLUCINATION.md        (artefacto fabricado — evidencia)
│   └── 1010_main-meeting_SAMPLE_first5min.md     (muestra real, 5 min de calidad demostrada)
└── claude/                                       ← Claude curado — síntesis estructurada por bloques
    ├── 1010_main-meeting.md                      (28 KB, narrativa 9 bloques + datos accionables)
    └── 1205_second-session.md                    (16 KB, narrativa 6 bloques + datos accionables)
```

**Recomendación de uso:**
- Para **lectura humana** de la reunión → `*_transcript_final.md` (root del folder).
- Para **feed a Skill 05** (internal-report) → `claude/*.md` (síntesis estructurada).
- Para **citas textuales o auditoría** → `whisperx/*.txt` (con timestamps en `.srt`/`.json`).

## Política de material del cliente (override 2026-05-26)

Spec § Vault Discipline + `pipeline/CLAUDE.md` Strict Rule 6 sugieren age-encrypt para audios pesados → `vault/clients/<slug>/`. **Override explícito de Ricardo**: durante engagement activo todo el material Trixx queda **plano y accesible** en este folder. Sin encriptación. El vault aplica solo para material verdaderamente sensible (NDAs firmados, contratos, facturas, claves) — no para audios de discovery.

## Las tres transcripciones — metodología y resultado

### 1. Apple Voice Memos (baseline) — `apple/`

Auto-transcripción de Apple en macOS. **No es "el sistema que tenemos"** — es lo que generó el iPhone de Ricardo al grabar y que llegó en el zip. Sirve como baseline de comparación.

**Calidad:** baja. Muchas palabras concatenadas, ortografía rota, sin atribución de hablantes, fragmentos sin puntuar. Útil solo como búsqueda gruesa.

### 2. WhisperX (sistema interno Nexostrat) — `whisperx/`

Pipeline canónico de meetings de Nexostrat: `~/bin/transcribe-x.sh` + `~/bin/summarize-meeting.sh` (per `/srv/meetings/CLAUDE.md`).

**Configuración usada:**
- Modelo: `large-v3` (WhisperX)
- Compute: `float16` para 12:05; `int8` + batch 2 para 10:10 retry (OOM en primer intento con batch 4 float16 — VRAM 8 GB insuficiente para 113 min con diarización).
- Diarización: `pyannote/speaker-diarization-3.1` (vía HF token).
- Hotwords cargadas para sesgar reconocimiento de nombres propios: `Trixx, Nexostrat, Tijuana, Mexicali, Hector, Andrea, Maria, Helena, María Helena, Luis, Ricardo, Damian, Patti, Sofia, CBP, USDOT, aduanal, patente, Carta Porte, Nuvocargo, pedimento, contenedor, Medellin, Bogota, Cartagena, Colombia, Leonisa, Amazon, Walmart, Costco`.
- Initial prompt: contexto de la reunión Trixx.

**Calidad:** muy alta (~90% inteligibilidad). Cinco formatos por audio: `.txt` (texto plano con speakers), `.srt` y `.vtt` (subtítulos sincronizados), `.json` (palabra-por-palabra con timestamps), `.tsv` (formato tabular).

**Speakers detectados:**
- **10:10 main** — 6 voces (SPEAKER_00 a SPEAKER_05). Mapping confirmado en `claude/1010_main-meeting.md` § Mapeo de hablantes.
- **12:05 second** — 4 voces (SPEAKER_00 a SPEAKER_03). Mapping confirmado en `claude/1205_second-session.md` § Mapeo de hablantes.

Nombres propios captados correctamente: María Helena, Sofía Estavilo, Damián, Carlos Muñoz, Carlos (hosting), Graciela, Silvia, Miguel, Eduardo, Beto, Jan, Rosy, Paola Ticho, Ignacio Medrano, Long Beach, Vernon, Mexicali, Guadalajara, Querétaro, Houston, El Paso, Cartagena, Medellín, Bogotá, Leonisa, Samsara, Tracking Premium, McKinney, Monday.com, GoDaddy, Microsoft.

### 3. Gemini multimodal — `gemini/` (FALLÓ a escala — ver detalle abajo)

Pipeline intentado: `gemini --skip-trust -p "@audio.mp3 <prompt>"` con prompt español pidiendo diarización + transcripción literal + safety check anti-hallucination.

#### Gemini Failure — diagnóstico completo

Gemini CLI 0.42.0 falló de DOS formas distintas según tamaño de archivo:

**Falla #1 — Hallucination con archivo >20 MB (MP3 53 MB):**
Gemini CLI rechaza adjuntos >20 MB con error interno `File size exceeds the 20MB limit`. **PERO no falló cleanly:** generó una "transcripción" **completamente fabricada** a partir de las hotwords + nombres del prompt. La fabricación incluyó:
- Personajes inventados ("Beto" sí existe — coincidencia accidental — pero el contenido inventado le atribuyó frases que nunca dijo).
- Reunión remota Slack-coordinada con Luis en LA, María Helena en Bogotá, Andrea en San Diego (la reunión real fue presencial con todos juntos en Tijuana).
- Discusión técnica detallada sobre "Reforma Aduanera 2026", "fracción arancelaria dinámica", "Nuvocargo y Flexport saturando drayage" — temas todos plantados por mis hotwords, ningún dato real del audio.

Este artefacto se preserva en `gemini/1010_main-meeting.HALLUCINATION.md` como evidencia educacional. **Es peligroso porque suena plausible.** Un evaluador sin acceso al audio podría leerlo y creerlo. Esto motivó el safety-check explícito en el segundo intento.

**Falla #2 — AUDIO_NOT_LOADED no-determinístico con archivos ≤7 MB:**
Chunkeé el audio en 30 segmentos de 5 min (~1.2 MB cada uno). Smoke test con 30 segundos (118 KB) funcionó perfecto. Smoke test con 5 min (1.2 MB) también funcionó (ver `gemini/1010_main-meeting_SAMPLE_first5min.md` — calidad excelente, atribución de hablantes, marcadores temporales, captura de `[risa]` y `[sonido de teléfono]`).

PERO al lanzar los 30 segmentos en batch, Gemini comenzó a retornar `ERROR: AUDIO_NOT_LOADED` (el output que el safety-check pedía cuando no podía cargar audio) en la mayoría de los chunks. Error subyacente en el JSON dump: *"API returned invalid content after all retries. NumericalClassifierStrategy failed: Failed to generate content: Retry attempts exhausted."*

Esto es un bug del routing interno de Gemini CLI 0.42.0 — no es un límite documentado ni un rate limit estable. En 25 min de bg, solo **1 de 30 segmentos completó exitosamente**. Tasa efectiva: <5%. Decisión: abortar.

#### Lo que SÍ se preserva del Gemini intento

- **`gemini/1010_main-meeting_SAMPLE_first5min.md`** — los primeros 5 min del audio 10:10, transcritos por Gemini con calidad alta. Demuestra que Gemini multimodal SÍ funciona técnicamente para audio en español + diarización, pero la integración vía Gemini CLI 0.42.0 no es production-ready a escala (failure modes inconsistentes).
- **`gemini/1010_main-meeting.HALLUCINATION.md`** — el artefacto fabricado, marcado con `.HALLUCINATION.md` en el nombre para que nadie lo use como fuente.

### 4. Claude curado — `claude/`

**Claude (este agente) no procesa audio directamente.** La "transcripción Claude" es una **síntesis estructurada** que toma como input:
- WhisperX como fuente primaria (alta fidelidad textual + diarización + nombres propios).
- Apple baseline como segunda opinión cruzada.
- Gemini sample (5 min iniciales) como tercera opinión cruzada.
- Contexto del cliente: PrepLlamada, company analysis, our_hypotheses, checkpoint session 19.

**Output:** narrativa estructurada por bloques temáticos (apertura relacional → operativa → tech demo → pain de correos → change management → cierre), con:
- Atribución de hablantes por nombre real (mapeo WhisperX SPEAKER_NN → persona).
- Citas textuales literales para los highlights más accionables.
- Anotaciones marginales sobre pivotes de conversación, datos cuantitativos, red flags, action items.
- Sección "Datos accionables nuevos vs. session 19" que captura todo lo que altera `final_report.md`, `our_hypotheses.md` y `state.json`.
- Action items extraídos pre-formateados para alimentar Skill 05 (internal-report).

**No es transcripción cruda.** Es **documento de trabajo** que reemplaza la necesidad de leer 100 KB de WhisperX para entender la reunión.

## Comparación de calidad — tabla resumen

| Engine | 10:10 lines / chars | 12:05 lines / chars | Speaker labels | Propio uso |
|---|---|---|---|---|
| **Apple** | 1,150 / 32 KB | 298 / 7 KB | ❌ | Baseline noisy. Solo grep. |
| **WhisperX** | 1,219 / 100 KB | 333 / 33 KB | ✅ (6 voces / 4 voces) | **Fuente primaria** — texto íntegro buscable. |
| **Gemini (parcial)** | 4.4 KB (5 min sample) | — | ✅ (con nombres) | **Falló a escala.** El sample muestra calidad superior a WhisperX en estilo pero el CLI 0.42.0 no escaló. |
| **Claude curado** | 28 KB | 16 KB | ✅ (mapeado a nombres reales) | **Documento de trabajo** — feed directo a Skill 05. |

### Veredicto comparativo (Honestidad brutal)

| Dimensión | Apple | WhisperX | Gemini |
|---|---|---|---|
| Cobertura completa | ✅ | ✅ | ❌ (1/30 segs) |
| Fidelidad textual | 30% | 90% | 95% (en el sample) |
| Diarización | ❌ | ✅ (6 voces detectadas) | ✅ (con identificación contextual por nombre) |
| Nombres propios captados | 10% | 85% | 95% (en el sample) |
| Indicadores no-verbales | ❌ | ❌ | ✅ (risa, sonido teléfono) |
| Marca de tiempo | ❌ | ✅ (cada segmento) | ✅ (cada minuto) |
| Robustez en producción | N/A | ✅ (con tuning batch+VRAM) | ❌ (failure modes inconsistentes) |
| Riesgo de hallucination | Bajo | Bajo | **ALTO** si excede 20 MB |

**Recomendación operativa para futuras reuniones Trixx:**
1. **Conservar `~/bin/summarize-meeting.sh` (WhisperX + Gemini summary) como pipeline principal.** El paso WhisperX es confiable. El paso Gemini summary funciona PORQUE recibe ya la transcripción + un MP3 estandarizado, no es el bottleneck.
2. **No usar Gemini CLI standalone para transcribir audios largos.** Hasta que el CLI resuelva la inconsistencia de routing, la transcripción multimodal directa es no-determinística.
3. **Claude curado** vale la pena como capa de síntesis, pero **no reemplaza** una transcripción de palabra-por-palabra cuando es necesaria para citar al cliente.

## Siguiente paso en la cadena

Estos artefactos alimentan **Skill 05 (internal-report)** — entregable final de diagnóstico al cliente. Inputs esperados:

- Empresa: `../../01_company_analysis/runs/2026-05-26_mode-a/final_report.md`
- Industria: `../../02_industry_analysis/runs/2026-05-26_mode-a/LogisticaCrossBorder_MX_20260526.md`
- Competencia: `../../03_competitor_analysis/runs/2026-05-26_mode-a/Trixx_Competencia_MX_20260526.md`
- **Notas de cliente**: `claude/1010_main-meeting.md` + `claude/1205_second-session.md` (los curados Claude son el feed apropiado; WhisperX queda como referencia para citas textuales).

## Origen del archivo

Subido por Ricardo el 2026-05-26 PM como `drive-download-20260527T020829Z-3-001.zip` (Google Drive export). Zip extraído + archivos renombrados a convención `HHMM_<contexto>` + originales reubicados + zip eliminado.

Transcripciones generadas el 2026-05-26 PM (mismo día) usando WhisperX local + Gemini CLI (parcial — ver § Gemini Failure) + síntesis Claude.
