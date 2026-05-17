#!/usr/bin/env bash
# checkpoint-mtime-check.sh — Nexostrat (R4)
#
# Warn if any CHECKPOINT.md in the repo was modified within the last
# THRESHOLD_MIN minutes. Catches concurrent-session edits.
#
# Usage:
#   checkpoint-mtime-check.sh [THRESHOLD_MIN]
# Default threshold: 10 minutes.
# Note (MVP scope): in normal single-operator flow the gap between session-end
# (push CHECKPOINT.md) and the next session-start (read CHECKPOINT.md) is well
# under 10 minutes, which means this check will warn often when the system is
# behaving correctly. That noise is the cost of an mtime-only MVP. Plan 03's
# events.jsonl router supersedes this with a proper session-lock; until then
# operators can tune `THRESHOLD_MIN` per host if the warnings are too chatty.
#
# Exit codes:
#   0 — no recent edits (or only by this session, which we can't detect; documented limitation)
#   1 — at least one CHECKPOINT.md modified within the threshold (warning printed)

set -uo pipefail

REPO="/srv/Nexostrat"
THRESHOLD_MIN="${1:-10}"

if ! [[ "$THRESHOLD_MIN" =~ ^[0-9]+$ ]]; then
  echo "ERROR: THRESHOLD_MIN must be a positive integer; got '${THRESHOLD_MIN}'" >&2
  exit 2
fi

# find CHECKPOINT.md files modified within the last THRESHOLD_MIN minutes
mapfile -t recent < <(
  find "$REPO" \
    -path '*/.git' -prune -o \
    -name 'CHECKPOINT.md' -type f -mmin "-${THRESHOLD_MIN}" -print 2>/dev/null
)

if [[ ${#recent[@]} -eq 0 ]]; then
  exit 0
fi

{
  echo
  echo "========================================================================"
  echo "WARNING — CHECKPOINT.md(s) modified within the last ${THRESHOLD_MIN} min:"
  for f in "${recent[@]}"; do
    ts=$(stat -c '%y' "$f" | cut -d. -f1)
    rel="${f#$REPO/}"
    echo "  $rel  (mtime $ts)"
  done
  echo
  echo "If ANOTHER Claude Code session is open against this repo, close it"
  echo "before continuing — concurrent CHECKPOINT.md edits cause confusion."
  echo "If this is intentional (e.g., you just finished writing CHECKPOINT.md"
  echo "for THIS session), this warning is safe to ignore."
  echo "========================================================================"
  echo
} >&2
exit 1
