# 2026-05-23 — DaVinci MP4 playback fix + reusable converter + take-01 transcode

**Session type:** maintenance
**Duration:** ~30 min
**Agent:** Claude

## What was done

- Diagnosed Ricardo's reported symptom ("DaVinci MP4 exports won't play in Celluloid — `Playback was terminated abnormally`"). Probed three files side-by-side with `ffprobe`:
  - `operations/marketing/website-intro/edits/Intro V1.0.mp4` (yesterday's working conversion) — h264 High + AAC LC.
  - `operations/marketing/website-intro/edits/Intro V1.2.mp4` (broken DaVinci direct export, 615 MB) — video codec `unknown` + audio `flac`. Non-standard MP4; mpv/GStreamer-stack players refuse FLAC-in-MP4 by default.
  - `operations/marketing/website-intro/edits/Intro V1.2.mkv` (source) — ProRes HQ + PCM 24-bit.
- Confirmed root cause: DaVinci Resolve **Free** on Linux lacks the H.264/H.265 encoder (Studio-only on Linux). The only MP4 codecs offered in this build are APV (video) + FLAC (audio) — both mastering codecs that no standard playback stack supports inside MP4.
- Re-encoded `Intro V1.2.mkv` → `Intro V1.2.mp4` overwriting the broken file: `ffmpeg -i input.mkv -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart output.mp4`. Result: 42 MB, h264 High + AAC LC, plays normally in Celluloid.
- Built reusable CLI wrapper at `/srv/Nexostrat/infra/scripts/video-to-mp4.sh` (executable; `set -euo pipefail`; sane error messages; `-f` to overwrite; `-h` for help; env-var knobs `CRF` / `PRESET` / `AUDIO_BITRATE`). Default recipe matches the one used above. Symlinked to `/home/ricardo/.local/bin/video-to-mp4` so `video-to-mp4 <file>` works as a bare command on `ricardo-desktop`.
- Documented in `/home/ricardo/Desktop/DESKTOP_PC_COMMANDS.md` (outside repo): new section "Video conversion (DaVinci → playable MP4)" placed between Meeting-transcription and DroidCam; one quick-reference row added; changelog row appended. Includes basic usage, env-var knobs, ffprobe diagnosis one-liner, and the DaVinci-side workaround attempt (switch container from MP4 to QuickTime in case H.264 appears there).
- **Mid-session add:** Ricardo dropped a new phone take `raw/2026-05-22_take-01.mp4`. Probed → HEVC Main 10 at 3840×2160 (4K). Same blocker as session 11; ran the documented `ffmpeg → DNxHR HQ MOV` recipe from `operations/marketing/README.md`. Output: `raw/transcoded/2026-05-22_take-01.mov`, 4.85 GB, ready to import into DaVinci. Disk after: 228 GB / 1.8 TB used.

## Decisions made

- **Re-use, don't re-invent.** The new converter script lives at `infra/scripts/video-to-mp4.sh` (version-controlled, syncs to all clones) with a per-machine symlink at `~/.local/bin/video-to-mp4`. Why: same pattern as the rest of the repo's tooling. Future: if marketing video work expands to the laptop, one-line symlink there reuses the script.
- **CRF 18 + preset slow + AAC 192k as default.** Visually-lossless for talking-head footage from a ProRes/APV master, ~5-10% the size. Env vars expose the knobs if a future shoot needs different trade-offs.
- **No new tasks added.** The script + cheatsheet entry are sufficient institutional memory. Symlinking on the laptop is a one-liner that doesn't merit task tracking.
- **Did not touch `operations/marketing/README.md`.** Existing README covers the ingest side (HEVC → DNxHR for editing). The new script covers the export side (APV/ProRes → h264 for playback) and is documented at the desktop-cheatsheet layer because it's a machine-scoped CLI tool, not a project workflow.

## Open items

- `t-pick-website-intro-final-version` (medium 2026-06-15) — now has 3 candidates instead of 2: V1.0, V1.1, V1.2. Still JP-gated.
- New take `raw/transcoded/2026-05-22_take-01.mov` is ready for DaVinci import — Ricardo's next editing pass to integrate or skip.
- Symlink `video-to-mp4` on `ricardo-hp-laptop` is a 1-line `ln -sf` if/when the laptop becomes a video-editing surface. Not tracked as a task; lives only in this journal.

## Notes

- Two related blockers are now both documented and tooled. Session 11 covered the ingest side (Pixel HEVC Main 10 → DNxHR HQ MOV for DaVinci editing, documented in `operations/marketing/README.md`). This session covers the export side (DaVinci's APV+FLAC MP4 → h264+AAC MP4 for playback, documented in `~/Desktop/DESKTOP_PC_COMMANDS.md` and tooled at `infra/scripts/video-to-mp4.sh`). Together they close the codec gap created by DaVinci Resolve Free on Linux.
- Long-term escape hatch if marketing video volume grows: DaVinci Resolve Studio ($295 one-time perpetual) unlocks H.264/H.265 encoding directly in Deliver tab, which would eliminate the need for the `video-to-mp4` wrapper. Worth revisiting if Ricardo finds himself running the wrapper more than ~5×/week.
- Untouched untracked file `00_META/journal/2026-05-21_strategy-meeting-transcript.md` remains uncommitted (carried over from session 10/11 — pre-existing, not authored by this session; deliberate continuity with session 11's CHECKPOINT note).
- No architecture changes, no ADRs, no critical-path movement. Trixx meeting (2026-05-25) materials intact.
