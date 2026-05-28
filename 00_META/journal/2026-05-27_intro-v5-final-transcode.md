# 2026-05-27 — Intro V5 final transcode + new shoot ingest

**Session type:** maintenance (marketing)
**Duration:** ~10 min
**Persona:** Founder
**Predecessor context:** [`2026-05-23_davinci-mp4-playback-fix.md`](2026-05-23_davinci-mp4-playback-fix.md) (the `video-to-mp4` wrapper) + [`2026-05-25_intro-v3-shoot-and-overlays.md`](2026-05-25_intro-v3-shoot-and-overlays.md) (the HLG→BT.709 tonemap recipe + V3 edit baseline)

## What was done

Two video transcodes against the website-intro pipeline:

1. **New shoot ingest.** `raw/PXL_20260528_003128365.mp4` (Pixel 10 Pro XL, 4K30, HEVC Main 10, BT.2020/HLG HDR, 51.87s, 4.3 GB) → `raw/transcoded/PXL_20260528_003128365.mov` (DNxHR HQX, 10-bit yuv422p10le, BT.709 tone-mapped, 51.87s, 5.3 GB). Used the locked recipe from session 14 verbatim (HLG → linear → BT.709 primaries → Hable tonemap desat=0 → BT.709 transfer/matrix/TV range → DNxHR HQX). DaVinci-importable.

2. **V5 master → web MP4.** `edits/Intro V5.mkv` (DaVinci master: ProRes 1080p30 BT.709 + PCM 24-bit, 57s, 1.4 GB) → `edits/Intro V5.mp4` (H.264 CRF 18 preset slow + AAC 192k + faststart, 26 MB) via `video-to-mp4 -f`. 53× compression, visually indistinguishable from the ProRes master (CRF 18 = visually-lossless threshold for talking-head footage). `color_space=bt709` preserved end-to-end.

Ricardo declared V5 the **final webpage version**, closing the V1/V2/V3 candidate sweepstakes that had been open since session 11. CEO title confirmed in the V5 lower-third ("Ricardo Mejía / CEO") — Ricardo is CEO + public face of Nexostrat; JP's matching role designation is a future conversation.

## Decisions locked this session

- **Intro V5 is the website hero video** (final, not a candidate). Supersedes V1.0/V1.1/V1.2/V3.
- **CEO title on Ricardo's lower-third stands** as approved. Ricardo = CEO + face of the company. JP's reciprocal title (CTO? Co-fundador?) deferred to a future Ricardo↔JP conversation.
- **Diferencia overlay question moot.** V5 declared final = current overlay treatment is accepted, regardless of whether the Diferencia slide is present or briefly visible.
- **Wrapper-default recipe holds** for web export. CRF 18 / preset slow / AAC 192k / faststart is the standard. Mathematical losslessness (CRF 0) not pursued — overkill for web delivery and produces ~1 GB files.

## Files created or modified this session

- **new (gitignored, heavy)**: `raw/transcoded/PXL_20260528_003128365.mov` (5.3 GB)
- **new (gitignored, heavy)**: `edits/Intro V5.mp4` (26 MB)
- **pre-existing (gitignored, heavy)**: `raw/PXL_20260528_003128365.mp4`, `edits/Intro V5.mkv` (input files; not authored this session)
- **modified (tracked)**: `STATUS.md`, `tasks.json`, `CHECKPOINT.md`, `00_META/journal/2026-05-27_intro-v5-final-transcode.md` (this file)

Heavy video assets remain untracked per the backup posture (Drive 2TB destination for marketing raw + masters + exports).

## Tasks closed

- `t-intro-v3-ceo-vs-cofundador` — CEO title confirmed (Ricardo is CEO + face)
- `t-intro-v3-diferencia-slide` — V5 final = current treatment accepted
- `t-intro-v3-web-export` — `edits/Intro V5.mp4` IS the web export

## Open items / follow-ups

- **Move V5.mp4 into `final/`** per the README convention (`operations/marketing/website-intro/final/`). Not done this session because: the folder exists but I didn't want to relocate the file without explicit confirmation; the `.mp4` is gitignored either way so a `mv` only affects local working tree.
- **`00_PARTNERSHIP/ROLES.md` amendment.** Currently doesn't designate CEO/CTO between Ricardo + JP. Ricardo's CEO designation is now publicly committed via the homepage video. Should be reflected in the partnership doc — but it's a signed legal artifact (signed 2026-05-12), so amendment process should be deliberate (addendum rather than grep-replace), and JP's reciprocal role should be agreed first. Not blocking anything immediate.
- **Drive backup pending** for the new heavy assets (raw + transcoded + V5.mp4). No firm schedule.

## What didn't happen

- No commit yet — fires immediately after this journal in the session-end commit block.
- No ADR. Marketing-artifact iteration; no architectural change.
- No memo to other personas. Work stayed inside `operations/marketing/`.
- No Gemini handoff opened.
- No update to `operations/marketing/README.md`. The wrapper and the tonemap recipe are already documented (wrapper in `~/Desktop/DESKTOP_PC_COMMANDS.md`, tonemap recipe in `00_META/journal/2026-05-25_intro-v3-shoot-and-overlays.md`).

## Reversal

If V5 turns out to need a re-edit (CEO title flip-flop, music change, runtime trim):
- ProRes master `edits/Intro V5.mkv` is preserved (1.4 GB, local).
- Raw take `raw/PXL_20260528_003128365.mp4` is preserved + transcoded DNxHR copy ready for DaVinci.
- The wrapper recipe is one CLI call away: `video-to-mp4 -f 'edits/Intro V5.mkv'`.
- Older candidates V1.x/V2.x/V3 still in `edits/` as fallback options.

The expensive intellectual work (script, brand system, overlay PNGs, color recipe) all carries forward.
