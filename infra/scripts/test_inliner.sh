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

# Path-escape test: absolute include outside the allowed root is rejected.
# /etc/hostname is reliable on Linux — exists, readable, definitely outside /tmp/.
# Under the new boundary (base.parent = TMPDIR), the old ../escape.md fixture would
# resolve to /tmp/escape.md which IS under TMPDIR's parent, so it no longer escapes.
# An absolute path to /etc/hostname always escapes any tmpdir-rooted boundary.
cat > "$TMPDIR/template-escape.tmpl" <<'EOF'
{{include: /etc/hostname}}
EOF
set +u
python3 "$INLINER" --template "$TMPDIR/template-escape.tmpl" --output "$TMPDIR/escape-out.md" > "$TMPDIR/escape-stdout.txt" 2>&1
ec=$?
set -u
if [[ $ec -ne 0 ]] && grep -q "escapes allowed root" "$TMPDIR/escape-stdout.txt"; then
  echo "PASS — path-escape rejected with correct error"
else
  echo "FAIL — path-escape: ec=$ec stdout=$(cat "$TMPDIR/escape-stdout.txt")"
  exit 1
fi

# Multi-newline test: a snippet ending with two trailing newlines ("BODY\n\n") must
# have exactly ONE trailing newline stripped — leaving "BODY\n" inlined, not "BODY"
# (which rstrip('\n') would have produced).
# The template is a single marker line, so the rendered output is "BODY\n" exactly
# (the inlined "BODY\n" — one newline survived — occupies the marker's position).
# Verification: output contains BODY, and the file ends with a newline byte (i.e.,
# `wc -c` equals `wc -m` of "BODY\n" = 5 bytes).
printf 'BODY\n\n' > "$TMPDIR/snippet-multinl.md"
cat > "$TMPDIR/template-multinl.tmpl" <<'EOF'
{{include: snippet-multinl.md}}
EOF
python3 "$INLINER" --template "$TMPDIR/template-multinl.tmpl" --output "$TMPDIR/multinl-out.md"
multinl_bytes=$(wc -c < "$TMPDIR/multinl-out.md")
if grep -q '^BODY$' "$TMPDIR/multinl-out.md" && [[ $multinl_bytes -eq 5 ]]; then
  echo "PASS — multi-newline snippet preserves one trailing newline"
else
  echo "FAIL — multi-newline snippet output wrong (bytes=$multinl_bytes, expected 5):"
  cat -A "$TMPDIR/multinl-out.md"
  exit 1
fi
