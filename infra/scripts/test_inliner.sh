#!/usr/bin/env bash
# Test: inline_includes.py replaces {{include: path}} markers correctly,
#       and --check detects drift.
set -uo pipefail

INLINER="/srv/Nexostrat/infra/scripts/inline_includes.py"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

# Make a fixture: an include source + a template that includes it
echo "INCLUDED-CONTENT" > "$TMPDIR/snippet.md"
cat > "$TMPDIR/template.tmpl" <<'EOF'
Before
{{include: snippet.md}}
After
EOF

# Generate
python3 "$INLINER" --template "$TMPDIR/template.tmpl" --output "$TMPDIR/out.md"
[[ -f "$TMPDIR/out.md" ]] || { echo "FAIL — output file not created"; exit 1; }

# Verify content
if grep -q '^INCLUDED-CONTENT$' "$TMPDIR/out.md"; then
  echo "PASS — content inlined"
else
  echo "FAIL — content not inlined; got:"
  cat "$TMPDIR/out.md"
  exit 1
fi

if grep -q '{{include:' "$TMPDIR/out.md"; then
  echo "FAIL — marker still present"
  exit 1
else
  echo "PASS — marker consumed"
fi

# --check should report no drift
if python3 "$INLINER" --template "$TMPDIR/template.tmpl" --check "$TMPDIR/out.md"; then
  echo "PASS — --check no drift"
else
  echo "FAIL — --check unexpectedly reported drift"
  exit 1
fi

# Mutate the output, expect --check to flag drift
echo "DRIFT" >> "$TMPDIR/out.md"
if python3 "$INLINER" --template "$TMPDIR/template.tmpl" --check "$TMPDIR/out.md"; then
  echo "FAIL — --check missed drift"
  exit 1
else
  echo "PASS — --check detected drift"
fi

# Nested include: the inliner iterates to a fixed point. snippet-outer includes
# snippet-inner, and template includes snippet-outer. Both levels must expand.
echo "INNER" > "$TMPDIR/snippet-inner.md"
cat > "$TMPDIR/snippet-outer.md" <<'EOF'
OUTER-PRE
{{include: snippet-inner.md}}
OUTER-POST
EOF
cat > "$TMPDIR/template-nested.tmpl" <<'EOF'
TOP
{{include: snippet-outer.md}}
BOTTOM
EOF
python3 "$INLINER" --template "$TMPDIR/template-nested.tmpl" --output "$TMPDIR/nested-out.md"
if grep -q '^INNER$' "$TMPDIR/nested-out.md" && ! grep -q '{{include:' "$TMPDIR/nested-out.md"; then
  echo "PASS — nested include fully expanded"
else
  echo "FAIL — nested include not expanded:"
  cat "$TMPDIR/nested-out.md"
  exit 1
fi
