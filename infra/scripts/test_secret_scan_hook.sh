#!/usr/bin/env bash
# Test: pre-commit-secret-scan.sh blocks a planted secret in staged content.
set -u
HOOK="/srv/Nexostrat/infra/hooks/pre-commit-secret-scan.sh"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Create a fake staged file with a planted secret.
# The secret string is assembled at runtime so this script itself does not
# contain a literal match that would trip the pre-commit hook on commit.
PLANTED="$TMPDIR/planted.txt"
SECRET_PREFIX="sk-ant-"
SECRET_SUFFIX="test1234567890abcdef"
printf 'something something\n%s%s\nfoo bar\n' "$SECRET_PREFIX" "$SECRET_SUFFIX" > "$PLANTED"

# Hook reads file paths from stdin (one per line) — simulate staged file list
if echo "$PLANTED" | bash "$HOOK" --files-from-stdin; then
  echo "FAIL — hook did NOT block the planted secret"; exit 1
else
  echo "PASS — hook blocked the planted secret"
fi

# Negative test: a clean file should pass
CLEAN="$TMPDIR/clean.txt"
echo "this is fine" > "$CLEAN"
if echo "$CLEAN" | bash "$HOOK" --files-from-stdin; then
  echo "PASS — hook permitted a clean file"
else
  echo "FAIL — hook rejected a clean file"; exit 1
fi
