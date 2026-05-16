#!/usr/bin/env bash
# Test: run-with-secrets.sh creates plaintext at /dev/shm DURING execution,
#       and removes it AFTER exit (positive + negative control for C1).
#
# This test is INTERACTIVE — the wrapper's inner `age -d` reads the age-key
# passphrase from /dev/tty. Enter Ricardo's (or JP's) passphrase when prompted.
#
# Per Finding 2 of the 2026-05-14 re-audit: this replaces an earlier version
# that backgrounded the wrapper, never created the plaintext (wrapper was
# blocked on passphrase prompt), then false-PASSed by observing absence of a
# file that was never written. The new design polls for the file's appearance
# (positive control), then checks the specific path is gone after kill
# (negative control). It also avoids blasting concurrent legitimate sessions
# (no global `rm -f /dev/shm/nexostrat-secrets-*`).

set -uo pipefail
WRAPPER="/srv/Nexostrat/infra/scripts/run-with-secrets.sh"
SENTINEL_CMD='sleep 20'   # long enough to observe + kill mid-execution
POLL_DEADLINE_SECS=30     # generous: user types passphrase, age decrypts, wrapper writes

if [[ ! -x "$WRAPPER" ]]; then
  echo "FAIL — wrapper script not found or not executable at $WRAPPER"
  exit 1
fi

echo "================================================================"
echo "  C1 Leak Test (interactive — type your age passphrase when asked)"
echo "================================================================"
echo "  Backgrounded wrapper runs '$SENTINEL_CMD'. Polling /dev/shm for"
echo "  up to ${POLL_DEADLINE_SECS}s to see the plaintext appear (positive"
echo "  control). Then kills the wrapper and verifies cleanup (negative"
echo "  control)."
echo

# Snapshot existing /dev/shm/nexostrat-secrets-* files so concurrent sessions
# are preserved. We compute set-difference to identify OUR file.
BEFORE=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | sort -u || true)

"$WRAPPER" sh -c "$SENTINEL_CMD" &
WRAPPER_PID=$!

# Poll for a new file to appear (means wrapper got past decrypt+write).
echo "--- waiting for plaintext to appear at /dev/shm ---"
FOUND=""
DEADLINE=$((SECONDS + POLL_DEADLINE_SECS))
while (( SECONDS < DEADLINE )); do
  if ! kill -0 "$WRAPPER_PID" 2>/dev/null; then
    echo "FAIL — wrapper exited before creating plaintext (decrypt failure?)"
    wait "$WRAPPER_PID" 2>/dev/null
    exit 1
  fi
  CURRENT=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | sort -u || true)
  NEW=$(comm -23 <(echo "$CURRENT") <(echo "$BEFORE") 2>/dev/null | head -1)
  if [[ -n "$NEW" ]]; then FOUND="$NEW"; break; fi
  sleep 1
done

if [[ -z "$FOUND" ]]; then
  echo "FAIL — no plaintext file appeared at /dev/shm within ${POLL_DEADLINE_SECS}s"
  echo "  (user may not have entered passphrase, or wrapper is broken)"
  kill "$WRAPPER_PID" 2>/dev/null
  wait "$WRAPPER_PID" 2>/dev/null
  exit 1
fi
echo "PASS — wrapper created $FOUND during execution (positive control)"

# Now kill the wrapper and verify the SPECIFIC file we observed is removed.
kill "$WRAPPER_PID" 2>/dev/null
wait "$WRAPPER_PID" 2>/dev/null
sleep 1

if [[ -e "$FOUND" ]]; then
  echo "FAIL — $FOUND still exists after wrapper killed; C1 cleanup did NOT fire"
  ls -la "$FOUND"
  exit 1
fi
echo "PASS — $FOUND removed after wrapper exit (negative control — C1 cleanup verified)"

# Optional sanity: any other newly-created leftovers we didn't track?
AFTER=$(ls /dev/shm/nexostrat-secrets-* 2>/dev/null | sort -u || true)
EXTRA=$(comm -23 <(echo "$AFTER") <(echo "$BEFORE") 2>/dev/null || true)
if [[ -n "$EXTRA" ]]; then
  echo "WARN — unexpected leftover files (concurrent session, or test ran twice?):"
  printf '  %s\n' $EXTRA
fi

echo
echo "All assertions passed (C1 leak test)."
