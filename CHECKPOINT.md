# CHECKPOINT — root (Founder)

**Updated:** 2026-05-25T11:00:00-07:00
**By:** ricardo (via Claude Code session 13, driven from `/srv/meetings/nexostrat/` cwd; all work landed in `/srv/Nexostrat/`)
**Persona:** Founder
**Session topic:** Website intro V3 redesign — full design system from CMO-audit response to production-ready HTML deck + spoken script + design spec. Approach A "Anchor + Brand Wall" (wall-mounted TV displays a keyboard-driven HTML slide deck synced to the spoken script via Bluetooth clicker; sync happens in-camera, not in post). No architecture changes, no ADRs.

## What just happened (last session — read once, don't re-litigate)

Three-hour brainstorming → design → build session, end-to-end on the homepage hero video. Outcome: V3 design locked, deck shipped, script + spec written, gitignore exception added, tasks updated.

**1. Audit absorption.** Read the `Comentarios Video` CMO critique on `Intro V1.x`/`V2.mkv`. Sampled V2.mkv at 4s intervals to confirm V2 made cosmetic gains (name overlay, wordmark overlay) but left the structural critique unaddressed: white wall, lavalier visible, 3-CTA end card, no value-prop text overlays, two logo lock-ups, assertive gestures.

**2. Strategic frame locked.** Goal=convert to WhatsApp. Single CTA. 45s final. *Tranquilidad y competencia* tone. *Tú* register. Pre-launch-honest framing ("La meta:" instead of fake "Nuestros clientes recuperan…"). Ricardo's homepage-context-already-shows-who-I-am insight let us drop "Soy Ricardo Mejía" entirely, saving 4 seconds.

**3. Approach A: Anchor + Brand Wall.** Evaluated four backdrops Ricardo had staged (wood paneling, wall-mounted TV, balcony with city/golf-course view, cleaner wood) + a chroma-key-on-white-wall composite alternative. Backdrop 02 (wall-mounted TV) chosen because the TV becomes a brand-content panel synced to the script — production-design half of the message, not just a backdrop. Chroma-key rejected for one-day-edit constraints (Natron edge artifacts would survive into final).

**4. HTML deck built** at `operations/marketing/website-intro/tv-loop/index.html` (15.9 KB, self-contained, zero build deps). Six slides on Midnight `#0C1A2E` with Sky-Blue `#0EA5E9` accents. Single-page-app navigation: Space/→ advances, ← reverses, F toggles fullscreen, G shows rule-of-thirds grid, R toggles rehearsal HUD, H shows cursor, 0-5 jump-to-slide, click-anywhere fallback. All content sits in the canvas's left 60% so Ricardo on the right third of camera frame doesn't cover it.

**5. Slide-specific animations.** Slide 1 animates a 1→20 hour counter (JS, eased-out) over 6s + a filling progress bar in parallel. Slide 2 auto-reveals three stair pills (Estudiamos at 0.3s, Identificamos at 3.5s, Implementamos at 8.0s) on a single SPACE press — pill timings track Ricardo's spoken pace through the slide-2 line. Slide 5 closes on a WhatsApp CTA (icon + `+57 333 286 3969` + "30 minutos · sin costo"). All animations restart cleanly when slides are re-entered (selector-based CSS animations + JS rAF for the counter).

**6. Spoken script locked by Ricardo** at 5 SPACE-cue beats. Annotated prompter version at `operations/marketing/website-intro/tv-loop/SCRIPT.md`. Final pill labels (Estudiamos · Identificamos · Implementamos) match Ricardo's verb flow and land naturally on the spoken word "implementación."

**7. Design spec written** at `operations/marketing/website-intro/INTRO_V3_DESIGN.md` — strategic locks, approach rationale, production system diagram, shoot-day setup (room/camera/lighting/audio/wardrobe), edit plan (DaVinci 1-day timeline + color + music + export), V1-V2-critique-to-V3-response table, file map, V4 trigger conditions.

**8. gitignore exception** added at `operations/marketing/.gitignore`. The marketing folder previously declared everything ignored except README; V3 introduces a deliberate exception for `website-intro/tv-loop/**` (deck + script + brand-asset PNGs) and `website-intro/*.md` (design spec). Both are canonical brand artifacts, not regenerable working files. ~40 KB total. Verified with `git check-ignore -v` + `git add --dry-run`.

**9. Tasks updated.** Superseded `t-pick-website-intro-final-version` (V3 obsoletes the V1.0-vs-V1.1 choice). Added: `t-intro-v3-dry-run` (high · 2026-05-30), `t-buy-presenter-clicker` (low · 2026-06-05), `t-intro-v3-shoot-and-edit` (high · 2026-06-15).

**Result:** V3 is the new canonical homepage hero video direction. Shoot is gated only on a 30-60 min dry-run (verify font sizes + TV reflection control + pill timing) and a $15-25 Bluetooth clicker. Same-day shoot + same-day edit feasible once those two checkboxes hit.

## Decisions locked this session

