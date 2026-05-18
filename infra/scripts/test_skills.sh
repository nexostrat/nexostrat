#!/usr/bin/env bash
# test_skills.sh — Validates the 4 mature Nexostrat skills (01, 02, 03, 06).
#
# Checks:
#   [1/8] YAML frontmatter parses cleanly + has name + description
#   [2/8] Frontmatter `name:` matches the .claude/skills/ symlink target
#   [3/8] Every Python script in skills/<NN>_<name>/scripts/ compiles
#   [4/8] Every `skills/.*\.py` path referenced in SKILL.md exists on disk
#   [5/8] Every `.claude/skills/<name>/SKILL.md` symlink resolves
#   [6/8] No stale `/tmp/<skill>/` or `/var/folders/` paths in skills/
#   [7/8] generate_docx.py smoke test (renders a minimal MD → DOCX) per skill
#   [8/8] extract_financials.py smoke test (runs not-found path) for skills 01 + 03
#
# Layer-aware SKIP: checks gated on python-docx, pandas, openpyxl SKIP-not-FAIL
# when the dep is missing, matching infra/scripts/smoke-test.sh's R2 convention.
#
# Exit 0 on full pass (PASS or SKIP across the board); exit 1 if any FAIL.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

# ── Skill registry (NN-folder, frontmatter-name) ─────────────────────────────
SKILLS=(
  "01_company_analyst:company-analyst"
  "02_industry_analyst:industry-analyst"
  "03_competitor_analyst:competitor-analyst"
  "06_discovery_meeting:discovery-meeting"
)

PASS=0
FAIL=0
SKIP=0

# ── ANSI colors (only if stdout is a TTY) ────────────────────────────────────
if [ -t 1 ]; then
  G='\033[0;32m'; R='\033[0;31m'; Y='\033[0;33m'; B='\033[0;34m'; N='\033[0m'
else
  G=''; R=''; Y=''; B=''; N=''
fi

pass() { echo -e "  ${G}PASS${N}  $*"; PASS=$((PASS+1)); }
fail() { echo -e "  ${R}FAIL${N}  $*"; FAIL=$((FAIL+1)); }
skip() { echo -e "  ${Y}SKIP${N}  $*  (reason: $2)"; SKIP=$((SKIP+1)); }
section() { echo -e "\n${B}── $* ──${N}"; }

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 1: YAML frontmatter parses cleanly + has name + description
# ─────────────────────────────────────────────────────────────────────────────
section "[1/8] YAML frontmatter — name + description present"

if ! python3 -c "import yaml" 2>/dev/null; then
  skip "All 4 skills" "PyYAML not installed"
else
  for entry in "${SKILLS[@]}"; do
    folder="${entry%%:*}"
    expected_name="${entry##*:}"
    skill_md="skills/${folder}/SKILL.md"

    if [ ! -f "$skill_md" ]; then
      fail "${folder}: SKILL.md not found"
      continue
    fi

    result=$(python3 - "$skill_md" "$expected_name" <<'PY'
import sys, yaml, pathlib
skill_path = pathlib.Path(sys.argv[1])
expected_name = sys.argv[2]
text = skill_path.read_text(encoding="utf-8")
if not text.startswith("---\n"):
    print("NO_FRONTMATTER"); sys.exit(0)
parts = text.split("---", 2)
if len(parts) < 3:
    print("MALFORMED_FRONTMATTER"); sys.exit(0)
try:
    fm = yaml.safe_load(parts[1])
except yaml.YAMLError as e:
    print(f"YAML_PARSE_ERROR:{e}"); sys.exit(0)
if not isinstance(fm, dict):
    print("FRONTMATTER_NOT_DICT"); sys.exit(0)
name = fm.get("name", "")
desc = fm.get("description", "")
if not name:
    print("MISSING_NAME"); sys.exit(0)
if not desc:
    print("MISSING_DESCRIPTION"); sys.exit(0)
if name != expected_name:
    print(f"NAME_MISMATCH:{name}"); sys.exit(0)
print("OK")
PY
)
    case "$result" in
      OK) pass "${folder}: name='${expected_name}' + description present" ;;
      NAME_MISMATCH:*) fail "${folder}: frontmatter name='${result#NAME_MISMATCH:}' but expected '${expected_name}'" ;;
      *) fail "${folder}: ${result}" ;;
    esac
  done
