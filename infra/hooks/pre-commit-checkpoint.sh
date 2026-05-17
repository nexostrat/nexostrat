#!/usr/bin/env bash
# pre-commit-checkpoint.sh — Nexostrat
#
# Per ADR-031: empty CHECKPOINT.md commits refused unless they contain the
# token CHECKPOINT_NO_ACTIVE_WORK.
#
# "Empty" = file size < 100 bytes OR no body content beyond a heading.

set -uo pipefail

mapfile -t staged < <(git diff --cached --name-only --diff-filter=ACMR | grep -E '(^|/)CHECKPOINT\.md$' || true)
[[ ${#staged[@]} -eq 0 ]] && exit 0

violations=0
for f in "${staged[@]}"; do
  [[ -f "$f" ]] || continue
  if grep -q 'CHECKPOINT_NO_ACTIVE_WORK' "$f"; then
    continue  # explicit no-active-work marker
  fi
  # File must have substantive content (≥ 200 bytes is an OK proxy)
  bytes=$(wc -c < "$f")
  if [[ "$bytes" -lt 200 ]]; then
    echo "BLOCKED: $f is too short (${bytes} bytes) and lacks CHECKPOINT_NO_ACTIVE_WORK token"
    violations=$((violations+1))
  fi
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "Per ADR-031: CHECKPOINT.md must either have substantive content or"
  echo "explicitly contain the literal token: CHECKPOINT_NO_ACTIVE_WORK"
  echo "Hook: infra/hooks/pre-commit-checkpoint.sh"
  exit 1
fi
exit 0
