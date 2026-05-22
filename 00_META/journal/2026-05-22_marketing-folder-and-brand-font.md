# Session 11 — Marketing folder structure + brand font fix

**Date:** 2026-05-22
**Persona:** Founder (root) → momentarily crossed into Skills-Master scope for brand.py / generate_docx.py edits (operator-driven per Strict Rule 1)
**Host:** `ricardo-desktop` (note — Nexostrat repo cloned here as part of the 2026-05-20 desktop bootstrap; the laptop `ricardo-hp-laptop` remains primary server)
**Duration:** ~3 hours
**Topic:** Operational arc — no architecture changes, no ADRs. Folder cleanup, video pipeline troubleshooting, brand font flip.

## Arc summary

A clean, tangential session. Ricardo opened with a one-line ask: organize the `Temporal Assets and video/` folder he'd just dropped into the repo root (raw phone footage + logo PNGs for the website intro video he's editing in DaVinci Resolve). What followed was four discrete pieces of work, each triggered by a real obstacle hit during the editing flow:

1. **Folder organization.** Built `operations/marketing/{brand,website-intro}/` tree with documented `raw/ → edits/ → final/` per-campaign pipeline. `brand/` for long-lived logo + brand assets; `website-intro/` for the current campaign. All gitignored except the README which documents the structure. Ricardo's preference locked: nothing committed (heavy regenerable assets), README explains the convention so future sessions inherit it.
2. **DaVinci Resolve HEVC blocker.** Ricardo dragged the 3 raw `PXL_*.mp4` clips into DaVinci and got "green bar, no image." Diagnosed in one ffprobe: HEVC Main 10 (H.265 10-bit), which DaVinci Resolve Free on Linux cannot decode (Studio-only codec on Linux). Transcoded all 3 to DNxHR HQ in MOV containers (DaVinci's native editing codec), wrote them to `raw/transcoded/` next to the originals, and documented the workflow (ffmpeg one-liner + batch loop) in the marketing README so future shoots inherit the fix.
3. **Brand font.** Ricardo asked what Nexostrat's brand font is for use in LibreOffice. Memory `outputs-premium-visual.md` mandates Inter — but `fc-match Inter` returned Liberation Sans (not installed). Worse, code audit revealed `skills/shared/brand.py:26` shipped `BRAND_FONT = "Calibri"` (not Inter), and `skills/05_opportunity_report/scripts/generate_docx.py` imported the constant but hardcoded `'Calibri'` literal 17 times. Ricardo ran `sudo apt install fonts-inter fonts-jetbrains-mono` on `ricardo-desktop`; flipped `BRAND_FONT` → `"Inter"` (added `BRAND_FONT_MONO = "JetBrains Mono"` for future use); replaced all 17 hardcoded `'Calibri'` strings in generate_docx.py with the imported `BRAND_FONT` constant (cleanup of a longstanding code smell). Test harness: 32 PASS · 0 SKIP · 0 FAIL — same as baseline. Brand-spec divergence in `operations/assets/brand/Nexostrat_Logo_Kit.html` (Century Gothic + Nunito) flagged but NOT touched — that's the logo wordmark font, separate concern.
4. **Web export.** Ricardo dropped two DaVinci ProRes MKV exports (~855 MB each, 1080p30, FLAC) into `website-intro/edits/` and asked for MP4. Transcoded both to H.264 High + AAC 192k + `+faststart` (so the browser starts playing before the file fully buffers). 817 MB → 21 MB each, no visible quality loss at CRF 20 for talking-head footage. Originals preserved as editing masters.

## Decisions locked

1. **Marketing folder layout** documented in `operations/marketing/README.md`. Per-campaign `raw/ → edits/ → final/` standard. Future campaigns drop as siblings of `website-intro/`.
2. **Heavy assets stay out of git.** `operations/marketing/.gitignore` ignores everything except README + the gitignore itself. Backup posture: Drive 2TB (heavy-assets-pattern from root CLAUDE.md) — though this session's raw + transcoded video files are ~10 GB and not currently backed up. Acceptable for working files; flag if they become irreplaceable.
3. **Brand font is Inter.** Single source of truth: `skills/shared/brand.py` — `BRAND_FONT = "Inter"`, `BRAND_FONT_MONO = "JetBrains Mono"`. All 5 skills now pull from this constant. Inter package installed via apt `fonts-inter` (Ubuntu/Mint noble package, 4.0+ds-1, MIT/SIL licensed, OTF in /usr/share/fonts/opentype/inter/).
4. **DNxHR HQ MOV is the DaVinci-on-Linux editing intermediate.** Workflow: source camera files → `raw/` (archive) → ffmpeg to `raw/transcoded/` as DNxHR HQ MOV → import into DaVinci → export edits → optional re-encode to H.264 MP4 for web. Documented in marketing README.

## Files modified this session

NEW (committed):
- `operations/marketing/README.md` — folder convention + video pipeline workflow
- `operations/marketing/.gitignore` — ignore everything except README

NEW (gitignored, on-disk only):
- `operations/marketing/brand/logos/` — 18 PNG logo variants (moved from Temporal Assets and video/Logos/)
- `operations/marketing/website-intro/raw/2026-05-21_take-{01,02,03}.mp4` — 3 phone takes
- `operations/marketing/website-intro/raw/transcoded/2026-05-21_take-{01,02,03}.mov` — DaVinci-ready DNxHR HQ
- `operations/marketing/website-intro/edits/Intro V1.{0,1}.mkv` — DaVinci ProRes exports
- `operations/marketing/website-intro/edits/Intro V1.{0,1}.mp4` — web-ready H.264

MODIFIED (committed):
- `skills/shared/brand.py` — BRAND_FONT = "Inter" + BRAND_FONT_MONO = "JetBrains Mono" + 2 docstring updates
- `skills/05_opportunity_report/scripts/generate_docx.py` — 17 hardcoded `'Calibri'` → `BRAND_FONT` constant

DELETED:
- `Temporal Assets and video/` — relocated, then removed

Session-end bookkeeping (this commit):
- `STATUS.md` — header + session 11 block
- `tasks.json` — 3 new tasks + updated timestamp
- `CHECKPOINT.md` — rewritten
- `00_META/journal/2026-05-22_marketing-folder-and-brand-font.md` — this file

Untouched:
- `00_META/journal/2026-05-21_strategy-meeting-transcript.md` — pre-existing untracked file from earlier, not authored this session.

## Tasks added

| Slug | Priority | Due | Why |
|---|---|---|---|
| `t-install-brand-fonts-laptop` | high | 2026-05-30 | Inter installed only on desktop; laptop is where most renders happen. Without it, LibreOffice substitutes to Liberation Sans on the laptop's renders. |
| `t-pick-website-intro-final-version` | medium | 2026-06-15 | V1.0 vs V1.1 pick gated on JP review. When decided, move chosen MP4 to `final/`. |
| `t-fix-logo-kit-html-fonts` | low | 2026-07-15 | Logo kit HTML still references Century Gothic + Nunito. Brand-spec-level decision: restamp wordmark in Inter or accept divergence. |

## Open creative question (not blocking)

**Music vs no-music for the website intro.** Raised in-session: for a 38s founder-to-camera intro, options are (a) sober/cinematic music ducked under voice (-14 to -18 LUFS intro/outro, -24 to -30 ducked), or (b) no music + clean room tone (Anthropic/Linear pattern). Sources flagged: Pixabay Music (free), Epidemic Sound (~$15/mo), Artlist (~$17/mo). NOT Spotify/YouTube tracks (copyright). Decision deferred to next editing pass.

## Architecture-conflict check (passed)

| This session's work | Verification |
|---|---|
| Cross-scope edit into skills/ (brand.py + generate_docx.py) | Ricardo operator-driving per Strict Rule 1. Skills-Master CLAUDE.md Strict Rule 6 ("versioning + benchmarks are gates") doesn't apply — this was a constant + literal-cleanup, not a prompt edit. No skill versions bumped; behavior unchanged at the test-harness level (32 PASS preserved). |
| New marketing/ folder under operations/ | operations/ is already Founder-owned per root CLAUDE.md Strict Rule 2. README + gitignore committed are the only tracked artifacts; heavy assets are gitignored per heavy-assets-pattern from § Vault / Sensitive Discipline. |
| Brand font change | Consistent with memory `outputs-premium-visual.md` (mandates Inter). Closes a longstanding spec-vs-code divergence (memory said Inter; code shipped Calibri). |
| No `feedback_no_brain_references` violations | No /srv/brain references introduced. |

## Memory updates

None new. Existing memories applied:
- `outputs-premium-visual.md` — drove the Inter font choice + JetBrains Mono addition.
- `do-it-right-do-it-once.md` — drove the generate_docx.py hardcode cleanup (replacing 17 literal `'Calibri'` strings instead of just patching the constant in one place) and the README documentation of the DNxHR workflow.
- `complete-or-nothing.md` — drove bundling folder org + transcoding + font fix + web export + tests + task tracking + journal + commit all in one session.

## For a future auditor

This was an operational, tangential session — no ADRs, no architecture changes, nothing on the critical Trixx-2026-05-25 path. The lasting value is twofold: (1) the marketing/ folder structure + README that future campaigns inherit, and (2) the brand font fix that closes a memory-vs-code divergence and unifies the BRAND_FONT constant across all 5 skill renderers. Side effect: the marketing README now documents the DaVinci-on-Linux HEVC workaround so the next time Ricardo (or JP) shoots phone footage, they have the ffmpeg recipe ready.

Critical path remains Trixx 2026-05-25 1pm Tijuana (T-3 days from this session). Materials intact. Nothing on this side blocks it.