fi

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 2: Symlink resolution + content match
# ─────────────────────────────────────────────────────────────────────────────
section "[2/8] .claude/skills/<name>/ symlinks resolve to the right skill"

for entry in "${SKILLS[@]}"; do
  folder="${entry%%:*}"
  name="${entry##*:}"
  symlink=".claude/skills/${name}"

  if [ ! -L "$symlink" ]; then
    fail "${name}: .claude/skills/${name} is not a symlink"
    continue
  fi

  target=$(readlink "$symlink")
  expected_target="../../skills/${folder}"
  if [ "$target" != "$expected_target" ]; then
    fail "${name}: symlink target='${target}' but expected '${expected_target}'"
    continue
  fi

  if [ ! -f "${symlink}/SKILL.md" ]; then
    fail "${name}: SKILL.md not found via symlink"
    continue
  fi

  pass "${name} → ${expected_target} (SKILL.md resolves)"
done

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 3: Python scripts compile (py_compile)
# ─────────────────────────────────────────────────────────────────────────────
section "[3/8] Every Python script under skills/<NN>/scripts/ compiles"

scripts_found=0
while IFS= read -r -d '' script; do
  scripts_found=$((scripts_found+1))
  if python3 -m py_compile "$script" 2>/dev/null; then
    pass "$(echo "$script" | sed 's|^skills/||')"
  else
    err=$(python3 -m py_compile "$script" 2>&1 | tr '\n' ' ' | head -c 200)
    fail "$(echo "$script" | sed 's|^skills/||'): ${err}"
  fi
done < <(find skills -path '*/scripts/*.py' -print0)

if [ "$scripts_found" -eq 0 ]; then
  fail "No Python scripts found under skills/*/scripts/ — expected at least 4"
fi

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 4: Every `skills/.*\.py` referenced in SKILL.md exists on disk
# ─────────────────────────────────────────────────────────────────────────────
section "[4/8] Script paths referenced in SKILL.md resolve on disk"

for entry in "${SKILLS[@]}"; do
  folder="${entry%%:*}"
  skill_md="skills/${folder}/SKILL.md"

  # Extract paths matching `skills/NN_name/scripts/file.py` (with or without leading slash)
  refs=$(grep -oE 'skills/[0-9]+_[a-z_]+/scripts/[a-z_]+\.py' "$skill_md" | sort -u)

  if [ -z "$refs" ]; then
    # No script refs in this SKILL.md (acceptable if skill is prompt-only)
    pass "${folder}: no script refs in SKILL.md (nothing to validate)"
    continue
  fi

  all_resolve=1
  for ref in $refs; do
    if [ ! -f "$ref" ]; then
      fail "${folder}: SKILL.md refs '${ref}' but file does not exist"
      all_resolve=0
    fi
  done

  if [ "$all_resolve" -eq 1 ]; then
    n_refs=$(echo "$refs" | wc -l)
    pass "${folder}: ${n_refs} script ref(s) resolve"
  fi
done

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 5: Asset XLSX files exist where SKILL.md / scripts expect them
# ─────────────────────────────────────────────────────────────────────────────
section "[5/8] Asset XLSX files present (extract_financials.py dependency)"

for skill_with_assets in "01_company_analyst" "03_competitor_analyst"; do
  bg="skills/${skill_with_assets}/assets/supersociedades_balance_general.xlsx"
  er="skills/${skill_with_assets}/assets/supersociedades_estado_resultados.xlsx"
  if [ -f "$bg" ] && [ -f "$er" ]; then
    bg_kb=$(($(stat -c %s "$bg") / 1024))
    er_kb=$(($(stat -c %s "$er") / 1024))
    pass "${skill_with_assets}: balance_general (${bg_kb}KB) + estado_resultados (${er_kb}KB)"
  else
    [ ! -f "$bg" ] && fail "${skill_with_assets}: missing ${bg}"
    [ ! -f "$er" ] && fail "${skill_with_assets}: missing ${er}"
  fi
done

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 6: No stale /tmp/<skill>/ or /var/folders/ paths in skills/
# ─────────────────────────────────────────────────────────────────────────────
section "[6/8] No stale /tmp/<skill>/ or /var/folders/ paths in SKILL.md"

