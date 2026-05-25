# Website Intro V3 — Design Spec

> **Created:** 2026-05-25
> **Replaces:** V1.x and V2.x (single-shot talking head on white wall — see `edits/Intro V1.0…V2.mkv` and the critique in `Comentarios Video`)
> **Status:** Locked. Shoot day pending.
> **Author:** Ricardo + Claude (brainstorming session 2026-05-25)

---

## 1. Strategic frame (the locks)

| Lock | Decision |
|---|---|
| Goal | Convert a PYME director landing on `nexostrat.com` into a WhatsApp message. **Not** to "introduce Ricardo." |
| Promise | In ~45 seconds, viewer understands the problem we solve, gets one credible proof point, and sees one clear next step. |
| Tone | *Tranquilidad y competencia.* Consultant who has already solved this. Not a motivator. No fist, no pointing, no "vamos." |
| Single CTA | WhatsApp. Web + email are pulled out of the video and live on the page surrounding the video instead. |
| Length | **45s final.** Pre-launch and zero testimonials → defer the 60-75s "social-proof" structure to V4. |
| Language | Spanish only, neutral LATAM, *tú* register. |
| Speaker | Ricardo, single talking head. (Co-founder JP is referenced through the plural "nosotros" in the script but is not on camera at Stage 1.) |

## 2. Approach — "Anchor + Brand Wall" (Option A)

Selected after evaluating four backdrops + a chroma-key composite alternative. The TV mounted on the wall (Backdrop 02) becomes a brand-content panel — the **production-design half** of the message — synced to spoken script beats.

**Why not the alternatives** (one line each):
- *Wood backdrops 01 / 04* — read "closet at home"; do nothing to anchor the brand.
- *Balcony (03)* — strongest "boutique" feel but weather-dependent and harder to retake in one day.
- *White wall + chroma in Natron* — without a real green screen, one edit day cannot produce clean edges; output looks faker than a real backdrop.

## 3. Production system

```
[ Laptop ]─HDMI─►[ TV mounted on wall ]   ◄── camera frame: TV on left, Ricardo on right third
   │                                          (TV brightness 30-40%, color "Cinema")
   │
   ▼
[ Browser fullscreen → tv-loop/index.html ]
   │                            ▲
   │                            │ Space-bar presses advance the slide deck.
   │                            │ Source of truth: SCRIPT.md (5 cues).
   ▼                            │
[ Camera = phone, landscape, tripod, eye level, 1.5m subject distance ]
                                │
[ Audio: lavalier hidden under shirt, transmitter on belt ]   ──┐
                                                                ▼
[ Bluetooth presenter clicker mapped to Space/PgDn ]  ◄── operator holds in hand
```

The deck **and the take are recorded together in one frame** — sync happens in-camera, not in post. This is the design innovation that makes the V3 shoot day affordable.

## 4. Script (locked)

See [`tv-loop/SCRIPT.md`](tv-loop/SCRIPT.md) for the canonical, annotated, prompter-ready version. Summary:

- 5 SPACE-press cues, each opening a new slide
- ~38-45s of spoken Spanish across five beats: Hook · Solution (auto-revealed stair labels) · Proof · Differentiation · CTA
- Pre-roll 5s silence on logo card, post-roll 5-10s silence on CTA card

## 5. TV slide deck

See [`tv-loop/index.html`](tv-loop/index.html). Six slides on Midnight `#0C1A2E` background, type in Arctic White `#F0FBFF`, hero numbers + accents in Sky Blue `#0EA5E9`:

| # | Slide | What it shows |
|---|---|---|
| 0 | Cover (pre-roll) | Wordmark + `nexostrat.com`, left-anchored |
| 1 | Hook | "¿Cuántas horas pierde tu equipo?" + animated 1→20 counter + filling progress bar |
| 2 | Stairs | Three pills auto-reveal in a staircase: **Estudiamos** (bottom-left, 0.3s) · **Identificamos** (middle, 3.5s) · **Implementamos** (top-right, 8.0s). Dashed connector fades in once all three are present. |
| 3 | Proof | "**8–20 hrs**" hero number + "horas recuperadas / semana" |
| 4 | Diferencia | "Hecho **a tu medida.**" + "Sin plantillas · sobre cómo funciona tu negocio" |
| 5 | CTA | WhatsApp icon + **+57 333 286 3969** + "30 minutos · sin costo" |

**All content sits in the left 60% of the canvas** so Ricardo standing on the right third of the camera frame never covers it.

**Keyboard controls** (inside the deck):

| Key | Action |
|---|---|
| Space / → / PgDn | Next station |
| ← / PgUp | Previous |
| Home | Reset to Slide 0 |
| F | Toggle fullscreen |
| G | Toggle rule-of-thirds grid (framing aid) |
| R | Toggle rehearsal HUD |
| H | Show cursor (hidden by default) |
| 0–5 | Jump directly to slide N |
| Click | Also advances (fallback) |

## 6. Shoot-day setup

