# CHECKPOINT — root (Founder)

**Updated:** 2026-05-22T15:25:18-07:00
**By:** ricardo (via Claude Code session 11 at /srv/Nexostrat/ on `ricardo-desktop`)
**Persona:** Founder
**Session topic:** Operational arc — organize the `Temporal Assets and video/` folder Ricardo dropped at the repo root (raw website-intro footage + brand logos); diagnose + fix the DaVinci Resolve "can't read HEVC" wall; flip the brand font from Calibri to Inter (memory said Inter, code shipped Calibri); export web-ready MP4 versions of two DaVinci ProRes edits. No architecture changes, no ADRs, no critical-path movement.

## What just happened (last session — read once, don't re-litigate)

Tangential operational session, ~3 hours, four discrete pieces of work each triggered by a real obstacle Ricardo hit while editing the Nexostrat website intro video in DaVinci Resolve:

**1. Folder reorganization.** Built `operations/marketing/{brand,website-intro}/` with documented per-campaign `raw/ → edits/ → final/` convention. `brand/logos/` holds the 18 PNG logo variants (moved out of the chaotic `Temporal Assets and video/` folder). `website-intro/` holds the current campaign. README in `operations/marketing/README.md` documents the structure + conventions (only it and `.gitignore` are committed; everything else is gitignored — heavy regenerable working files). Convention scales: future campaigns drop as siblings of `website-intro/`.

