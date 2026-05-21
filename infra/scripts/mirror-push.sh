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

TS=$(date -Iseconds)

# Refresh origin/main from the bare repo before pushing. Without this, pushes
# that landed via Gitea from other machines leave THIS working clone's
# remote-tracking refs stale, so `git push <mirror> main` sends the old hash
# and reports "Everything up-to-date" (silent no-op). Pushing origin/main
# directly avoids touching the working tree — no reset, no risk of clobbering
# uncommitted edits on HP.
if ! git fetch origin main 2>&1; then
  echo "[$TS] mirror-push: fetch from origin failed" >&2
  exit 1
fi

echo "[$TS] mirror-push: pushing origin/main → $REMOTE"

# The push uses the SSH key in ~/.ssh/config (via the alias) — no PAT needed
# for SSH-based remotes. The PATs in secrets.env.age are reserved for HTTPS
# fallback (TBD; Stage 1 ships SSH-only).
if git push "$REMOTE" origin/main:refs/heads/main 2>&1; then
  echo "[$TS] mirror-push: $REMOTE OK"
  exit 0
else
  echo "[$TS] mirror-push: $REMOTE FAILED" >&2
  exit 1
fi
