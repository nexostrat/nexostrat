# CHECKPOINT — root (Founder)

**Updated:** 2026-05-23T12:05:00-07:00
**By:** ricardo (via Claude Code session 12 at /srv/Nexostrat/ on `ricardo-desktop`)
**Persona:** Founder
**Session topic:** Maintenance — fix DaVinci Resolve's MP4-export blocker (Celluloid won't play APV+FLAC inside MP4); build a reusable `video-to-mp4` CLI wrapper at `infra/scripts/`; document on the desktop machine cheatsheet; mid-session transcode of a new 4K HEVC phone take using the session-11 documented recipe. No architecture changes, no ADRs, no critical-path movement.

## What just happened (last session — read once, don't re-litigate)

Short maintenance session, ~30 min, two pieces of work — both extensions of session 11's DaVinci-on-Linux codec arc:

**1. DaVinci MP4 playback fix (export side of the codec gap).** Ricardo's `Intro V1.2.mp4` (direct DaVinci export) wouldn't play in Celluloid: "Playback was terminated abnormally." `ffprobe` against the three candidate files isolated it instantly — the broken file has video codec `unknown` + audio `flac` inside an MP4 container. FLAC-in-MP4 is technically allowed since 2019 but most Linux playback stacks (Celluloid via mpv via GStreamer) refuse it; combined with an unrecognized video codec the container is non-standard. Root cause: DaVinci Resolve **Free** on Linux lacks the H.264/H.265 encoder (Studio-only on Linux), leaving only APV+FLAC as MP4-container options out of Deliver. Fix applied twice over: (a) re-encoded `Intro V1.2.mkv` → `Intro V1.2.mp4` via `ffmpeg -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`, overwriting the broken 615 MB direct export with a 42 MB playable file; (b) built reusable CLI wrapper `infra/scripts/video-to-mp4.sh` (executable, version-controlled, `set -euo pipefail`, `-f` to force-overwrite, `-h` for help, env-var knobs `CRF` / `PRESET` / `AUDIO_BITRATE`). Symlinked to `/home/ricardo/.local/bin/video-to-mp4` so `video-to-mp4 <input>` works as a bare command on `ricardo-desktop`. Documented at `~/Desktop/DESKTOP_PC_COMMANDS.md` (outside repo, machine-scoped cheatsheet): new section "Video conversion (DaVinci → playable MP4)" + one quick-reference entry + changelog row.

**2. Mid-session 4K HEVC transcode (ingest side, same blocker as session 11).** Ricardo dropped `raw/2026-05-22_take-01.mp4` (HEVC Main 10, 3840×2160, 46s, 242 MB) and reported DaVinci couldn't open it. Same blocker as session 11; ran the documented `ffmpeg → DNxHR HQ MOV` recipe from `operations/marketing/README.md`. Output: `raw/transcoded/2026-05-22_take-01.mov` (DNxHR HQ, yuv422p, PCM 16-bit, 4.85 GB) — ready to import into DaVinci. The fix is now muscle memory; no re-discovery needed because session 11 documented it in the README.

**Result:** No architectural change. The DaVinci-Free-on-Linux codec gap is now closed on both sides — ingest (session 11's HEVC → DNxHR recipe in README) and export (session 12's `video-to-mp4` wrapper). Marketing video work no longer requires Ricardo to remember or look up codec recipes; both sides hit muscle-memory or one-line invocations. No new tasks added (script + cheatsheet are sufficient institutional memory; symlinking on the laptop is a 1-line `ln -sf` captured in the journal).

## Decisions locked this session

1. **Reusable converter at `infra/scripts/`, per-machine symlink in `~/.local/bin/`.** Pattern matches the rest of the repo's tooling — version-controlled script syncs to all clones; the symlink is the only per-machine bit. Default recipe baked in: h264 High + AAC LC 192k + yuv420p + `+faststart` at CRF 18 preset slow. Env vars override when needed. Reversal: trivial — remove the symlink + delete the script.

2. **CRF 18 preset slow as the default.** Near-lossless for talking-head footage from a ProRes/APV master; output is ~5-10% the size of the master. For a 1080p30 38s ProRes input the output is ~21-42 MB which fits browser/email/Slack uploads. If Ricardo finds the default too heavy or too light for a future shoot, env-var overrides (`CRF=23 ...` or `CRF=15 ...`) handle it without touching the script.

3. **Documentation at the desktop-cheatsheet layer, not the marketing README.** `~/Desktop/DESKTOP_PC_COMMANDS.md` is machine-scoped and lists `~/.local/bin` tools; that's where `video-to-mp4` belongs. `operations/marketing/README.md` covers project workflow (ingest recipe + folder convention); the export-side wrapper is a generic tool that any video work on this machine can use, not a marketing-specific recipe. Reversal: if future projects also need it, lift the section out of the cheatsheet into a `docs/` page.

