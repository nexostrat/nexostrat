# CHECKPOINT — root (Founder)

**Updated:** 2026-05-19T21:05:00-07:00
**By:** ricardo (via Claude Code session 8 at /srv/Nexostrat/)
**Persona:** Founder
**Session topic:** Stand up the meeting-recording + transcription stack on the server laptop (OBS + Whisper.cpp large-v3 + `~/bin/transcribe.sh`). Lock a new file-organization pattern (one `COMMANDS.md` per project folder, sections per PC, plus one `~/Desktop/COMMANDS.md` aggregator per PC). Produce both files. Tactical arc, zero architecture impact.

## What just happened (last session — read once, don't re-litigate)

Tactical operational session. Started with a strategic question — *"when are we installing meeting-recording software, can we jump ahead?"* — and ended with a working end-to-end recording + transcribe chain plus a refactor of the personal command-file layout.

**Result:**

- **OBS Studio 30.0.2 + pavucontrol 5.0** installed via apt. `audio-meeting` profile configured: Simple output, MKV format, **Software (x264) encoder** (NOT NVENC — NVIDIA driver not installed; NVENC raised an error), 640×360@10fps, Global Audio Devices = `Default` for both Desktop Audio + Mic/Aux, Sources panel empty.
- **Whisper.cpp `ggml-large-v3.bin`** (~2.9 GB, ~95-97% Spanish accuracy) downloaded. `/opt/whisper.cpp/models/` chowned to ricardo. Existing `ggml-small.bin` retained as fallback.
- **`~/bin/transcribe.sh`** wrapper landed (~50 LOC bash). Auto-prefers `large-v3 > medium > small`. Smoke-tested end-to-end.
- **`/srv/Nexostrat/COMMANDS.md`** (~380 lines) — canonical Nexostrat ops runbook at repo root. Sections per PC (Server, Desktop, Other) plus Whisper model table + flat appendix.
- **`~/Desktop/COMMANDS.md`** (~325 lines) — this PC's aggregator. Project pointers + general Linux ref + PC-specific specifics.
- **`~/Desktop/Nexostrat-Operations-Guide.md`** — created earlier in same session as monolithic Operations Guide (644 lines), deleted post-migration once the COMMANDS.md split was decided.

## Decisions locked this session

1. **Install timing for meeting capture.** Binaries (Whisper.cpp + ffmpeg + recording GUI) are PC-level capability with zero Plan 08 architectural surface. Installing them now pre-commits to nothing. Plan 08's eventual scope is the *automation glue* (event router, Telegram digest, Ollama summarization) — separable from the binaries themselves.

2. **OBS audio capture mechanism.** Use **Settings → Audio → Global Audio Devices** (Desktop Audio + Mic/Aux set to `Default`). **Never add audio sources from the Sources panel** — they create PipeWire loopback nodes that hijack system routing (mid-session bug: adding such sources killed system audio system-wide until the lingering OBS process was killed). The Sources panel is for *video* sources; audio mixing in OBS is configured via Settings → Audio.

3. **OBS encoder.** Software (x264) for all profiles until NVIDIA driver is installed. x264 is actually higher quality than NVENC at same bitrate; the only cost is CPU (negligible for audio-purposed recording). NVIDIA driver install is a separate future task, not gated on anything.

4. **Whisper model strategy.** Default to `large-v3` (3 GB, ~95-97% Spanish accuracy). Keep `small` (466 MB) as auto-fallback. `transcribe.sh` does the model preference logic internally. `~/.config` or `WHISPER_MODEL=...` env-var override available for power-user cases.

5. **OBS Profiles strategy.** Two profiles planned — `audio-meeting` (configured today: 640×360@10fps, throwaway video) and `video` (future setup: 1920×1080@30fps, x264 medium). Switch via OBS top menu Profile → before each recording.

6. **NEW file-organization pattern** (introduced by Ricardo mid-session):
   - **One `COMMANDS.md` per project folder.** Sections per computer. File lives inside the project folder so it travels via git. *Project-local commands.*
   - **One `~/Desktop/COMMANDS.md` per PC.** Aggregator: project-folder pointers + general Linux reference + this-PC specifics. *PC-local navigation.*
   - Pattern supersedes the ad-hoc-files-on-Desktop scatter. `AttenBot-Commands.md` still exists on Desktop and should eventually migrate to its project folder (out of scope for Nexostrat sessions).

