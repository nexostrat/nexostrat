#!/usr/bin/env bash
# video-to-mp4.sh — transcode any DaVinci/ffmpeg-readable video to a universally
# playable MP4 (H.264 High + AAC LC, yuv420p, faststart). Produced because
# DaVinci Resolve free on Linux can only export APV+FLAC inside MP4, which
# Celluloid/mpv refuse to play.
#
# Usage:
#   video-to-mp4.sh <input> [output]
#
# If output is omitted, writes <input-basename>.mp4 next to the input.
# Refuses to overwrite unless -f / --force is passed.
#
# Defaults tuned for 1080p marketing video: CRF 18 (visually lossless), preset
# slow, AAC 192k stereo. Override with env vars: CRF, PRESET, AUDIO_BITRATE.

set -euo pipefail

force=0
args=()
for arg in "$@"; do
  case "$arg" in
    -f|--force) force=1 ;;
    -h|--help)
      sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) args+=("$arg") ;;
  esac
done

if [[ ${#args[@]} -lt 1 || ${#args[@]} -gt 2 ]]; then
  echo "usage: $(basename "$0") <input> [output] [-f]" >&2
  exit 64
fi

input="${args[0]}"
if [[ ! -f "$input" ]]; then
  echo "error: input not found: $input" >&2
  exit 66
fi

if [[ ${#args[@]} -eq 2 ]]; then
  output="${args[1]}"
else
  dir="$(dirname -- "$input")"
  base="$(basename -- "$input")"
  stem="${base%.*}"
  output="$dir/$stem.mp4"
fi

if [[ -e "$output" && $force -eq 0 ]]; then
  echo "error: output exists: $output (pass -f to overwrite)" >&2
  exit 73
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "error: ffmpeg not installed (sudo apt install ffmpeg)" >&2
  exit 69
fi

crf="${CRF:-18}"
preset="${PRESET:-slow}"
abr="${AUDIO_BITRATE:-192k}"

echo "input:  $input"
echo "output: $output"
echo "recipe: libx264 preset=$preset crf=$crf  |  aac $abr  |  yuv420p +faststart"
echo

ffmpeg -hide_banner -y \
  -i "$input" \
  -c:v libx264 -preset "$preset" -crf "$crf" -pix_fmt yuv420p \
  -c:a aac -b:a "$abr" \
  -movflags +faststart \
  "$output"

in_size=$(stat -c%s "$input")
out_size=$(stat -c%s "$output")
printf '\ndone. %s  →  %s  (%.1f MB → %.1f MB)\n' \
  "$(basename -- "$input")" "$(basename -- "$output")" \
  "$(echo "$in_size/1048576" | bc -l)" \
  "$(echo "$out_size/1048576" | bc -l)"