**2. DaVinci Resolve HEVC blocker.** Ricardo's symptom: dragging the 3 raw `PXL_*.mp4` phone clips into DaVinci showed a green bar (audio) but no image. One `ffprobe` confirmed: HEVC Main 10 (H.265 10-bit HDR) — DaVinci Resolve Free on Linux can't decode this (Studio-only codec on Linux). Transcoded all 3 to DNxHR HQ MOV (DaVinci's preferred edit codec, visually lossless, intra-frame, full source resolution 3564×1932 preserved). Output ~9.4 GB in `website-intro/raw/transcoded/`. Documented the ffmpeg recipe + batch loop in marketing README so future Pixel shoots inherit the fix.

**3. Brand font flip (Calibri → Inter).** Memory `outputs-premium-visual.md` mandated Inter; code (`skills/shared/brand.py:26`) shipped `BRAND_FONT = "Calibri"`. Divergence since v0.1 of the skills. Ricardo ran `sudo apt install fonts-inter fonts-jetbrains-mono` on `ricardo-desktop`. Updated `brand.py`: BRAND_FONT → "Inter" + new `BRAND_FONT_MONO = "JetBrains Mono"` constant (future use) + 2 docstring updates. Cleaned `skills/05_opportunity_report/scripts/generate_docx.py`: 17 hardcoded `'Calibri'` literals replaced with the imported `BRAND_FONT` constant — file already imported the constant but ignored it (longstanding code smell). Test harness: 32 PASS · 0 SKIP · 0 FAIL, same as baseline. Brand-spec divergence in `operations/assets/brand/Nexostrat_Logo_Kit.html` (Century Gothic + Nunito for the logo wordmark) flagged but not touched — that's a separate concern (logo design font vs document body font).

**4. Web exports.** Ricardo dropped two DaVinci ProRes HQ MKV exports (~855 MB each, 1080p30, FLAC, 38s) into `edits/`. Transcoded both to H.264 High + AAC 192k + `+faststart` (instant browser playback). Output: `Intro V1.{0,1}.mp4`, 21 MB each, visually transparent at CRF 20 for talking-head footage. JP gates the V1.0 vs V1.1 pick (Ricardo's note in-session: "Final version done i will confirm once juan pablo choose").

**Result:** No architectural change. Operational hygiene: marketing folder convention documented, video pipeline blocker permanently solved with documented workaround, brand font divergence closed at the renderer-constant level. 3 new tasks tracked for follow-up.

## Decisions locked this session

1. **Marketing folder layout.** `operations/marketing/<campaign-slug>/{raw,edits,final}/` per campaign; `operations/marketing/brand/` for cross-campaign brand assets (logos, etc.). All gitignored except README + .gitignore. Documented in `operations/marketing/README.md`.

2. **DaVinci Resolve on Linux Free = DNxHR HQ MOV.** Workflow: source camera → `raw/` (archive) → ffmpeg transcode → `raw/transcoded/` as DNxHR HQ MOV → import into DaVinci → export edits → optional re-encode to H.264 MP4 for web delivery. Recipe documented in marketing README. Reversal: irrelevant — codec choice is forced by DaVinci Free's Linux capabilities, no alternative.

3. **Brand font = Inter (single source: `skills/shared/brand.py`).** `BRAND_FONT = "Inter"`; `BRAND_FONT_MONO = "JetBrains Mono"`. All 5 skill renderers (01-05) pull from the constant. Installed system-wide via apt `fonts-inter` (4.0+ds-1, MIT/SIL, OTF in /usr/share/fonts/opentype/inter/) + `fonts-jetbrains-mono` (2.304+ds-4, TTF). On `ricardo-desktop` so far; laptop still pending (tracked in `t-install-brand-fonts-laptop`).

4. **Heavy assets stay out of git.** `operations/marketing/.gitignore` ignores `*` except README + .gitignore. Working files (raw camera, DaVinci intermediates, web exports) backed by source-of-truth (camera roll, DaVinci project files in editing app) + optionally Drive 2TB for irreplaceable masters. Session-11 generated ~10 GB of marketing files locally; none on Drive yet (working files, acceptable).

## Stack state (live & verifiable next session)

```
HP (ricardo-hp-laptop, Tailscale 100.64.121.80) — unchanged from session 10:
  baserow + bookstack + bookstack-db + caddy all healthy.
  systemd nexostrat-foss-stack.service enabled.
  Two nightly timers still MASKED (reconcile @03:30, schema-check @Mon04:00) —
    waiting on t-plan-02a-chunk-b-systemd-creds (high, due 2026-06-01).

Desktop (ricardo-desktop) — bootstrapped session 8 (journal 2026-05-20b):
  /srv/Nexostrat/ cloned + working tree active.
  Inter + JetBrains Mono now installed system-wide (session 11).
  ALL skills runnable here; DaVinci Resolve installed; OBS + Whisper not
    (per t-desktop-pc-recording-stack-install).

Recording + transcription stack — unchanged from session 9:
  Server laptop has OBS Studio 30.0.2 + pavucontrol 5.0
  Whisper.cpp /opt/whisper.cpp/ + models (small fallback, large-v3 preferred)
  ~/bin/transcribe.sh wrapper
  OBS profile audio-meeting

Vault discipline — unchanged from session 9:
  infra/age-recipients.txt: 2 keys (Ricardo, JP). C2 operationally closed.

Brain Bot Platform tenancy — locked session 10:
  ADR-039 active. ADR-020 superseded.

NEW this session (11) — operational changes:
  operations/marketing/ tree built + documented.
  3 raw HEVC takes transcoded to DNxHR HQ MOV in raw/transcoded/.
  2 ProRes MKV edits transcoded to H.264 MP4 in edits/.
  Brand font flipped: skills/shared/brand.py BRAND_FONT = "Inter".
  17 hardcoded 'Calibri' literals in opportunity-report renderer cleaned up.
  Test harness: 32 PASS · 0 SKIP · 0 FAIL.
```

## In flight — concrete next actions

```
NEXT SESSION:
  1. Open Claude Code AT /srv/Nexostrat/.
  2. Ricardo types "Start Session."
  3. Claude reads CHECKPOINT + STATUS + tasks + calendar + latest journal
     (00_META/journal/2026-05-22_marketing-folder-and-brand-font.md).
  4. Ricardo decides arc.

CRITICAL PATH (unchanged from session 10):

  ┌── 2026-05-25 1pm Tijuana ─────────────────────────────┐
  │  REUNIÓN TRIXX LOGISTICS                               │
  │  (t-trixx-meeting-execution, critical)                 │
  │  T-3 days. Materiales en Desktop intactos.             │
  └─────────────────────┬──────────────────────────────────┘
                        │
  ┌── 2026-05-27 ─▼─────────────────────────────────────────┐
  │  SKILL 05 (Opportunity Report)                          │
  │  (t-trixx-skill-05-opportunity-report, high)            │
  └─────────────────────────────────────────────────────────┘

NEW THIS SESSION (3 tasks, low-blast-radius cleanups):

  ┌── 2026-05-30 ─┐ NEW (high)
  │  t-install-brand-fonts-laptop                           │
  │  sudo apt install fonts-inter fonts-jetbrains-mono     │
  │  on ricardo-hp-laptop. Without it, LO substitutes      │
  │  to Liberation Sans on the laptop's renders.            │
  └───────────────┘

  ┌── 2026-06-15 ─┐ NEW (medium)
  │  t-pick-website-intro-final-version                     │
  │  Pick V1.0 vs V1.1 of the website intro MP4.            │
  │  Gated on JP. Move chosen file edits/ → final/.         │
  │  Open creative question: music vs no-music.             │
  └───────────────┘

  ┌── 2026-07-15 ─┐ NEW (low)
  │  t-fix-logo-kit-html-fonts                              │
  │  Logo kit HTML still references Century Gothic +        │
  │  Nunito. Decide: restamp wordmark in Inter or accept   │
  │  divergence between wordmark font + body font.          │
  └───────────────┘

BRAIN BOT PLATFORM PRE-LAUNCH (unchanged from session 10):
  - t-plan-04-description-update (high 2026-05-28)
  - t-nexostrat-telegram-account (critical 2026-06-15)
  - t-weekend-desktop-on-decision (high 2026-06-15)
  - t-confidence-calibration-corpus (high 2026-06-22)
  - t-plan-08-client-meeting-integration (medium 2026-07-15)

PARALLEL TRACK — Chunk B follow-ups (unchanged from session 10):
  - t-plan-02a-chunk-b-systemd-creds (high 2026-06-01)
  - t-plan-02a-chunk-b-renderer-hook-lift (medium 2026-06-10)
  - t-plan-02a-chunk-b-test-coverage (medium 2026-06-10)

CHUNK C — next major arc (unchanged from session 10):
  - t-plan-02a-execute-chunk-c (medium 2026-06-12)
  - t-plan-02b-write (medium 2026-06-30)

PARTIALLY CLOSED (unchanged from session 9):
  - t-plan-01a-jp-and-tty-deferred (medium 2026-06-30)
    Items (1)-(4) DONE. Items (6)(7)(8)(9) remain TTY-gated.

OTHER OPEN (unchanged from session 10 — see tasks.json):
  - t-vault-backup-foss-env, t-whatsapp-andrea-audiencia,
    t-practice-meeting-jp, t-migrate-pilotos-to-clients,
    t-presentation-refresh-post-adr-038,
    t-plan-01b-execute-warm-standby (gated on physical second host),
    t-confidence-marking-company-analyst, t-nexostrat-capabilities-catalog,
    t-validate-pipeline-improvements, t-plan-01c-polish-pass,
    t-desktop-pc-recording-stack-install
```

## Architecture-conflict check (passed)

| This session's work | Verification |
|---|---|
| Cross-scope edit into skills/ (brand.py + generate_docx.py) | Ricardo operator-driving per root CLAUDE.md Strict Rule 1. Skills-Master Strict Rule 6 (versioning + benchmarks) doesn't apply — constant + literal-cleanup, not a prompt edit. Test harness preserved (32 PASS). |
| New marketing/ folder under operations/ | operations/ is Founder-owned per root CLAUDE.md Strict Rule 2. Only README + .gitignore committed; heavy assets gitignored per § Vault / Sensitive Discipline heavy-assets-pattern. |
| Brand font change | Consistent with memory `outputs-premium-visual.md`. Closes a memory-vs-code divergence. |
| No `/srv/brain` references introduced | Confirmed by grep — no new references. Strict Rule 4 preserved. |
| Three new tasks | Dates aligned to Stage 1 launch window. Priorities match dependency reality (font install = high pre-render; final pick = medium JP-gated; logo HTML = low cosmetic). |

## Blocked on

**Trixx critical path:** materials ready, nothing on our side.

**JP review for intro MP4 pick** (t-pick-website-intro-final-version): explicit user note "i will confirm once juan pablo choose."

**Laptop font install** (t-install-brand-fonts-laptop): Ricardo needs to be at the laptop with sudo. One-line apt install.

## Open questions (no blocking)

1. **Music vs no-music for the website intro.** Raised in-session, deferred to next editing pass. Carried in the journal's "Open creative question" section.

2. **Logo wordmark font reconciliation.** Logo kit HTML uses Century Gothic + Nunito; brand spec mandates Inter. Decision: restamp wordmark in Inter or accept divergence. Tracked in `t-fix-logo-kit-html-fonts`.

3. **Where to back up heavy marketing assets.** Currently ~10 GB of website-intro raw + transcoded + edits + exports live only on `ricardo-desktop`. Working files (regenerable), so acceptable now; if the final intro version is locked + Ricardo wants belt-and-suspenders, age-encrypt the final MP4 to Drive 2TB per heavy-assets-pattern.

## Files modified this session

Session-end commit (this one) will include:

- `STATUS.md` (header + session 11 block prepended)
- `tasks.json` (top-level `updated` bumped to 2026-05-22T15:25:18-07:00; 3 new tasks appended)
- `CHECKPOINT.md` (this file, rewritten)
- `00_META/journal/2026-05-22_marketing-folder-and-brand-font.md` (NEW)

Already on-disk (will be committed in the same commit):

- NEW `operations/marketing/README.md`
- NEW `operations/marketing/.gitignore`
- MODIFIED `skills/shared/brand.py` (BRAND_FONT = "Inter" + BRAND_FONT_MONO + 2 docstring updates)
- MODIFIED `skills/05_opportunity_report/scripts/generate_docx.py` (17 hardcoded `'Calibri'` → `BRAND_FONT`)
- DELETED `Temporal Assets and video/` (relocated, then removed)

NOT committed (gitignored, on-disk only):

- 18 logo PNGs under `operations/marketing/brand/logos/`
- 3 raw HEVC takes + 3 DNxHR HQ transcodes under `operations/marketing/website-intro/raw/`
- 2 DaVinci ProRes MKV edits + 2 H.264 MP4 web exports under `operations/marketing/website-intro/edits/`

Untouched this session (pre-existing untracked, not ours):

- `00_META/journal/2026-05-21_strategy-meeting-transcript.md` — pre-existing untracked from session 10's day, not authored by this session.

## Memory updates this session

None new. Existing memories applied:

- `outputs-premium-visual.md` — drove the Inter font choice + JetBrains Mono addition + the rationale for the cleanup.
- `do-it-right-do-it-once.md` — drove cleaning ALL 17 hardcoded `'Calibri'` literals in generate_docx.py (instead of just patching the constant) and documenting the DNxHR workflow in the README (instead of a one-off ffmpeg run).
- `complete-or-nothing.md` — drove bundling folder org + transcoding + font fix + web export + tests + task tracking + journal + commit in one session.

## Estimated time to next milestones

- **Trixx meeting (2026-05-25 1pm Tijuana):** T-3 days. Materials intact.
- **Skill 05 post-Trixx:** ~30-45 min execution + ~70 min wall-time large-v3 transcription + 30 min Ricardo+JP review.
- **t-install-brand-fonts-laptop:** ~2 min (one apt install + restart of any open LibreOffice instance).
- **t-pick-website-intro-final-version:** ~15-30 min (JP review + decision + file move + optional music decision).
- **t-fix-logo-kit-html-fonts:** ~30 min if accepting divergence (CSS-only change); ~2-4 hrs if restamping wordmark PNGs.
- **Stage 1 launch realistic:** 2026-06-30 to 2026-07-15 (unchanged).

## After this, what's next

Ricardo picks. Trixx Monday meeting (T-3 days) remains the critical-path gate; materials intact, nothing on our side blocks it. Otherwise: any open task from above. Font install on laptop is the cheapest meaningful follow-up (1 command, removes a font-substitution risk for the next deliverable rendered on the laptop).

## For a future auditor reading this baton

This was the 20th execution arc since 2026-05-15 and the 11th end-to-end Claude session. Tangential operational scope: no ADRs, no architecture changes, no impact on the critical Trixx-2026-05-25 path. Lasting value: (1) `operations/marketing/` folder convention + README documents future-campaign structure; (2) brand font finally unified at Inter (`skills/shared/brand.py:26` is now the single source of truth — closes a v0.1 memory-vs-code divergence); (3) DaVinci-on-Linux HEVC workaround documented so future phone shoots inherit the fix without re-discovery. Session quality: clean, in-scope, no drift, no half-measures, 32 PASS test-harness preserved across the renderer changes.

---

*This CHECKPOINT.md is the baton between sessions. Next session: type "Start Session" → Claude reads this + STATUS + tasks + calendar + latest journal → present the path forward.*
