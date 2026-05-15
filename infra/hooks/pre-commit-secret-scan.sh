#!/usr/bin/env bash
# pre-commit-secret-scan.sh — Nexostrat
#
# Blocks any commit whose newly-staged content contains a known secret prefix.
# Run modes:
#   1. Default: invoked by git as the pre-commit hook. Reads `git diff --cached --name-only`.
#   2. --files-from-stdin: read newline-delimited paths from stdin (used by the test harness).
#
# Patterns covered (extend as needed):
#   sk-ant-XXX     Anthropic API key
#   sk-XXX         OpenAI/legacy API key
#   AKIA           AWS access key
#   ghp_/gho_/ghs_/ghu_/glpat-  GitHub/GitLab personal-access tokens
#   xoxb-/xoxp-    Slack tokens
#   eyJ            JWT (heuristic — three base64 segments separated by .)
#
# Exit 0 = clean. Exit 1 = secret found (or hook error).

set -uo pipefail

# Pattern set — pipe-separated for a single grep -E
PATTERNS='(sk-ant-[A-Za-z0-9_-]{20,})|(\bsk-[A-Za-z0-9]{20,})|(\bAKIA[0-9A-Z]{16}\b)|(\bghp_[A-Za-z0-9]{30,})|(\bgho_[A-Za-z0-9]{30,})|(\bghs_[A-Za-z0-9]{30,})|(\bghu_[A-Za-z0-9]{30,})|(\bglpat-[A-Za-z0-9_-]{20,})|(\bxox[baprs]-[A-Za-z0-9-]{10,})|(\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)'

# Decide source of paths AND which content surface to scan.
#   git-hook mode (default):   scan the STAGED BLOB via `git show :<path>` —
#                              this is what the commit actually contains, not
#                              what's on disk (per Finding 3 of the 2026-05-14
#                              re-audit: stage-then-edit-clean would bypass an
#                              on-disk scanner).
#   --files-from-stdin mode:   scan on-disk content directly — used by the
#                              unit-test harness where files aren't in any git
#                              index. (Integration test in Task 3 Step 6b
#                              exercises the staged-blob path via a real git
#                              workflow.)
MODE="git-hook"
if [[ "${1:-}" == "--files-from-stdin" ]]; then
  MODE="stdin"
  mapfile -t FILES < <(cat)
else
  mapfile -t FILES < <(git diff --cached --name-only --diff-filter=ACMR)
fi

[[ ${#FILES[@]} -eq 0 ]] && exit 0

scan_content() {
  # stdin: content to scan; $1: label (file path) for grep output
  grep -EHn "$PATTERNS" --label="$1" - 2>/dev/null
}

violations=0
for f in "${FILES[@]}"; do
  # Skip anything that matches our own .gitignore secret patterns — defensive
  case "$f" in
    *.age) continue ;;
    *secrets*) ;;  # still scan — explicit
  esac
  if [[ "$MODE" == "git-hook" ]]; then
    # Read the staged blob. Skip silently if blob unavailable (e.g. deleted path).
    if blob=$(git show ":$f" 2>/dev/null); then
      if printf '%s' "$blob" | scan_content "$f"; then
        violations=$((violations+1))
      fi
    fi
  else
    # stdin mode — scan disk file directly
    [[ -f "$f" ]] || continue
    if grep -EHn "$PATTERNS" "$f" 2>/dev/null; then
      violations=$((violations+1))
    fi
  fi
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "============================================================"
  echo "  BLOCKED: $violations file(s) contain secret-prefix matches."
  echo "  If this is a false positive, rewrite the value or unstage."
  echo "  Hook: infra/hooks/pre-commit-secret-scan.sh"
  echo "============================================================"
  exit 1
fi

exit 0