7. **No script/glue lands in `/srv/Nexostrat/`.** All capability lives in `~/bin/`, `/opt/`, system `apt` packages — outside the repo. The only Nexostrat-repo artefact this session is the new `COMMANDS.md` documentation file. Plan 08 territory remains unwritten and unaffected.

## Stack state (live & verifiable next session)

```
HP (ricardo-hp-laptop, Tailscale 100.64.121.80) — unchanged from session 7:
  baserow + bookstack + bookstack-db + caddy all healthy.
  systemd nexostrat-foss-stack.service enabled.
  Two nightly timers still MASKED (reconcile @ 03:30, schema-check @ Mon 04:00) —
    waiting on t-plan-02a-chunk-b-systemd-creds (high, due 2026-06-01).

NEW this session — recording + transcription stack:
  OBS Studio 30.0.2 (apt)
  pavucontrol 5.0 (apt)
  Whisper.cpp /opt/whisper.cpp/ — pre-existing build
    models/ggml-small.bin   (466 MB) — fallback
    models/ggml-large-v3.bin (2.9 GB) — preferred
  ~/bin/transcribe.sh — wrapper auto-prefers large-v3
  OBS profile audio-meeting:
    640×360 @ 10 fps · Software (x264) · MKV · ~/Videos · Global Audio Devices = Default

NEW files in repo:
  /srv/Nexostrat/COMMANDS.md (~380 lines)
    → Canonical Nexostrat ops runbook, sections per PC.
```

## In flight — concrete next actions

```
NEXT SESSION:
  1. Open Claude Code AT /srv/Nexostrat/.
  2. Ricardo types "Start Session."
  3. Claude reads CHECKPOINT + STATUS + tasks + calendar + latest journal
     (00_META/journal/2026-05-19_recording-stack-setup.md).
  4. Ricardo decides arc.

CRITICAL PATH UNCHANGED FROM SESSION 7:

  ┌── 2026-05-25 1pm Tijuana ─────────────────────────────┐
  │  REUNIÓN TRIXX LOGISTICS                               │
  │  (t-trixx-meeting-execution, critical)                 │
  │  Materiales: 4 PDFs en Desktop (intactos)              │
  │  Recording stack: phone voice memo (in-person)         │
  │    → transfer to laptop → transcribe.sh → Skill 05     │
  └─────────────────────┬──────────────────────────────────┘
                        │
  ┌── 2026-05-27 ─▼─────────────────────────────────────────┐
  │  SKILL 05 (Opportunity Report)                          │
  │  (t-trixx-skill-05-opportunity-report, high)            │
  │  Consume: 4 reportes + transcript + notas reunión       │
  │  → Revisión Ricardo+JP (Fase 5) → entrega (Fase 6)      │
  └─────────────────────────────────────────────────────────┘

PARALLEL TRACK — Chunk B follow-ups (architectural):

  ┌── 2026-06-01 ─┐
  │  t-plan-02a-chunk-b-systemd-creds (high)                │
  │  Fix nightly timer creds — write /etc/nexostrat/        │
  │  baserow.env mode 0640, swap unit ExecStart to use      │
  │  EnvironmentFile=, unmask + enable --now both timers.   │
  │  ~30-45 min.                                             │
  └───────────────┘

  ┌── 2026-06-10 ─┐
  │  t-plan-02a-chunk-b-renderer-hook-lift (medium)         │
  │  Lift 27-LOC renderer hook into skills/shared/baserow:  │
  │  post_from_render(md, docx, skill_name). 5 renderers    │
  │  each become 1 line. ~45 min.                            │
  └───────────────┘

  ┌── 2026-06-10 ─┐
  │  t-plan-02a-chunk-b-test-coverage (medium)              │
  │  4 small test additions (~95 LOC total). ~30 min.       │
  └───────────────┘

NEW THIS SESSION:

  ┌── 2026-06-15 ─┐
  │  t-desktop-pc-recording-stack-install (medium)          │
  │  Replicate today's stack on the desktop PC. Follow      │
  │  /srv/Nexostrat/COMMANDS.md → "Desktop PC" section.     │
  │  6 sub-steps: apt + cmake whisper.cpp + download        │
  │  large-v3 + transcribe.sh + OBS audio-meeting profile   │
  │  + verify e2e. ~15-30 min + model download time.        │
  └───────────────┘

CHUNK C — next major arc (architecture):

  ┌── 2026-06-12 ─┐
  │  t-plan-02a-execute-chunk-c (medium)                    │
  │  Plan 02a Tasks 11-20: BookStack shelves + books +      │
  │  seeded pages, backup scripts, recovery scripts,        │
  │  sync-state-from-baserow.sh, 5 runbooks, smoke-test     │
  │  extension, e2e test, master index + tag v0.2a-foss-    │
  │  stack. Recommended order: do systemd-creds first so    │
  │  the new nightly backup timer joins a healthy ecosystem.│
  └───────────────┘

  ┌── 2026-06-30 ─┐
  │  t-plan-02b-write (medium)                              │
  │  Just-in-time write via writing-plans skill. Scope:     │
  │  docs/ Diátaxis + drift hook + 5 auto-generators + 15   │
  │  ADRs 021-035 + 10 how-tos + paired -explicado.md.      │
  └───────────────┘

OTHER OPEN (unchanged from session 7):
  - t-vault-backup-foss-env (medium, due 2026-06-30) — plan defect
  - t-whatsapp-andrea-audiencia (high, due 2026-05-23) — optional
  - t-practice-meeting-jp (low, due 2026-05-24) — optional
  - t-migrate-pilotos-to-clients (medium, due 2026-05-30) — parallel
  - t-presentation-refresh-post-adr-038 (high, due 2026-06-01)
```

