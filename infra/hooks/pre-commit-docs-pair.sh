#!/usr/bin/env bash
# pre-commit-docs-pair.sh — Nexostrat (BASIC version; Plan 02 ships the full hook)
#
# In tier-1 folders (00_PARTNERSHIP/, 00_GOVERNANCE/, root README.md), if X.md
# is modified, X-explicado.md must also be staged (or vice versa). Escape
# hatch: 'docs-skip-pair' in the commit message body (handled by Plan 02).
#
# This basic version covers only the most rigid case (00_PARTNERSHIP/ +
# 00_GOVERNANCE/ + root README.md). docs/ tier-1 enforcement comes in Plan 02
# alongside the auto-generators.

set -uo pipefail

mapfile -t staged < <(git diff --cached --name-only --diff-filter=ACMR)

violations=0

for f in "${staged[@]}"; do
  case "$f" in
    00_PARTNERSHIP/*.md|00_GOVERNANCE/*.md|README.md) ;;
    *) continue ;;
  esac

  # Skip already -explicado partners and the raised_hand_log
  case "$f" in
    *-explicado.md|*/raised_hand_log.md|*/CHANGELOG.md|*/DECISIONS.md) continue ;;
  esac

  partner="${f%.md}-explicado.md"

  # If partner exists in the working tree but is NOT staged → block
  if [[ -f "$partner" ]] && ! printf '%s\n' "${staged[@]}" | grep -qFx "$partner"; then
    echo "BLOCKED: $f modified but its partner $partner is not staged"
    violations=$((violations+1))
  fi
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "Tier-1 docs require the -explicado partner to be staged in the same commit."
  echo "Either stage the partner, or use 'git commit --no-verify' if intentionally"
  echo "skipping the pair. (A 'docs-skip-pair' commit-body escape-hatch is planned"
  echo "for Plan 02; pre-commit hooks can't inspect the commit message yet, so for"
  echo "now --no-verify is the documented escape.)"
  echo "Hook: infra/hooks/pre-commit-docs-pair.sh"
  exit 1
fi
exit 0
