#!/usr/bin/env bash
# mirror-push.sh — Nexostrat
#
# Push the canonical local clone of /srv/Nexostrat/ to a named git remote.
# Called by nexostrat-mirror-<remote>.service (systemd).
#
# Usage: mirror-push.sh <remote>
#
# Exit codes:
#   0  push succeeded (or nothing to push)
#   1  push failed
#   2  remote not found / invalid argument

set -uo pipefail

REPO="/srv/Nexostrat"
REMOTE="${1:?usage: mirror-push.sh <remote>}"

cd "$REPO"

# Sanity: remote exists
if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "ERROR: remote '$REMOTE' not configured for $REPO" >&2
  exit 2
fi

# Use a deterministic timestamped log line so journalctl is greppable
TS=$(date -Iseconds)
echo "[$TS] mirror-push: pushing main → $REMOTE"

# The push uses the SSH key in ~/.ssh/config (via the alias) — no PAT needed
# for SSH-based remotes. The PATs in secrets.env.age are reserved for HTTPS
# fallback (TBD; Stage 1 ships SSH-only).
if git push "$REMOTE" main 2>&1; then
  echo "[$TS] mirror-push: $REMOTE OK"
  exit 0
else
  echo "[$TS] mirror-push: $REMOTE FAILED" >&2
  exit 1
fi