4. **No new tasks added.** Decision rationale: the script is now in muscle memory + documented in two places (cheatsheet + this journal). Laptop symlink is a 1-line `ln -sf` captured in the journal's open-items section. Adding a task for it would be ceremony.

## Stack state (live & verifiable next session)

```
HP (ricardo-hp-laptop, Tailscale 100.64.121.80) — unchanged from session 10:
  baserow + bookstack + bookstack-db + caddy all healthy.
  systemd nexostrat-foss-stack.service enabled.
  Two nightly timers still MASKED (reconcile @03:30, schema-check @Mon04:00) —
    waiting on t-plan-02a-chunk-b-systemd-creds (high, due 2026-06-01).

Desktop (ricardo-desktop) — bootstrapped session 8 (journal 2026-05-20b):
  /srv/Nexostrat/ cloned + working tree active.
  Inter + JetBrains Mono installed system-wide (session 11).
  ALL skills runnable here; DaVinci Resolve installed; OBS + Whisper not
    (per t-desktop-pc-recording-stack-install).
  NEW session 12: ~/.local/bin/video-to-mp4 -> infra/scripts/video-to-mp4.sh

Recording + transcription stack — unchanged from session 9:
  Server laptop has OBS Studio 30.0.2 + pavucontrol 5.0
  Whisper.cpp /opt/whisper.cpp/ + models (small fallback, large-v3 preferred)
  ~/bin/transcribe.sh wrapper
  OBS profile audio-meeting

Vault discipline — unchanged from session 9:
  infra/age-recipients.txt: 2 keys (Ricardo, JP). C2 operationally closed.

Brain Bot Platform tenancy — locked session 10:
  ADR-039 active. ADR-020 superseded.

NEW this session (12) — operational additions:
  infra/scripts/video-to-mp4.sh (new, executable, version-controlled)
  ~/.local/bin/video-to-mp4 symlink on ricardo-desktop
  ~/Desktop/DESKTOP_PC_COMMANDS.md updated (outside repo, machine-scoped)
  edits/Intro V1.2.mp4 replaced (615 MB broken -> 42 MB playable; gitignored)
  raw/transcoded/2026-05-22_take-01.mov produced (4.85 GB; gitignored)
  Test harness not re-run (no skill-renderer changes; preserved baseline 32/0/0).
```

## In flight — concrete next actions

```
NEXT SESSION:
  1. Open Claude Code AT /srv/Nexostrat/.
  2. Ricardo types "Start Session."
  3. Claude reads CHECKPOINT + STATUS + tasks + calendar + latest journal
     (00_META/journal/2026-05-23_davinci-mp4-playback-fix.md).
  4. Ricardo decides arc.

CRITICAL PATH (unchanged from session 11):

  ┌── 2026-05-25 1pm Tijuana ─────────────────────────────┐
  │  REUNIÓN TRIXX LOGISTICS                               │
  │  (t-trixx-meeting-execution, critical)                 │
  │  T-2 days. Materiales en Desktop intactos.             │
  └─────────────────────┬──────────────────────────────────┘
                        │
  ┌── 2026-05-27 ─▼─────────────────────────────────────────┐
  │  SKILL 05 (Opportunity Report)                          │
  │  (t-trixx-skill-05-opportunity-report, high)            │
  └─────────────────────────────────────────────────────────┘

CARRIED FORWARD from session 11 (no new tasks this session):

  ┌── 2026-05-30 ─┐ (high)
  │  t-install-brand-fonts-laptop                           │
  │  sudo apt install fonts-inter fonts-jetbrains-mono     │
  │  on ricardo-hp-laptop.                                  │
  └───────────────┘

  ┌── 2026-06-15 ─┐ (medium) — NOW 3 candidates instead of 2
  │  t-pick-website-intro-final-version                     │
  │  Pick V1.0 vs V1.1 vs V1.2 of the website intro MP4.    │
  │  All three are h264+AAC playable mp4s now. JP-gated.    │
  │  Move chosen file edits/ → final/.                      │
  └───────────────┘

  ┌── 2026-07-15 ─┐ (low)
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

UNTRACKED follow-up (intentionally not a task):
  - Symlink video-to-mp4 on ricardo-hp-laptop when/if needed:
      ln -sf /srv/Nexostrat/infra/scripts/video-to-mp4.sh ~/.local/bin/video-to-mp4
```

## Architecture-conflict check (passed)

| This session's work | Verification |
|---|---|
| New script under `infra/scripts/` | Founder-owned per root CLAUDE.md Strict Rule 2. Pattern matches existing scripts (`baserow-reconcile.sh`, `mirror-push.sh`, etc.). |
| No `/srv/brain` references introduced | Confirmed by review. Strict Rule 4 preserved. |
| No edits to skills/, pipeline/, vault/, GEMINI.md | All work stayed in Founder-owned paths. |
| No backwards-compat shims, no half-finished implementations | Script is complete + documented + symlinked + executed against a real input. |
| Test harness not affected | No skill-renderer changes; previous baseline 32 PASS · 0 SKIP · 0 FAIL preserved by non-disturbance. |

