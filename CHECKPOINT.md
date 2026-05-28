# CHECKPOINT — root (Founder)

**Updated:** 2026-05-27T18:20:00-07:00
**By:** ricardo (via Claude Code session 22; evening on `ricardo-hp-laptop`)
**Persona:** Founder
**Session topic:** Marketing maintenance — Intro V5 declared FINAL webpage version + new shoot ingest. Two ffmpeg transcodes (today's raw take HLG→DNxHR for DaVinci + V5 ProRes master → web MP4). CEO title locked on Ricardo's V5 lower-third. No architecture changes, no ADRs, no Gemini handoff. Short session (~10 min wall-time).

## What just happened (last session — read once, don't re-litigate)

**Sesión 22 (2026-05-27, ~10 min wall-time, evening, immediately after session 21's pipeline-redesign brainstorm).** Ricardo dropped two video conversion requests in sequence, each closing a long-running thread:

**1. New shoot ingest.** Today's phone take `raw/PXL_20260528_003128365.mp4` (Pixel 10 Pro XL, 4K30 HEVC Main 10, BT.2020/HLG HDR, 51.87s, 4.3 GB) → `raw/transcoded/PXL_20260528_003128365.mov` using the locked HLG→BT.709 tonemap recipe from session 14 (the recipe that fixed Ricardo's "color shift" complaint in V3 production). Output: DNxHR HQX 10-bit yuv422p10le, BT.709, 5.3 GB. Color metadata verified `bt709/bt709/bt709/tv`. DaVinci-importable with correct color interpretation (no washed-out / hue-shifted artifacts that plagued the pre-session-14 8-bit pipeline). Used `ffmpeg -vf "zscale=transfer=linear:npl=100,format=gbrpf32le,zscale=primaries=bt709,tonemap=hable:desat=0,zscale=transfer=bt709:matrix=bt709:range=tv,format=yuv422p10le" -c:v dnxhd -profile:v dnxhr_hqx ...` end-to-end.

**2. V5 master → web MP4.** Ricardo's DaVinci-rendered V5 master `edits/Intro V5.mkv` (ProRes 1080p30 BT.709 + PCM 24-bit, 57s, 1.4 GB) → `edits/Intro V5.mp4` (H.264 High + AAC 192k + faststart, 26 MB) via `infra/scripts/video-to-mp4.sh` (the May-23 wrapper, CRF 18 / preset slow defaults). 53× compression with visually-lossless quality on talking-head footage. Ricardo declared **V5 is the final webpage version** — closes the V1/V2/V3 candidate sweepstakes open since session 11. **CEO title confirmed**: Ricardo = CEO + public face of Nexostrat (V5 lower-third "Ricardo Mejía / CEO" stands as approved). JP's reciprocal role (CTO? Co-fundador?) is a future Ricardo↔JP conversation.

**3. Session-end artifacts.** Journal + STATUS prepend + tasks.json (3 closed) + CHECKPOINT (this file) + commit + push. Only 4 small text files in the commit; all 4 heavy video files (raw, transcoded, mkv master, mp4 export) verified gitignored.

## Decisiones locked esta sesión

1. **Intro V5 is the website hero video** (final, not a candidate). Supersedes V1.0/V1.1/V1.2/V3 as the canonical homepage video.
2. **Ricardo is CEO + public face of Nexostrat.** The "Ricardo Mejía / CEO" lower-third in V5 is approved and ships to the homepage.
3. **JP's reciprocal title deferred** to a future Ricardo↔JP conversation. Won't block the V5 deploy because the V5 video only features Ricardo's title.
4. **Wrapper-default recipe (`video-to-mp4`) is the standard** for web export. CRF 18 / preset slow / AAC 192k / faststart. CRF 0 mathematical losslessness is overkill for web (~1 GB output for ~50s of 1080p) and not pursued.
5. **HLG→BT.709 tonemap recipe (session 14) is the canonical Pixel-phone ingest** path. Used verbatim today; producing correct color metadata reliably.
6. **No tasks created for the two soft follow-ups** (move V5.mp4 into `final/` per README; ROLES.md CEO/CTO amendment). Both noted in this CHECKPOINT for the next session to surface naturally if relevant.

## Stack state (live & verifiable next session)

```
/srv/Nexostrat/
├── 00_META/
│   └── journal/
│       └── 2026-05-27_intro-v5-final-transcode.md          ← NEW (this session, ~80 lines)
├── operations/marketing/website-intro/
│   ├── raw/
│   │   ├── PXL_20260528_003128365.mp4                      ← gitignored (today's shoot, 4.3 GB)
│   │   └── transcoded/
│   │       └── PXL_20260528_003128365.mov                  ← NEW gitignored (5.3 GB DNxHR HQX)
│   └── edits/
│       ├── Intro V5.mkv                                    ← gitignored (1.4 GB ProRes master, pre-existing)
│       └── Intro V5.mp4                                    ← NEW gitignored (26 MB web export — the final webpage video)
├── tasks.json                                              ← MODIFIED (3 closed; updated timestamp 18:20 PT)
├── STATUS.md                                               ← MODIFIED (session-22 entry prepended)
└── CHECKPOINT.md                                           ← THIS FILE (rewritten)
```

## Open items (carried forward — esta sesión cerró 3, no abrió ninguna)

**Tasks cerradas esta sesión (3):**
- `t-intro-v3-ceo-vs-cofundador` — closed 2026-05-27 (CEO confirmed; was overdue 1 day)
- `t-intro-v3-diferencia-slide` — closed 2026-05-27 (V5 final = accepted; was overdue 1 day)
- `t-intro-v3-web-export` — closed 2026-05-27 (Intro V5.mp4 IS the export; was due 2026-06-15, closed 19 days early)

**Soft follow-ups (NOT tracked as tasks):**
- **Move `edits/Intro V5.mp4` → `final/Intro V5.mp4`** per `operations/marketing/README.md` convention. Local mv only; both paths are gitignored. Next session can offer this; or the website-deploy session can grab from wherever.
- **`00_PARTNERSHIP/ROLES.md` CEO/CTO amendment.** Currently doesn't designate titles between Ricardo + JP. Now that Ricardo's CEO is publicly committed via the homepage video, ROLES.md should eventually catch up. Process: deliberate addendum to the 2026-05-12 signed legal artifact (per "prefer architecture over ceremony" + the partnership-doc precedent). Needs JP's reciprocal title decision first. Non-blocking.
- **Drive 2TB backup of new heavy assets** (5.3 GB DNxHR mov + 26 MB V5 mp4 + 1.4 GB V5 mkv + 4.3 GB raw mp4 = ~11 GB net new). No firm schedule.

**Tasks carried forward (de sesiones previas, unchanged this session):**

| ID | Subject | Priority | Due |
|---|---|---|---|
| `t-skill6-jp-feedback-await` | Esperar feedback JP sobre spec + deck | high | 2026-06-03 |
| `t-skill6-implementation-plan` | Invocar writing-plans para Fases A-H | high | tras feedback JP |
| `t-skill5-rename-and-reprofile` | Rename 05_opportunity_report → 05_internal_report | high | tras feedback JP |
| `t-skill6-build-skeleton` | Construir skills/06_client_deliverables/ | high | tras feedback JP |
| `t-skill7-placeholder-spec` | Crear skills/07_implementation_roadmap/SKILL.md placeholder | medium | tras feedback JP |
| `t-clients-folder-rename` | Migrar reporte_oportunidades → reporte_interno | high | tras feedback JP |
| `t-meeting-transcription-protocol-doc` | Crear 00_META/protocols/meeting_transcription.md | medium | 2026-06-10 |
| `t-editorial-designer-fix-description` | Fix frontmatter editorial-designer | low | 2026-06-15 |
| `t-anthropic-license-decision-doc` | Documentar nota source-available | low | 2026-06-15 |
| `t-internal-deck-iteration-feedback` | Iterar HTML deck según feedback JP | medium | tras feedback JP |
| `t-plan-04-description-update` | Update Plan 04 description in master index | high | 2026-05-28 (due mañana) |
| `t-install-brand-fonts-laptop` | Install Inter + JetBrains Mono on laptop | high | 2026-05-30 |
| `t-migrate-pilotos-to-clients` | Migrate 3 test companies from Pilotos/ to pipeline/clients/ | medium | 2026-05-30 |
| `t-trixx-la-visit-schedule` | Agendar visita LA Vernon | high | 2026-06-15 |
| `t-trixx-refresh-final-report` | Refresh Skill 01 con correcciones del meeting 2026-05-26 | medium | 2026-06-05 |
| `t-nexostrat-telegram-account` (B19) | Procure firm Telegram account (gates P-H1) | critical | 2026-06-15 |
| `t-weekend-desktop-on-decision` (B16) | Weekend desktop-on schedule decision | high | 2026-06-15 |

**Cross-scope context:**
- No Gemini handoff open.
- No memos pending en `00_META/inbox/`.
- One untracked file from before this session (pre-existing, not authored here): `pipeline/clients/trixx-logistics/etapa_2_diagnostico/May 27 at 06-27.m4a` — Trixx audio, belongs to Client-Owner scope, leave for that persona.

## What next session opens onto

**Most likely trigger**: feedback from JP on the session-21 spec + HTML deck (the dominant open thread). Three paths per session-21's CHECKPOINT still apply:
1. JP aprueba sin cambios → invocar `superpowers:writing-plans` para Fases A-H.
2. JP pide cambios menores al deck → iterar HTML.
3. JP propone cambios estructurales al spec → re-abrir brainstorm.

**Less likely but possible triggers:**
- Website deploy / homepage launch pickup → would surface the V5.mp4 → final/ folder move + ROLES.md amendment as natural follow-ups.
- Plan 04 description update (due 2026-05-28) — would be the smallest open thread.
- Brand font install on laptop (due 2026-05-30) — short maintenance task.

> **Recomendación al próximo Claude:** abrir leyendo este CHECKPOINT + STATUS + journal `2026-05-27_intro-v5-final-transcode.md` (this session) + journal `2026-05-27_skill6-pipeline-redesign-brainstorm.md` (session 21 — the dominant open thread). If Ricardo abre con feedback JP on the pipeline redesign, pivot directly to `t-skill6-implementation-plan` (writing-plans). If abre con un tema de marketing/website, the V5 finalization is fresh context. If abre vacío, ofrecer (a) las 3 tareas no-bloqueadas paralelas a feedback JP (transcription protocol, editorial-designer fix, license note), (b) the soft follow-ups noted above (V5.mp4 → final/ move + ROLES.md amendment), or (c) the small overdue/imminent items (Plan 04 desc 2026-05-28; brand fonts 2026-05-30).