## Architecture-conflict check (passed)

| This session's work | Verification |
|---|---|
| OBS + Whisper.cpp install | PC-level capability. No Nexostrat repo internals touched. Plan 08 territory remains unwritten + unaffected. |
| `~/bin/transcribe.sh` lives outside repo | Personal helper script. Plan 08 will write its own automation glue when it lands. |
| `/srv/Nexostrat/COMMANDS.md` in repo | Documentation file. Doesn't conflict with any plan; complements CLAUDE.md (which is *context*, not ops reference). |
| New file-org pattern | Convention for Ricardo's personal organization. No conflict with repo structure or any persona's scope. |
| OBS profile config in `~/.config/obs-studio/` | User-level OBS state. Not architecturally relevant. |

## Blocked on

**Next-session priority 1 (Trixx meeting):** nada del lado nuestro — materiales en Desktop, recording stack ready (phone voice recorder Monday → `transcribe.sh` Tuesday → `/opportunity-report` skill).

**Tomorrow's online meetings:** can use either this laptop (full stack here) or desktop PC (after `t-desktop-pc-recording-stack-install` runs). Laptop suffices if desktop PC install slips.

**Chunk B follow-ups (3) + Chunk C:** unchanged from session 7. Recommended order still systemd-creds → hook-lift → test-coverage → Chunk C.

**Warm-standby Tasks 7-12 Plan 01b:** physical second host (unchanged).

## Open questions (no blocking)

1. **Ollama on the server laptop?** Ricardo mentioned interest in testing whether a small Ollama model runs usably on this CPU-only machine. Deferred this session ("we can revise that an try to implement even the smaller model to see what happens"). Open for future session. Not architectural — Ollama on this PC would be standalone, not wired into Nexostrat.

2. **Desktop PC OS version assumption.** `t-desktop-pc-recording-stack-install` documented for **Linux Mint** matching the laptop. If the desktop PC turns out to be on a different distro (Ubuntu/Fedora/etc.), the apt commands need swapping. Currently assumed Mint per Ricardo's session statement.

3. **AttenBot file migration.** `~/Desktop/AttenBot-Commands.md` still exists on Desktop. Per the new pattern it should move to AttenBot's project folder. Out of scope for Nexostrat sessions; flagged in `~/Desktop/COMMANDS.md` as a known migration deferred.

## Files modified this session

Session-end commit will include:

