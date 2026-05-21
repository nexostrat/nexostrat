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

# Fetch into a per-mirror staging ref instead of refs/remotes/origin/main.
# Two reasons:
#   (1) Off-HP pushes leave this working clone's remote-tracking refs stale,
#       so naively pushing local 'main' would send the old hash and report
#       "Everything up-to-date" (silent no-op).
#   (2) Both mirror services fire on the same .path watcher event and run in
#       parallel. If they both fetched into refs/remotes/origin/main, they'd
#       race on the ref lock ("cannot lock ref ... is at X but expected Y")
#       and one would fail. A per-remote staging ref isolates them.
# This also avoids touching the working tree — no reset, no risk of
# clobbering uncommitted edits on HP.
STAGING_REF="refs/mirror-stage/$REMOTE"
if ! git fetch origin "refs/heads/main:$STAGING_REF" 2>&1; then
  echo "[$TS] mirror-push: fetch from origin failed" >&2
  exit 1
fi

echo "[$TS] mirror-push: pushing $STAGING_REF → $REMOTE"

# The push uses the SSH key in ~/.ssh/config (via the alias) — no PAT needed
# for SSH-based remotes. The PATs in secrets.env.age are reserved for HTTPS
# fallback (TBD; Stage 1 ships SSH-only).
if git push "$REMOTE" "$STAGING_REF:refs/heads/main" 2>&1; then
  echo "[$TS] mirror-push: $REMOTE OK"
  exit 0
else
  echo "[$TS] mirror-push: $REMOTE FAILED" >&2
  exit 1
fi
