# Journal — 2026-05-25: Website Intro V3 — Redesign + Production System

**Session:** Thirteenth (driven from `/srv/meetings/nexostrat` cwd; work landed entirely on Nexostrat artifacts)
**Persona:** Founder (with Meetings Curator scope present but unused)
**Duration:** ~3 hours
**Inputs read:**
- `operations/marketing/website-intro/Comentarios Video` — original CMO critique of V1/V2
- `operations/marketing/website-intro/edits/Intro V2.mkv` — sampled at 4s intervals to confirm current state
- `operations/marketing/website-intro/Backdrop 01..04.jpeg` — four backdrop options Ricardo staged
- Brand logo PNGs from `operations/marketing/brand/logos/` — extracted Midnight `#0C1A2E` / SkyBlue `#0EA5E9` / Arctic `#F0FBFF` palette
- `operations/marketing/README.md` (video pipeline + folder convention)

## What this session was

Ricardo asked to "redesign the initial setup" of the homepage hero video — the video at `nexostrat.com`. V1.x and V2.x exist in `edits/` but failed the CMO audit captured in `Comentarios Video`. The session was end-to-end brainstorming → design → implementation of V3.

The work followed the superpowers `brainstorming` skill protocol: explore context → ask clarifying questions one at a time → propose 2-3 approaches → present design in sections → get approval per section → write spec + implementation only after approval. Ricardo drove most of the script and visual decisions; Claude drove the technical synthesis (brand color extraction, animation timing, slide layout, gitignore mechanics).

## Decisions locked this session

### 1. Approach A — "Anchor + Brand Wall"

After evaluating four backdrops Ricardo had staged (honey-wood with seam, wall-mounted TV, balcony with city/golf-course view, cleaner wood paneling) plus an alternative chroma-key-on-white-wall composite approach, **Backdrop 02 (wall-mounted TV) won**.

Rationale: the TV becomes a **brand-content panel** synced to the spoken script — it's the production-design half of the message, not just a backdrop. The white wall around the TV gives hair-edge separation (which dark wood backdrops don't). One-day-edit constraints killed the chroma-key option — without a real green screen, Natron edge artifacts would survive into the final cut.

The other backdrops were rejected for credibility-vs-effort reasons documented in `INTRO_V3_DESIGN.md` §2.

### 2. The HTML-deck-on-TV technique

Ricardo proposed the central technical idea: **the TV plays a keyboard-driven HTML slide deck during the take.** Ricardo holds a Bluetooth presenter clicker that maps to Space/PgDn; presses it at scripted moments while reading the spoken script off a teleprompter (Elegant Prompter). Sync happens **in-camera, not in post** — the TV slides are recorded as-is in every frame.

This is the design innovation that made V3 affordable: no compositing day, no green-screen-rotoscope work, no After Effects motion graphics. Just an HTML file + a clicker + a phone on a tripod.

Implementation lives at `operations/marketing/website-intro/tv-loop/index.html` — 15.9 KB, single self-contained file, zero build dependencies, runs from `python3 -m http.server` or directly via `file://`.

### 3. Slide content + animation choices

Six slides:
- **0 — Cover** (logo, left-anchored) — for pre-roll silence
- **1 — Hook** — animated 1→20 hour counter + filling progress bar (6s)
- **2 — Stairs** — three pills auto-revealing in a staircase: Estudiamos (bottom-left, 0.3s) → Identificamos (middle, 3.5s) → Implementamos (top-right, 8.0s) → dashed connector at 8.4s. **Single SPACE press for the whole slide** — pill timing tracks Ricardo's spoken pace.
- **3 — Proof** — hero "8–20 hrs" + "horas recuperadas / semana"
- **4 — Diferencia** — "Hecho a tu medida" + "Sin plantillas"
- **5 — CTA** — WhatsApp icon + `+57 333 286 3969` + "30 minutos · sin costo"

**Pill labels evolved.** First draft had "Estudiamos · Identificamos · Diseñamos". After Ricardo locked the final script, the third verb shifted to "Implementamos" — more concrete for PYME directors, and it lands on the spoken word "implementación." The visual stair order (Est bottom → Ident middle → Implem top) also matches the spoken-verb order in the final script, so reveal feels natural.

**Number animation** — first iteration had a static "20". After Ricardo's feedback, switched to JS-animated `1→20` over 6 seconds with eased-out interpolation. The progress bar fills 0→100% in parallel via CSS `@keyframes fillBar`. Both reset when the slide is re-entered.