- `STATUS.md` (header + session 8 block prepended)
- `tasks.json` (added `t-desktop-pc-recording-stack-install`)
- `CHECKPOINT.md` (this file, rewritten)
- `00_META/journal/2026-05-19_recording-stack-setup.md` (NEW)
- `COMMANDS.md` (NEW at repo root)

**Outside the repo (manual changes on HP):**

- `~/Desktop/COMMANDS.md` (NEW, ~325 lines, this-PC aggregator)
- `~/Desktop/Nexostrat-Operations-Guide.md` (created earlier in session, deleted post-migration)
- `~/bin/transcribe.sh` (NEW, ~50 LOC wrapper)
- `/opt/whisper.cpp/models/ggml-large-v3.bin` (downloaded, ~2.9 GB)
- `/opt/whisper.cpp/models/` (chowned `ricardo:ricardo`)
- `obs-studio` + `pavucontrol` + `vlc` (deps) installed via apt
- `~/.config/obs-studio/basic/profiles/audio-meeting/` (OBS profile config)
- `~/Videos/2026-05-19 20-25-26.mkv` + `.txt` (smoke-test recording + transcript, can be deleted any time)

## Memory updates this session

None new. Existing memories applied — particularly:
- `feedback_complete_or_nothing.md` — drove the end-to-end smoke test rather than declaring done at install time
- `feedback_do_it_right_do_it_once.md` — drove the audio-amplitude verification of both halves rather than trusting "Whisper transcribed your voice → done"
- `feedback_outputs_premium_visual.md` — drove the COMMANDS.md structure (tables, scannable headings, clean code blocks)
- `feedback_honestidad_brutal_evaluacion.md` — drove the explicit "music isn't in the transcript, but amplitude proves capture worked, here's the proof" framing rather than glossing over

## Estimated time to next milestones

- **Tomorrow (2026-05-20):** any online meeting → record on this laptop (OBS audio-meeting profile) → transcribe via `transcribe.sh`. ~5 min setup time per meeting.
- **Trixx meeting (2026-05-25):** unchanged — 30 min meeting + 30 min prep.
- **Skill 05 post-Trixx:** ~30-45 min execution + ~70 min wall-time for large-v3 transcription of ~30-min recording + 30 min Ricardo+JP review.
- **`t-desktop-pc-recording-stack-install`:** ~15-30 min + ~5-10 min model download time (depending on desktop PC connection).
- **`t-plan-02a-chunk-b-systemd-creds`:** ~30-45 min.
- **Chunk B follow-ups (3) + Chunk C:** unchanged from session 7 estimates.
- **Stage 1 launch realistic:** 2026-07-15 to 2026-07-30 (unchanged).

## After this, what's next

Ricardo picks. Recording stack is operational on the server laptop. Trixx Monday materials remain intact. Architecture work (Chunk B follow-ups → Chunk C → Plan 02b → Plans 03+04+05-10) all unchanged from session 7's baton.

## For a future auditor reading this baton

This was the 17th execution arc since 2026-05-15. Pattern reinforced: even tactical, non-architectural sessions deserve the same end-to-end verification discipline as the architectural ones. Specifically:
- Don't trust "the install completed" → verify by running the chain on test data.
- When the test produces unexpected output (e.g., "music not in transcript"), don't gloss over — check the lower-level signal (amplitude in this case) to distinguish "feature not used" from "feature broken".
- The OBS Sources-panel-kills-audio bug was the kind of subtle integration failure that only mid-session manual testing would surface; documenting the fix and the root cause in COMMANDS.md prevents the next user (Ricardo on desktop PC, or future-Ricardo on a re-install) from re-hitting it.

The session-end bookkeeping commit (next) locks all of this. Next session opens with: Ricardo's choice among (a) Chunk B follow-ups (recommended: systemd-creds first), (b) Chunk C straight, (c) post-Trixx Skill 05 if meeting has occurred, (d) Plan 02b write, (e) Desktop PC stack install (likely done from the desktop PC directly, not from this laptop), (f) something else.

---

*This CHECKPOINT.md is the baton between sessions. Next session: type "Start Session" → Claude reads this + STATUS + tasks + calendar + latest journal → present the path forward.*