## Blocked on

**Trixx critical path:** materials ready, nothing on our side. T-2 days.

**JP review for intro MP4 pick** (t-pick-website-intro-final-version): now 3 candidates (V1.0, V1.1, V1.2) all in playable h264+AAC mp4. Explicit user note from session 11: "i will confirm once juan pablo choose."

**Laptop font install** (t-install-brand-fonts-laptop): Ricardo needs to be at the laptop with sudo. One-line apt install.

## Open questions (no blocking)

1. **Music vs no-music for the website intro.** Carried from session 11. Deferred to next editing pass.

2. **DaVinci Resolve Studio purchase ($295 one-time).** Would eliminate the need for `video-to-mp4` by unlocking H.264/H.265 directly in Deliver. Worth revisiting if Ricardo runs the wrapper more than ~5×/week.

3. **Where to back up heavy marketing assets.** Carried from session 11. Same posture: working files, regenerable, acceptable on `ricardo-desktop` only. Now ~15 GB after the session-12 4K transcode.

## Files modified this session

Session-end commit (this one) will include:

- `STATUS.md` (header + session 12 block prepended)
- `CHECKPOINT.md` (this file, rewritten)
- `00_META/journal/2026-05-23_davinci-mp4-playback-fix.md` (NEW)
- `infra/scripts/video-to-mp4.sh` (NEW, executable)

Outside repo (already on-disk, not committed):

- `~/Desktop/DESKTOP_PC_COMMANDS.md` — new section "Video conversion (DaVinci → playable MP4)" + 1 quick-ref entry + changelog row
- `~/.local/bin/video-to-mp4` — symlink to `/srv/Nexostrat/infra/scripts/video-to-mp4.sh`

NOT committed (gitignored, on-disk only):

- `operations/marketing/website-intro/edits/Intro V1.2.mp4` — replaced 615 MB broken → 42 MB playable
- `operations/marketing/website-intro/raw/transcoded/2026-05-22_take-01.mov` — new 4.85 GB DNxHR HQ edit master

Untouched this session (pre-existing untracked, carried from session 10/11):

- `00_META/journal/2026-05-21_strategy-meeting-transcript.md` — pre-existing untracked from session 10's day, deliberately not committed in session 11 either. Continuing that pattern.

## Memory updates this session

None new. Existing memories applied:

- `do-it-right-do-it-once.md` — drove building the reusable wrapper script + symlink + cheatsheet documentation (instead of just running ffmpeg one-shot for V1.2). Same operational arc as session 11's batch-loop documentation in the marketing README.
- `complete-or-nothing.md` — drove bundling diagnose + fix + tool + docs + journal + commit in one session, including the mid-session 4K take that arrived as a surprise.

## Estimated time to next milestones

- **Trixx meeting (2026-05-25 1pm Tijuana):** T-2 days. Materials intact.
- **Skill 05 post-Trixx:** ~30-45 min execution + ~70 min wall-time large-v3 transcription + 30 min Ricardo+JP review.
- **t-install-brand-fonts-laptop:** ~2 min (one apt install + restart of any open LibreOffice instance).
- **t-pick-website-intro-final-version:** ~15-30 min (JP review across 3 candidates + decision + file move + optional music decision).
- **Stage 1 launch realistic:** 2026-06-30 to 2026-07-15 (unchanged).

## After this, what's next

Ricardo picks. Trixx Monday meeting (T-2 days) remains the critical-path gate; materials intact, nothing on our side blocks it. Otherwise: any open task from above. Font install on laptop is still the cheapest meaningful follow-up (1 command, removes a font-substitution risk for the next deliverable rendered on the laptop).

## For a future auditor reading this baton

This was the 21st execution arc since 2026-05-15 and the 12th end-to-end Claude session. Maintenance scope: no ADRs, no architecture changes, no impact on the critical Trixx-2026-05-25 path. Lasting value: (1) DaVinci-on-Linux codec gap closed on both sides — session 11's `operations/marketing/README.md` covers the ingest recipe, session 12's `infra/scripts/video-to-mp4.sh` covers the export recipe + CLI wrapper; (2) `~/Desktop/DESKTOP_PC_COMMANDS.md` accumulated a new section + quick-ref entry, growing the per-machine cheatsheet without bloating the project repo. Session quality: tight scope, fast diagnosis from ffprobe, no scope creep into adjacent concerns, mid-session surprise (the 4K take) handled cleanly using the recipe already documented in the marketing README. No tests run because no skill-renderer code changed.

---

*This CHECKPOINT.md is the baton between sessions. Next session: type "Start Session" → Claude reads this + STATUS + tasks + calendar + latest journal → present the path forward.*