**Layout discipline.** All content sits in the canvas's **left 60%** because Ricardo will be on the right third of the camera frame and would otherwise cover the slide. This was Ricardo's call after he visualized the framing.

### 4. Script rewriting

Original V1/V2 script ("Soy Ricardo Mejía, fundador de Nexostrat. Somos el nexo entre tu empresa y la estrategia de IA…") opened with self-introduction, which the Comentarios critique flagged as inversion error: the prospect doesn't care who you are until you've shown you understand their problem.

V3 final script (locked by Ricardo) opens with the prospect's pain:
> "¿Cuántas horas pierde tu equipo cada semana en tareas repetitivas? De esas que te quitan tiempo para crecer."

Then solution, proof, differentiation, CTA. ~38-45 seconds of speech, 5 SPACE-cue beats. Pre-launch-honest framing throughout — uses "La meta: que recuperes…" instead of "Nuestros clientes recuperan…" (zero clients exist yet; the projection is the projection).

Full annotated version with prompter cues at [`tv-loop/SCRIPT.md`](../../operations/marketing/website-intro/tv-loop/SCRIPT.md).

### 5. gitignore deviation

The marketing folder's `.gitignore` previously declared **everything except README.md** to be ignored — explicitly designed as a working-files-only tree. V3 introduces a deliberate exception: the HTML deck (canonical TV background, used during every shoot) and the design spec (source of truth for V3) are **tracked**.

Reasoning: these are not regenerable working files. The deck is the *physical artifact* played during the shoot; if lost, the shoot can't happen. The spec captures decisions that took 3 hours of strategy work to crystallize. Both are text + tiny PNGs (~40 KB total). No leak risk (no client data, no secrets). The exception pattern:

```
!website-intro/
website-intro/*
!website-intro/*.md
!website-intro/tv-loop/
!website-intro/tv-loop/**
```

Verified with `git check-ignore -v` and `git add --dry-run`. Other marketing assets remain ignored.

## Files created

- `operations/marketing/website-intro/tv-loop/index.html` — 6-slide deck (15.9 KB)
- `operations/marketing/website-intro/tv-loop/SCRIPT.md` — annotated prompter script
- `operations/marketing/website-intro/tv-loop/assets/icon.png` — copy of `brand/logos/Nexostrat_Icono_Monocromatico_Claro_Transparente.png` (7.4 KB)
- `operations/marketing/website-intro/tv-loop/assets/wordmark.png` — copy of `brand/logos/Nexostrat_Logo_Fondo_Midnight_Transparente.png` (28.6 KB)
- `operations/marketing/website-intro/INTRO_V3_DESIGN.md` — full design spec

## Files modified

- `operations/marketing/.gitignore` — added the V3 deck + spec exception
- `STATUS.md` — thirteenth-session entry at top + "Done this session" block
- `tasks.json` — superseded `t-pick-website-intro-final-version`; added `t-intro-v3-dry-run` (high · 2026-05-30), `t-buy-presenter-clicker` (low · 2026-06-05), `t-intro-v3-shoot-and-edit` (high · 2026-06-15)
- `CHECKPOINT.md` — baton rewritten for next session

## Open items

1. **Dry-run on real TV** (`t-intro-v3-dry-run`) — before any shoot day. Verify font legibility, TV reflection control, Slide 2 pill timing against natural speech pace. CSS tweak is a 30-second change if needed.
2. **Bluetooth presenter clicker** (`t-buy-presenter-clicker`) — $15-25, any Space/PgDn-mapping remote works. Test pairing with laptop before shoot day. Fallback: wireless mouse (deck advances on any click).
3. **Shoot + edit** (`t-intro-v3-shoot-and-edit`) — gated on the above two. Half-day shoot, one-day edit, export through `infra/scripts/video-to-mp4.sh` if DaVinci hits the MP4 codec gap.

## What didn't happen

- No memo to root or any other persona. The work stayed inside the Founder scope (`operations/marketing/`).
- No update to `00_META/CHANGELOG.md` — no persona context file (CLAUDE.md / GEMINI.md / README.md) was edited.
- No ADR. V3 is a marketing artifact, not an architectural decision.
- No commit yet — that lands at session-end, just after this journal is written.

## Reversal

If V3 underperforms and we want to revert to V1/V2 thinking: the legacy MKV/MP4 takes still live in `edits/`. V3 doesn't delete them. Reverting means moving V3 back to "deferred" status in `tasks.json` and re-opening `t-pick-website-intro-final-version` (or its descendant). The HTML deck stays — it's not coupled to V3 specifically; future versions can reuse the same TV-loop pattern with different content.