# Scope: SKILL.md only. CHANGELOG.md + README.md legitimately reference past stale
# paths when documenting fixes — excluding them prevents historical-mention false
# positives. SKILL.md is the runtime artifact; that's where stale paths bite.
stale=$(grep -rEn '/(tmp|var/folders)/[a-z-]*(-analyst|-meeting)?/scripts|/var/folders/\.\.\./skills' skills/*/SKILL.md 2>/dev/null || true)
if [ -z "$stale" ]; then
  pass "All 4 SKILL.md files free of stale extraction paths"
else
  fail "Stale paths found in SKILL.md:"
  echo "$stale" | sed 's/^/         /'
fi

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 7: generate_docx.py smoke test per skill
# ─────────────────────────────────────────────────────────────────────────────
section "[7/8] generate_docx.py smoke test (render minimal MD → DOCX)"

if ! python3 -c "import docx" 2>/dev/null; then
  skip "All 4 skills" "python-docx not installed (pip install python-docx --break-system-packages)"
else
  TMPDIR=$(mktemp -d)
  trap 'rm -rf "$TMPDIR"' EXIT

  # Minimal but representative MD that exercises h1/h2/h3, bullets, table, bold
  cat > "${TMPDIR}/sample.md" <<'EOF'
# Test Report

**Mejía, IA & CIA — Test Fixture**

## Section 1

Some paragraph text with **bold** and *italic*.

### Subsection

- Bullet 1
- Bullet 2

| Header A | Header B |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |

## Section 2

1. Numbered item
2. Another item
EOF

  for entry in "${SKILLS[@]}"; do
    folder="${entry%%:*}"
    name="${entry##*:}"
    script="skills/${folder}/scripts/generate_docx.py"
    output="${TMPDIR}/${name}.docx"

    if [ ! -f "$script" ]; then
      fail "${name}: ${script} not found"
      continue
    fi

    if python3 "$script" "${TMPDIR}/sample.md" "$output" > "${TMPDIR}/${name}.log" 2>&1; then
      if [ -f "$output" ] && [ "$(stat -c %s "$output")" -gt 1000 ]; then
        size_kb=$(($(stat -c %s "$output") / 1024))
        pass "${name}: rendered ${size_kb}KB DOCX from sample MD"
      else
        fail "${name}: script exited 0 but output missing or <1KB"
      fi
    else
      err=$(tail -3 "${TMPDIR}/${name}.log" | tr '\n' ' ' | head -c 200)
      fail "${name}: script failed: ${err}"
    fi
  done
fi

# ─────────────────────────────────────────────────────────────────────────────
# CHECK 8: extract_financials.py smoke test (not-found path)
# ─────────────────────────────────────────────────────────────────────────────
section "[8/8] extract_financials.py smoke test (not-found path)"

if ! python3 -c "import pandas, openpyxl" 2>/dev/null; then
  skip "Skills 01 + 03" "pandas + openpyxl not installed (pip install pandas openpyxl --break-system-packages)"
else
  for skill_with_extract in "01_company_analyst" "03_competitor_analyst"; do
    script="skills/${skill_with_extract}/scripts/extract_financials.py"
    # Use a deliberately impossible query so the script exits via not-found path
    output=$(python3 "$script" "ZZZ_NONEXISTENT_COMPANY_FOR_TESTING_ZZZ" 2>&1)
    if echo "$output" | grep -q "NO ENCONTRADO EN SUPERSOCIEDADES"; then
      pass "${skill_with_extract}: not-found path returned expected message"
    else
      err=$(echo "$output" | head -c 200)
      fail "${skill_with_extract}: not-found path did not return expected message: ${err}"
    fi
  done
fi

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════════"
echo -e "Skills test results: ${G}${PASS} PASS${N} · ${Y}${SKIP} SKIP${N} · ${R}${FAIL} FAIL${N}"
echo "════════════════════════════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
  echo
  echo "Test harness FAILED. See per-check output above."
  exit 1
fi

if [ "$SKIP" -gt 0 ]; then
  echo
  echo "Some checks skipped (missing optional deps). Test harness PASS — installable upgrade path:"
  echo "  pip install pandas openpyxl --break-system-packages"
fi

exit 0
