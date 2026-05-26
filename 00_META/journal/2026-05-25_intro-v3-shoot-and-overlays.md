# Journal — 2026-05-25 (PM): Intro V3 — Shoot, Transcode, Overlays, Final Edit

**Session:** Fourteenth (continuation of #13's design/build work, same day, separate session)
**Persona:** Founder (driven from `/srv/meetings/nexostrat` cwd; all work landed in `/srv/Nexostrat/`)
**Duration:** ~4 hours (intermittent during the shoot + edit day)
**Predecessor:** [`2026-05-25_website-intro-v3-redesign.md`](2026-05-25_website-intro-v3-redesign.md) — design lock + HTML deck + initial overlay design

## What this session was

Session 13 (AM) locked the V3 design — Approach A "Anchor + Brand Wall" with the wall-mounted TV playing a keyboard-driven HTML slide deck synced to the spoken script. Ricardo ran a real-world test on shoot day and the TV implementation didn't work (exact failure mode not deeply diagnosed; presumably some combination of glare, framing, sync timing, or clicker setup). He pivoted on the fly to a **white-background talking-head + post-production PNG overlays in DaVinci** — closer to the "Approach C: Post-Heavy White" I had originally discarded for one-day-edit infeasibility, except without the Natron chroma-key complexity. The script, slide content, and overlay design all carried forward; only the *delivery mechanism* (in-camera TV vs. post-production composite) changed.

This session is the implementation pass: pick a take, fix the color shift, build the overlay PNG set, iterate on slide 2, swap in the official WhatsApp logo, review Ricardo's V3 final edit.

## Decisions locked this session

### 1. Workflow pivot — post-production overlays over white background

The TV-deck approach is retired from the V3 critical path but **the HTML deck stays in the repo** as a reference artifact. The same script, the same slide content, the same brand system — just composited as PNG overlays on V2 above the talking head on V1 in DaVinci's Edit page, rather than physically playing on a TV in the shoot.

This is actually **cleaner from a production standpoint**: no glare management, no clicker timing, no on-set sync, more iteration freedom in post.

Reversal: if a future shoot has access to a proper green-screen or a controllable TV setup, the HTML deck is still there.

### 2. T7 as the locked take

7 new takes shot today (`PXL_20260525_195935355.mp4` through `PXL_20260525_201521963.mp4`). All ~53s, all 4K HEVC HLG. Compared by extracting 7 frames each at 8s intervals and viewing as a 7×3 grid:

- **T7 wins on opening warmth** (slight smile + direct camera engagement, others more neutral)
- **Friendly open-palm gesture** at ~16s explains rather than asserts
- **Clean closing pose** at ~48s — perfect "hold-on-this-frame" final pose for the WhatsApp graphic
- **Stable framing end-to-end** (T6 was rejected for framing drift)

Caveat flagged: at ~40s T7 has a pointing gesture that Comentarios specifically warned against. Editor can cut around it with T2 cutaway if it bothers, or keep it if it lands on "agenda" word (which makes it directive rather than aggressive).

### 3. Color-shift root cause + fix

The biggest technical win of the session. Ricardo had noticed color shift on previous transcodes. ffprobe on T7:

```
pix_fmt        = yuv420p10le        (10-bit)
color_space    = bt2020nc           (BT.2020 wide gamut, HDR)
color_transfer = arib-std-b67       (HLG)
color_primaries= bt2020             (BT.2020)
color_range    = tv                 (limited 16-235)
```

The footage is **HLG / BT.2020 HDR**. The session-11 documented recipe (`ffmpeg -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p`, no color flags, 8-bit) dumps HLG-encoded samples into an 8-bit SDR container — DaVinci then interprets the file as BT.709 SDR, treats the HLG-curve-encoded luma as gamma-2.2 luma, and renders washed-out, hue-shifted output.

**New recipe** (worked correctly on T7):

```
ffmpeg -i input.mp4 \
  -vf "zscale=transfer=linear:npl=100,format=gbrpf32le,zscale=primaries=bt709,tonemap=hable:desat=0,zscale=transfer=bt709:matrix=bt709:range=tv,format=yuv422p10le" \
  -c:v dnxhd -profile:v dnxhr_hqx \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a pcm_s16le -map_metadata 0 \
  output.mov
```

Six-step pipeline:
1. zscale: HLG → linear light, normalize peak to 100 nits (SDR target)
2. format: switch to float for accurate tone-map math
3. zscale: convert primaries BT.2020 → BT.709
4. tonemap: Hable tonemap with desat=0 (filmic rolloff, no desaturation in bright areas)
5. zscale: re-encode as BT.709 transfer / matrix / TV range
6. format: final 10-bit pixel format for DNxHR HQX encoder

The encoder is **DNxHR HQX** (not HQ) — HQX is 10-bit, preserving precision; HQ is 8-bit and would re-introduce some banding/crushing risk. Output is ~25% larger than HQ (T7 ended at 5.5 GB for 53s of 4K).

The marketing README's batch loop should be updated to the new recipe — that's a follow-up not done this session.

### 4. Reusable overlay generator: `tv-loop/build_overlays.py`

Single Python file using Pillow. Renders 1920×1080 RGBA PNG overlays with transparent backgrounds, dark navy `#0C1A2E` text + cyan `#0EA5E9` accents — colors specifically chosen to read on a white wall. All content positioned in the left 60% of the canvas (avoiding the central talking-head subject).

Outputs:
- 4 static slides: `slide-0_cover.png` · `slide-3_proof.png` · `slide-4_diferencia.png` · `slide-5_cta.png`
- 1 animation sequence: `slide-1_hook/frame_0001.png` ... `frame_0180.png` (180 frames @ 30fps = 6s; counter 1→20 with eased-out interpolation + filling progress bar)
- 4-state stair keyframes + final: `slide-2_stairs/state-1..4.png` + `final.png` for crossfading in DaVinci

Iteration arc:
- Round 1: 3 stairs (Estudiamos / Diseñamos / Identificamos), dashed connector. Connector touched Ricardo's hair → tightened positions. Stair order conflicted with spoken script verb order → updated script to match visual ordering.
- Round 2 (final): **4 stairs** (Estudiamos / Identificamos / Diseñamos / Implementamos), connector removed per Ricardo's request. Font reduced 58→52, padding 44→38 to fit 4 pills without crowding. "Implementamos" pill at top-right kept well clear of Ricardo's hairline.

The WhatsApp icon went through two rounds too: Round 1 was a hand-drawn approximation (looked passable but featureless white shape inside the green square). Round 2: Ricardo uploaded the **official WhatsApp logo** (`assets/Whatsapp Logo.png`, RGBA transparent), I copied it to `tv-loop/assets/whatsapp.png` and the script paste-composites it at 160px in Slide 5 — much cleaner branding.

### 5. V3 final edit review

Ricardo rendered the full piece in DaVinci as `edits/Intro V3.mkv` — 55.3s ProRes HQ 4K master, FLAC stereo, BT.709 SDR with proper color metadata, healthy audio levels (mean -22 dB, peak -2.1 dB).

What works (frame-by-frame review):
- **Intro card** (t=0-3s): big "nexostrat" wordmark on Midnight gradient with Ricardo silhouetted behind. Elevates production beyond plain talking-head + overlay.
- **Hook** (t=4-12s): counter visibly animates 1→20 with progress bar filling. Lower-third "Ricardo Mejía" appears for standalone shareability.
- **Stairs** (t=15-25s): 4 pills appear progressively. Composition holds.
- **Proof** (t=26-37s): "8-20 hrs" hero is the visual anchor.
- **CTA** (t=43-50s): WhatsApp logo + number land cleanly.
- **End card** (t=50-55s): brand bumper with wordmark + WhatsApp panel.

Two flags surfaced:
- **CEO title** on the lower-third (t≈5s): "Ricardo Mejía / CEO". Per the founding spec, Ricardo + JP are 50/50 co-founders. Needs verification with JP — either confirm CEO as an internal role split or change to "Co-fundador, Nexostrat".
- **Diferencia overlay missing** at t=37-43s: frames sampled show no overlay during the "Sin plantillas..." spoken line. Either overlay plays <2s and was missed by sampling, or it was dropped from the edit. If dropped, weakens the differentiation beat; drop in `slide-4_diferencia.png` for that ~5s.

## Files created or modified this session

- **new**: `operations/marketing/website-intro/tv-loop/build_overlays.py` — overlay generator script
- **new**: `operations/marketing/website-intro/tv-loop/assets/whatsapp.png` — official WA logo (copied from user upload at `assets/Whatsapp Logo.png`)
- **new**: `operations/marketing/website-intro/overlays/` — generated PNG overlay set (8 files + 180-frame sequence)
- **modified**: `operations/marketing/website-intro/tv-loop/SCRIPT.md` — updated for 4-stair design + new keyframe filenames
- **modified**: `operations/marketing/.gitignore` — extended to track `website-intro/overlays/**`
- **modified**: `STATUS.md` — 14th-session entry + done-block
- **modified**: `tasks.json` — closed 3, added 3
- **rewrote**: `CHECKPOINT.md` — next-session baton

**Heavy assets NOT tracked** (per backup posture, Drive 2TB destination):
- `raw/PXL_20260525_*.mp4` — 7 new takes, ~2 GB total
- `raw/transcoded/T7_PXL_20260525_201521963.mov` — 5.5 GB DNxHR HQX
- `edits/Intro V3.mkv` — 3.2 GB ProRes master

## Open items (carried to next session)

1. **`t-intro-v3-ceo-vs-cofundador`** (HIGH · 2026-05-26): verify CEO title with JP, edit lower-third if needed.
2. **`t-intro-v3-diferencia-slide`** (HIGH · 2026-05-26): confirm or restore Diferencia overlay at t=37-43s.
3. **`t-intro-v3-web-export`** (HIGH · 2026-06-15 — homepage launch): H.264 1080p30 ~6 Mbps faststart MP4. Use `infra/scripts/video-to-mp4.sh`.

## What didn't happen

- **No commit yet** — that fires immediately after this journal, in the session-end commit block.
- **No update to `operations/marketing/README.md`** — the documented batch transcode recipe is now outdated (should reference the HLG→BT.709 tonemap chain, not just `dnxhr_hq`). Filed mentally as a follow-up; can ship as a separate doc-only commit.
- **No update to `00_META/CHANGELOG.md`** — no persona context file edited.
- **No ADR.** No architectural change; this is a marketing artifact iteration.
- **No memo to other personas.** Work stayed inside `operations/marketing/`.

## Reversal

If V3 doesn't perform on the homepage and we need to rethink:
- V1.x/V2.x talking-head MKVs still in `edits/`
- All 7 raw takes preserved in `raw/`
- The overlay PNG set is reusable for any future iteration (re-run `build_overlays.py` to regenerate)
- The HLG→BT.709 transcode recipe is the new standard for any future Pixel/HDR phone shoot in this workflow

The expensive intellectual work (script, brand system, layout, color-shift fix) is captured in `INTRO_V3_DESIGN.md`, `SCRIPT.md`, this journal, and the build script. Pivoting again would not require redoing any of it.