1. **Approach A over B/C/composite.** TV-on-wall as a brand-content panel beats outdoor balcony (weather-dependent) and chroma-key composite (one-day edit not enough for clean edges without a real green screen). Reversal: trivial — V3 doesn't delete the V1/V2 takes; pivoting to outdoor or composite means a new shoot day with the same script + deck.

2. **5 SPACE cues total.** Pre-rolls stays on Slide 0 silent. SPACE 1-5 each open a new slide. Slide 2's three pills auto-reveal on timed delays (no extra SPACE per pill — Ricardo simplified this from an earlier 7-press version). Reversal: change `data-steps="1"` to `data-steps="3"` on Slide 2 and add per-pill `data-step` attributes — pattern is already in the JS station-counter logic, just unused.

3. **Pre-launch-honest projection language.** "La meta: que recuperes entre 8 y 20 horas a la semana" instead of "Nuestros clientes recuperan…" (which we cannot substantiate yet). Upgrade to the latter the moment Stage 1 ships testimonials.

4. **Lower-third in post for speaker ID.** The video itself drops "Soy Ricardo Mejía" — homepage context identifies Ricardo through the "Equipo" section. For standalone reposts (LinkedIn etc.) a 4-second lower-third "Ricardo Mejía · Co-fundador, Nexostrat" renders in DaVinci, not on the TV.

5. **gitignore exception is deliberate.** The marketing folder remains "ignore-by-default"; the V3 deck + spec are explicit exceptions because they are canonical brand artifacts. Other future campaigns (LinkedIn launch, pitch deck) follow the default unless their artifacts are similarly canonical.

## Stack state (live & verifiable next session)

```
/srv/Nexostrat/
├── operations/marketing/
│   ├── .gitignore                  ← MODIFIED (V3 exception pattern)
│   └── website-intro/
│       ├── INTRO_V3_DESIGN.md      ← NEW (full design spec)
│       ├── Comentarios Video       ← (existing CMO audit; informed V3)
│       ├── Backdrop 01..04.jpeg    ← (existing options; #02 chosen)
│       ├── tv-loop/                ← NEW (the deck)
│       │   ├── index.html          ← NEW (6-slide TV deck)
│       │   ├── SCRIPT.md           ← NEW (annotated prompter script)
│       │   └── assets/
│       │       ├── icon.png        ← NEW (copy of brand mark)
│       │       └── wordmark.png    ← NEW (copy of full wordmark on Midnight)
│       ├── edits/                  ← (V1.x / V2.x legacy DaVinci timelines)
│       ├── raw/                    ← (untouched — raw takes + transcoded MOVs)
│       └── final/                  ← (empty — V3 lands here after shoot+edit)
├── STATUS.md                       ← MODIFIED (thirteenth-session entry + done-block)
├── tasks.json                      ← MODIFIED (3 new tasks, 1 superseded)
├── 00_META/journal/
│   └── 2026-05-25_website-intro-v3-redesign.md  ← NEW
└── CHECKPOINT.md                   ← THIS FILE (rewritten)
```

## Open items (across sessions)

| ID | Subject | Priority | Due |
|---|---|---|---|
| t-intro-v3-dry-run | V3 deck — dry-run on real TV; tune CSS delays if needed | high | 2026-05-30 |
| t-buy-presenter-clicker | Bluetooth presenter remote ($15-25) for hands-free SPACE | low | 2026-06-05 |
| t-intro-v3-shoot-and-edit | Half-day shoot + 1-day DaVinci edit per INTRO_V3_DESIGN.md | high | 2026-06-15 |
| (Trixx pilot meeting) | Pilot meeting was scheduled 2026-05-25 — separate track | critical | (today) |
| (per tasks.json, ~70 other open tasks not directly related to V3) | | | |

## What did NOT happen this session

- **No commit yet** — that fires immediately after this CHECKPOINT.md write, in the session-end commit block.
- **No memo or cross-folder coordination.** Work stayed inside `operations/marketing/`.
- **No `00_META/CHANGELOG.md` update.** No persona context file was edited (CLAUDE.md / GEMINI.md / README.md untouched).
- **No ADR.** V3 is a marketing artifact, not an architectural decision.
- **No Gemini handoff.** No adversarial-audit or fresh-info-lookup need for V3.
- **No shoot.** That's a separate session, gated on `t-intro-v3-dry-run` and `t-buy-presenter-clicker`.
- **No Trixx meeting prep.** The Trixx pilot is the project's other critical-path item (2026-05-25 today) — handled in its own session track.

## Next session — what to read first

1. `STATUS.md` top — the thirteenth-session entry summarizes the V3 work in one paragraph.
2. `operations/marketing/website-intro/INTRO_V3_DESIGN.md` — full design context.
3. `operations/marketing/website-intro/tv-loop/SCRIPT.md` if working on the script or shoot prep.
4. `operations/marketing/website-intro/tv-loop/index.html` if tuning the deck (pill timings, animations, slide content).

If the next session is "do the dry-run" or "do the shoot": follow `INTRO_V3_DESIGN.md` §6 and §7 like a runbook.
