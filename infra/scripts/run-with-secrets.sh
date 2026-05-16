#!/usr/bin/env bash
# run-with-secrets.sh — Nexostrat
#
# Decrypts secrets.env.age into /dev/shm, sources it, runs the wrapped
# command, captures its exit code, then EXPLICITLY shreds plaintext and
# exits with the wrapped command's code.
#
# Per CRITICAL 1 fix (audit 2026-05-14): does NOT `exec "$@"` — that would
# leak the trap. Instead runs `"$@"` as a child, captures rc, runs cleanup
# unconditionally via trap, exits with rc.
#
# Plaintext lives at /dev/shm/nexostrat-secrets-<pid> for the lifetime of
# the wrapped command and is shred-removed on every exit path (success,
# error, signal).
#
# Usage:
#   infra/scripts/run-with-secrets.sh <command> [args...]
#
# Exit codes:
#   = exit code of the wrapped command, OR
#   1 if decrypt failed.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ENC="$REPO_ROOT/secrets.env.age"
PRIV_KEY_AGE="$HOME/.config/age/nexostrat.key.age"
PT="/dev/shm/nexostrat-secrets-$$"

cleanup() {
  if [[ -f "$PT" ]]; then
    shred -u "$PT" 2>/dev/null || rm -f "$PT"
  fi
}
trap cleanup EXIT INT TERM HUP

if [[ ! -f "$ENC" ]]; then
  echo "ERROR: $ENC not found" >&2
  exit 1
fi
if [[ ! -f "$PRIV_KEY_AGE" ]]; then
  echo "ERROR: $PRIV_KEY_AGE not found (set up Ricardo or JP age key first)" >&2
  exit 1
fi

# Decrypt secrets to /dev/shm
# (the inner age -d prompts for the private-key passphrase on /dev/tty;
#  age's diagnostic messages go to stderr — capture them rather than silence,
#  per Finding 7 of the 2026-05-14 re-audit: first-time users need to
#  distinguish wrong-passphrase vs recipient-mismatch vs identity-file-format
#  failures.)
AGE_ERR=$(mktemp)
if ! age -d -i <(age -d "$PRIV_KEY_AGE") "$ENC" > "$PT" 2>"$AGE_ERR"; then
  echo "ERROR: failed to decrypt $ENC" >&2
  echo "  hint: wrong passphrase, recipient mismatch, or identity-file format issue" >&2
  if [[ -s "$AGE_ERR" ]]; then
    echo "  age stderr:" >&2
    sed 's/^/    /' "$AGE_ERR" >&2
  fi
  rm -f "$AGE_ERR"
  exit 1
fi
rm -f "$AGE_ERR"
chmod 600 "$PT"

# Source the env into the current shell
set -a  # auto-export every assigned var
# shellcheck disable=SC1090
source "$PT"
set +a

# Run the wrapped command — NOT exec; we want the trap to fire after.
"$@"
RC=$?

# trap will run cleanup; explicit exit propagates the wrapped rc
exit "$RC"