### Room
- Close all blinds/curtains behind camera (TV reflects them)
- TV brightness 30–40%, color mode "Cinema" or "Standard" (never "Vivid")
- Disable laptop screen blanking: `xset s off ; xset -dpms`

### Camera
- Phone landscape, on tripod, lens at Ricardo's eye level
- Ricardo in **right third** of frame; TV in **left two-thirds**
- Subject distance ~1.5m, chest-up framing, head above TV's top edge

### Lighting
- Key: camera-left window light at 45°, diffused (sheer curtain)
- Fill: white wall/foamcore bounce on camera-right
- TV is *not* lit directly — it is its own light source

### Audio
- Lavalier under shirt, capsule on inside of placket, cable down inside, transmitter on belt
- Record 10s of room tone before first take (noise-floor sample for cleanup)
- Phone or audio recorder; clap at start of each take to sync if separate

### Wardrobe
- Navy or charcoal blazer · solid white or light-blue shirt buttoned to top · **no tie**
- Hair styled, not slicked

### Take protocol
- 6+ full takes with inflection / pause variation
- Then isolated takes of each beat (hook only, CTA only, etc.) as cutaway insurance
- Slate aloud before each take

## 7. Edit plan (1 day in DaVinci Resolve)

**Timeline (45s):**
1. `0:00–0:01` — fade from black, music in at -18dB
2. `0:01–0:43` — talking head with TV slides
3. `0:01` — lower-third "Ricardo Mejía · Co-fundador, Nexostrat" for 4s
4. `0:43–0:45` — fade to black, music tail, CTA slide still on TV through the fade

**Color:** mild grade — skin warmth +3, overall saturation -8, cooler shadows. Keep TV reading cool/cyan vs. skin warm — that contrast is what makes a frame feel produced.

**Music:** `assets/leberch-corporate-509707.mp3` (slower, sparser — "consultancy" rather than "upbeat"). Cut a 45s segment; keyframe down to -24dB during speech, back to -18dB on pre/post-roll. Sidechain not worth the time.

**Export:**
- Master: H.264 MP4, 1080p30, ~12 Mbps, AAC 192 kbps stereo — `~/srv/Nexostrat/.../final/intro-v3-master.mp4` (~70 MB)
- Web-optimized: 1080p30 at 6 Mbps, `-movflags +faststart` for `<video preload="metadata">`

**Run through `infra/scripts/video-to-mp4.sh`** if exporting MP4 directly from DaVinci hits the codec-gap blocker (session 12's fix).

## 8. What changed vs. V1 / V2 (Comentarios audit responses)

| Comentarios critique (V1/V2) | V3 response |
|---|---|
| White wall background kills credibility | TV brand-wall replaces white wall; brand content on TV behind subject |
| Lavalier visible | Lavalier hidden under shirt placket |
| End-card with 3 CTAs paralyzes prospect | Single CTA (WhatsApp). No separate end card — final frame holds on CTA slide on TV |
| Logo inconsistency intro vs. outro | Single wordmark variant used throughout; one logo lock-up |
| Aggressive gestures (puño, pointing) | Hands lower in frame; consultant posture |
| No text overlays for sound-off viewers | TV slides ARE the text overlays — designed for mobile autoplay-muted |
| Script opens with "Soy Ricardo Mejía" | Opens with prospect's pain ("¿Cuántas horas…") — viewer's problem, not our intro |
| "Nuestros clientes recuperan…" claim with zero clients | "**La meta:** recuperar…" — honest projection until Stage 1 has testimonials |
| "Sin compromiso" sounds like a used-car pitch | "Sin costo" only — drops the trigger phrase |

## 9. File map

```
operations/marketing/website-intro/
├── INTRO_V3_DESIGN.md          ← this file
├── Comentarios Video           ← original CMO critique (V1/V2 audit)
├── Backdrop 01..04.jpeg        ← backdrop options considered (#02 chosen)
├── tv-loop/
│   ├── index.html              ← the deck (6 slides, keyboard-driven)
│   ├── SCRIPT.md               ← annotated spoken script + SPACE cues
│   └── assets/
│       ├── icon.png            ← Nexostrat brand mark (top-right of content slides)
│       └── wordmark.png        ← Full wordmark (Slide 0 cover)
├── assets/                     ← shared assets (logos, music, ODP source files)
├── raw/                        ← raw camera takes (DNxHR HQ in raw/transcoded/)
├── edits/                      ← V1.x / V2.x DaVinci timelines (legacy)
└── final/                      ← final exported deliverables (V3 will land here)
```

## 10. V4 — when to revisit

Re-open this design when **any of these are true**:
- Stage 1 has shipped and 2+ client testimonials exist → 60-75s structure with social proof becomes viable
- The site analytics show a sub-2% click-through-to-WhatsApp from the hero video → re-test hook / CTA wording
- The brand palette is refined (current Midnight/SkyBlue is locked; if revisited, propagate before re-shooting)
- New shoot location available (rented office, proper studio backdrop) → revisit Approach C (full multi-shot production) discarded in V3

Until any of those, V3 is the canonical hero video.
