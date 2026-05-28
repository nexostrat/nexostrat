#!/usr/bin/env bash
# Regression test — Skill 05 markdown parser tolerates blank line between
# `### TABLA_OPORTUNIDADES` heading and the table start.
#
# Bug: 2026-05-26 — original parser interpreted the blank line as table
# terminator, producing reports with 0 opportunities and missing all
# downstream charts/matrix. See memo:
#   skills/00_META/inbox/archive/2026-05-26_2310_client-owner_skill05-parser-bug.md
#
# Usage: bash test_parser_regression.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GENERATOR="$SCRIPT_DIR/../scripts/generate_docx.py"
FIXTURE="$SCRIPT_DIR/fixtures/blank_line_before_table.md"
OUT_DOCX="$(mktemp -t skill05_regression_XXXXXX.docx)"

trap 'rm -f "$OUT_DOCX"' EXIT

echo "Running generator against fixture with blank line before TABLA_OPORTUNIDADES..."
OUTPUT="$(python3 "$GENERATOR" "$FIXTURE" "$OUT_DOCX" 2>&1)"

# Expect to find 3 opportunities (the fixture has 3 rows).
if echo "$OUTPUT" | grep -qE "Oportunidades encontradas:\s*3"; then
    echo "PASS — parser detected 3 opportunities despite blank line before table"
    exit 0
else
    echo "FAIL — parser did not detect the expected 3 opportunities"
    echo "--- generator output ---"
    echo "$OUTPUT"
    exit 1
fi
