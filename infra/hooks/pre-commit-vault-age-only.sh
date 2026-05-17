#!/usr/bin/env bash
# pre-commit-vault-age-only.sh — Nexostrat
#
# Refuse any staged file under vault/ that isn't:
#   - a .age file
#   - sensitive_index.md or README.md
#   - a .gitkeep
#
# This is belt-and-suspenders with .gitignore which already excludes
# plaintext under vault/ (matches *.pdf, *.docx, *.txt, *.md but
# !sensitive_index.md / !README.md / !.gitkeep).

set -uo pipefail

violations=0
mapfile -t staged < <(git diff --cached --name-only --diff-filter=ACMR)

for f in "${staged[@]}"; do
  [[ "$f" =~ ^vault/ ]] || continue
  case "$f" in
    *.age) continue ;;
    vault/*/sensitive_index.md|vault/sensitive_index.md) continue ;;
    vault/*/README.md|vault/README.md) continue ;;
    */.gitkeep) continue ;;
    *)
      echo "BLOCKED: $f staged under vault/ but is not .age/index/README/.gitkeep"
      violations=$((violations+1))
      ;;
  esac
done

if [[ $violations -gt 0 ]]; then
  echo
  echo "Vault accepts only .age ciphertext (+ sensitive_index/README/.gitkeep)."
  echo "Encrypt the file first:"
  echo "  age -R infra/age-recipients.txt -o vault/<path>/file.age <plaintext>"
  echo "Hook: infra/hooks/pre-commit-vault-age-only.sh"
  exit 1
fi
exit 0
