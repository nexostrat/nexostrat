# Session 8 — Recording + Transcription Stack Operational

**Date:** 2026-05-19 PM (eighth session)
**Persona:** Founder
**Topic:** Stand up the meeting-recording + audio-transcription stack on the server laptop ahead of tomorrow's online meetings and the Trixx Monday pilot. Mid-arc, pivot to a new file-organization pattern; consolidate command references.

---

## Arc shape

Tactical arc, not architectural. Started with a strategic question ("when are we installing meeting recording / can we jump ahead?") and ended with a working end-to-end chain: OBS Studio captures mic + system audio → ffmpeg extracts WAV → Whisper.cpp transcribes Spanish via `~/bin/transcribe.sh` wrapper. Plus a mid-session organizational pivot that produced two `COMMANDS.md` files (one inside the Nexostrat repo, one on the laptop's Desktop) replacing a single Operations Guide that had been written earlier in the same session.

## Decision tree walked

1. **Strategic question**: install the meeting-capture stack now, or defer to Plan 08?

   **Resolution**: install now. Plan 08's scope is the *automation glue* (T-15 reminders, `/meeting start|end` commands, event router, Ollama summarization, Telegram digest). The *binaries* — Whisper.cpp + ffmpeg + a recording GUI — are PC-level capability with zero architectural surface. Installing them does not pre-commit to any Plan 08 design. Verified pre-existing install at `/opt/whisper.cpp/` (built, `ggml-small.bin` present); only OBS Studio + pavucontrol needed to fill the gap.

2. **Recording tool choice**: OBS Studio (GUI, ~150 MB) vs. minimal CLI (pavucontrol + ffmpeg wrapper, ~2 MB)?

   **Resolution**: OBS. Reliability + visual confirmation (red REC indicator + audio level meters) outweighs the footprint for client-meeting recording where mid-call certainty matters. The CLI alternative would have worked too — both paths were valid.

3. **Recording profile config**: NVENC (GPU encode) or x264 (CPU encode)?

   **Resolution**: x264. NVIDIA driver not installed; NVENC raised an error. Swapped to Software (x264) at 640×360@10fps — the video is throwaway (we discard it via `ffmpeg -vn`), so neither resolution nor encoder quality matter. CPU cost is negligible for an audio-only effective recording.

4. **OBS Sources panel — add audio sources or not?**

   **Resolution (hard-won)**: leave Sources empty. Adding "Application Audio Capture" / "Audio Output Capture" sources from the Sources panel creates PipeWire loopback nodes that hijack the system's default sink. Mid-session this manifested as: closing OBS didn't restore system audio. Root cause: the OBS process was still alive (window closed ≠ process killed). Fix: `pkill -f /usr/bin/obs`. The correct OBS audio-capture mechanism is **Settings → Audio → Global Audio Devices** (Desktop Audio + Mic/Aux set to Default), NOT Sources panel additions. This is now documented as a hard rule in both COMMANDS.md files.

5. **Whisper model choice**: stay on `small` (466 MB, ~85-90% Spanish accuracy) or upgrade to `large-v3` (~3 GB, ~95-97%)?

   **Resolution**: download `large-v3`. Ricardo opted for max accuracy despite the slower transcribe time (~2.3× real-time on this laptop CPU). `transcribe.sh` auto-prefers large-v3 if present; `small` remains as fallback. Accuracy bump confirmed on the same 16.5-second smoke-test clip: `small` heard "ese momento", `large-v3` correctly heard "este momento" — subtle but real.

6. **Profile structure for video-or-audio recording**: one config or two OBS Profiles?

   **Resolution**: two profiles, configure only the audio one today. `audio-meeting` (640×360@10fps, x264, low bitrate) created and tested. The `video` profile (1920×1080@30fps, x264 medium) is documented for future setup; not configured today per Ricardo's explicit "we will setup only audio today".

7. **File organization pivot (mid-session)**: Ricardo flagged that he'd "been creating command files all around and by now I'm lost".

   **Resolution**: locked a new convention.
   - One `COMMANDS.md` per project folder. Sections divided by computer (e.g., Server PC, Desktop PC, Other PCs). File lives in the project folder so it travels via git.
   - One `~/Desktop/COMMANDS.md` per PC. Aggregator: pointers to each project's `COMMANDS.md` + general Linux reference + PC-specific specifics (installed services, ports, paths, SSH aliases).
   - This replaces ad-hoc command files scattered on Desktop.

   Applied immediately to Nexostrat: `/srv/Nexostrat/COMMANDS.md` (~380 lines) + `~/Desktop/COMMANDS.md` (~325 lines). The single `~/Desktop/Nexostrat-Operations-Guide.md` written earlier in the same session was deleted post-migration.

## Concrete deliverables

- **OBS Studio 30.0.2 + pavucontrol 5.0** installed via apt.
- **`audio-meeting` OBS profile** configured: Simple output mode, MKV format, x264 encoder, Quality "High Quality, Medium File Size", 640×360@10fps, Global Audio Devices `Default` for both, Sources panel empty.
- **`ggml-large-v3.bin`** (2.9 GB) downloaded to `/opt/whisper.cpp/models/`. Models dir `chown`ed to `ricardo:ricardo` so future model downloads don't require sudo.
- **`~/bin/transcribe.sh`** (~50 LOC bash): auto-selects model preference `large-v3 > medium > small`, takes input + optional language, produces `<input>.txt` next to input. End-to-end smoke-tested.
- **`/srv/Nexostrat/COMMANDS.md`** (~380 lines): Server PC section (Nexostrat daily/periodic operations), Desktop PC section (recording stack install — fully reproducible top-to-bottom, plus per-meeting workflow + transcript transfer), Other PCs placeholder, Whisper model selection table, flat appendix.
- **`~/Desktop/COMMANDS.md`** (~325 lines): This-PC aggregator with PC info, project pointers, recording stack PC-level workflow, general Linux reference (~50 commands), this-PC specifics.
- **`~/Desktop/Nexostrat-Operations-Guide.md`** (644 lines): created earlier in same session, deleted post-migration.

## End-to-end validation

| Stage | Result |
|---|---|
| OBS records mic + system audio | ✓ both bars bounce in Audio Mixer |
| `.mkv` lands in `~/Videos/` | ✓ 404 KB for 16.5s test |
| ffmpeg extracts 16 kHz mono WAV | ✓ |
| Whisper-cli (`small`) transcribes Spanish | ✓ "Esto es una prueba ... Voy a poner música en ese momento." |
| Whisper-cli (`large-v3`) transcribes Spanish | ✓ "...en **este** momento" — corrected the small-model miss |
| Both halves of recording amplitude-checked | ✓ first half -34 dB mean (mic), second half -27 dB mean (system audio); both captured cleanly |
| `transcribe.sh` auto-picks large-v3 once present | ✓ stdout: `>> model: ggml-large-v3.bin` |

## Performance notes

- Whisper large-v3 on this laptop CPU: ~2.3× real-time. 30-min meeting → ~70 min transcribe. Acceptable for overnight or background runs. The desktop PC (more powerful) will run faster.
- 30-min meeting recording at 640×360@10fps + ~128 kbps audio = ~50 MB `.mkv`. Disk cost trivial.
- 60 MB/s download speed observed during model fetch — network is fine.

## What was NOT done (deliberate)

- **Did not install Ollama on the server laptop.** Ricardo mentioned considering a small model for future local summarization but explicitly deferred: "Ollama is installed in another pc so we can skip it ... we can revise that an try to implement even the smaller model to see what happens" — future-track item, not today.
- **Did not install NVIDIA proprietary driver.** Software x264 encoding works fine for audio-purposed recording. Defer NVIDIA install until a use case requires GPU encoding (long screen recordings, multi-stream).
- **Did not write any scripts inside `/srv/Nexostrat/`.** All capability lives in `~/bin/`, `/opt/whisper.cpp/`, system `apt` packages — outside the repo. The only repo-touching artefact is `/srv/Nexostrat/COMMANDS.md` (documentation, not infrastructure).
- **Did not pre-commit to Plan 08 design.** No event-router hooks, no Baserow transcript table, no `/meeting start|end` commands, no Telegram digest. Plan 08 will design those when written.
- **Did not migrate AttenBot-Commands.md** from Desktop into AttenBot's folder per the new pattern. Outside Nexostrat scope; tracked mentally for Ricardo to do when he session-works AttenBot.

## Memories updated this session

None. Existing memories (e.g., `feedback_complete_or_nothing`, `feedback_do_it_right_do_it_once`) applied consistently throughout — particularly the smoke-test-end-to-end + verify-amplitude-of-both-halves discipline.

## Files touched

**Repo (in session-end commit):**

- `STATUS.md` — header updated + session-8 block prepended
- `tasks.json` — one new task (`t-desktop-pc-recording-stack-install`)
- `CHECKPOINT.md` — rewritten baton
- `00_META/journal/2026-05-19_recording-stack-setup.md` — this file (NEW)
- `COMMANDS.md` — new file at repo root (NEW)

**Outside repo (no commit):**

- `~/Desktop/COMMANDS.md` — created
- `~/Desktop/Nexostrat-Operations-Guide.md` — deleted (same-session create + delete)
- `~/bin/transcribe.sh` — created
- `/opt/whisper.cpp/models/ggml-large-v3.bin` — downloaded
- OBS Studio + pavucontrol installed via apt
- OBS profile `audio-meeting` created in `~/.config/obs-studio/basic/profiles/audio-meeting/`

## For the next session

Ricardo's choice. Open paths:

1. **Trixx Monday pilot** (T-6 days) — meeting itself, then Skill 05 production. Unchanged.
2. **Plan 02a Chunk B follow-ups** — `t-plan-02a-chunk-b-systemd-creds` (high, due 2026-06-01) is the most operationally pressing (re-enables the masked nightly timers). Plus the hook-lift and test-coverage follow-ups (both medium, due 2026-06-10).
3. **Plan 02a Chunk C** — BookStack content + backup/recovery + tag `v0.2a-foss-stack`. Recommended after Chunk-B-follow-up Task `t-plan-02a-chunk-b-systemd-creds` so the new nightly backup timer joins healthy peers.
4. **Plan 02b write** — Diátaxis docs + drift hook + auto-generators + ADRs 021-035 + how-tos.
5. **Desktop PC recording stack install** — `t-desktop-pc-recording-stack-install` (medium, due 2026-06-15); standalone setup task, can be done from the desktop PC directly once you scp `/srv/Nexostrat/COMMANDS.md` over.

Whatever Ricardo picks, the recording chain is now available for any of them — including the Trixx post-meeting Skill 05 invocation, which is the gating use of this session's work.
