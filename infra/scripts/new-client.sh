#!/usr/bin/env bash
# new-client.sh — scaffold a new client folder from pipeline/clients/_template/
#
# Usage:
#   bash infra/scripts/new-client.sh <slug> <country-ISO2> '<Legal Name>' <sector> [--pilot]
#
# Example:
#   bash infra/scripts/new-client.sh trixx-logistics MX 'Grupo Trixx' logistica --pilot
#
# Effect:
#   pipeline/clients/<slug>/                       ← copied from _template/
#   pipeline/clients/<slug>/00_intake/
#       research_input.md                          ← slug-substituted copy of skills/shared/research_input_template.md
#       our_hypotheses.md                          ← slug-substituted copy of skills/shared/our_hypotheses_template.md
#   pipeline/clients/<slug>/state.json             ← placeholders substituted
#   pipeline/clients/<slug>/checkpoint.md          ← slug + timestamp substituted
#   pipeline/clients/<slug>/README.md              ← replaced with per-client stub
#
# Idempotent failure: refuses to overwrite an existing pipeline/clients/<slug>/.
#
# Interim until Plan 07's full scaffolder (which adds events.jsonl emission, Telegram trigger, etc.).
# Per ADR-027 two-file intake split: research_input.md is read by Skills 01-03;
# our_hypotheses.md is SEALED during research and only read by Skills 04-05.

set -euo pipefail

# ─── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMPLATE_DIR="$REPO_ROOT/pipeline/clients/_template"
CLIENTS_DIR="$REPO_ROOT/pipeline/clients"
SHARED_TEMPLATES_DIR="$REPO_ROOT/skills/shared"

# ─── Usage / arg parsing ──────────────────────────────────────────────────────

usage() {
    cat <<'EOF'
Usage: bash infra/scripts/new-client.sh <slug> <country-ISO2> '<Legal Name>' <sector> [--pilot]

Args:
  <slug>           lowercase + dashes only (e.g., trixx-logistics)
  <country-ISO2>   CO | MX | other ISO-3166 alpha-2
  <Legal Name>     quoted; the full legal name
  <sector>         plain-text sector (e.g., logistica, cpg-alimentos, construccion)
  --pilot          (optional) set pilot=true in state.json
EOF
    exit 1
}

[[ $# -ge 4 ]] || usage

SLUG="$1"
COUNTRY="$2"
NAME="$3"
SECTOR="$4"
PILOT="false"

if [[ $# -ge 5 ]]; then
    if [[ "$5" == "--pilot" ]]; then
        PILOT="true"
    else
        echo "Unknown flag: $5" >&2
        usage
    fi
fi

# ─── Validation ───────────────────────────────────────────────────────────────

if [[ ! "$SLUG" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$ ]]; then
    echo "Invalid slug: '$SLUG'. Must be lowercase alphanumeric + dashes (no leading/trailing dash)." >&2
    exit 2
fi

if [[ ! "$COUNTRY" =~ ^[A-Z]{2}$ ]]; then
    echo "Invalid country: '$COUNTRY'. Must be ISO-3166 alpha-2 (e.g., CO, MX)." >&2
    exit 2
fi

if [[ ! -d "$TEMPLATE_DIR" ]]; then
    echo "Template not found at $TEMPLATE_DIR" >&2
    exit 3
fi

if [[ ! -f "$SHARED_TEMPLATES_DIR/research_input_template.md" \
   || ! -f "$SHARED_TEMPLATES_DIR/our_hypotheses_template.md" ]]; then
    echo "Intake templates missing in $SHARED_TEMPLATES_DIR" >&2
    exit 3
fi

TARGET="$CLIENTS_DIR/$SLUG"
if [[ -e "$TARGET" ]]; then
    echo "Refusing to overwrite existing $TARGET" >&2
    echo "If you really want to recreate, rm -rf it first (and check git status)." >&2
    exit 4
fi

# ─── Timestamps + operator ────────────────────────────────────────────────────

DATE_ISO="$(date -u +%F)"
TIMESTAMP_ISO="$(date -u +%FT%TZ)"
OPERATOR="${USER:-ricardo}"

# ─── Scaffold ─────────────────────────────────────────────────────────────────

cp -r "$TEMPLATE_DIR" "$TARGET"

# Copy 2-file intake templates per ADR-027
cp "$SHARED_TEMPLATES_DIR/research_input_template.md" "$TARGET/00_intake/research_input.md"
cp "$SHARED_TEMPLATES_DIR/our_hypotheses_template.md" "$TARGET/00_intake/our_hypotheses.md"

# Sed delimiter '|' avoids collisions with paths/spaces; escape only the name.
NAME_ESCAPED="${NAME//|/\\|}"

# Substitute placeholders in state.json
sed -i \
    -e "s|<slug>|$SLUG|g" \
    -e "s|<Full Legal Name>|$NAME_ESCAPED|g" \
    -e "s|<ISO-3166 alpha-2>|$COUNTRY|g" \
    -e "s|<plain-text sector>|$SECTOR|g" \
    -e "s|<ISO-8601 date>|$DATE_ISO|g" \
    -e "s|<ISO-8601 timestamp>|$TIMESTAMP_ISO|g" \
    -e "s|<persona — usually client-owner>|client-owner|g" \
    -e "s|<initiator — telegram-id or persona>|$OPERATOR|g" \
    "$TARGET/state.json"

# Flip pilot flag if requested
if [[ "$PILOT" == "true" ]]; then
    sed -i 's|"pilot": false|"pilot": true|' "$TARGET/state.json"
fi

# Substitute placeholders in checkpoint.md
sed -i \
    -e "s|<slug>|$SLUG|g" \
    -e "s|<ISO-8601 timestamp>|$TIMESTAMP_ISO|g" \
    -e "s|<session initiator>|$OPERATOR|g" \
    "$TARGET/checkpoint.md"

# Slug-stamp the intake template headers
sed -i "s|\`<slug>\`|\`$SLUG\`|g" \
    "$TARGET/00_intake/research_input.md" \
    "$TARGET/00_intake/our_hypotheses.md"

# Replace the carried-over _template README with a per-client stub
cat > "$TARGET/README.md" <<EOF
# $SLUG — $NAME

**Country:** $COUNTRY · **Sector:** $SECTOR · **Started:** $DATE_ISO · **Pilot:** $PILOT

Per-client work folder. Structure inherited from \`pipeline/clients/_template/\` —
see [\`../_template/README.md\`](../_template/README.md) for the 12-station + 3-cross-cutting
layout and the state-machine reference.

## Where things live (this client)

- **\`00_intake/research_input.md\`** — facts (ADR-027 slice 1+2). Read by Skills 01-03.
- **\`00_intake/our_hypotheses.md\`** — judgment (ADR-027 slice 3). SEALED during research; read by Skills 04-05.
- **\`state.json\`** — phase + history + pricing + KPIs. State-machine reference in \`../_template/README.md\`.
- **\`checkpoint.md\`** — session continuity baton (per ADR-031).
- **\`<NN>_<stage>/\`** — one folder per pipeline station (00 → 11).

## Next step

After editing \`00_intake/research_input.md\`, say in this Claude Code session:

> \`Analiza $SLUG\`

That triggers Skill 01 (company-analyst) with \`research_input.md\` as the operator-supplied context.
\`our_hypotheses.md\` remains sealed; it only opens when Skill 04 runs.
EOF

# ─── Done ─────────────────────────────────────────────────────────────────────

cat <<EOF

✓ Scaffolded $TARGET

Next steps:
  1. Edit  $TARGET/00_intake/research_input.md   (the facts you know)
  2. Edit  $TARGET/00_intake/our_hypotheses.md   (your judgment — keep this sealed during research)
  3. In Claude Code at /srv/Nexostrat/, say:    Analiza $SLUG
     → Skill 01 (company-analyst) reads research_input.md and runs the analysis.
     → Human review → Skill 02 → review → Skill 03 → review → Skill 04 (which now also reads our_hypotheses.md).

EOF

# ─── Plan 02a Task 8 — Baserow row sync ───────────────────────────────────────
# Non-fatal: filesystem is source of truth; baserow-reconcile.sh (Task 10) picks
# up orphans. Skipped if secrets aren't available.
#
# If BASEROW_URL is already in env (we're invoked from inside another
# run-with-secrets.sh context — e.g., pytest under the wrapper) call python3
# directly. Otherwise spawn run-with-secrets.sh to decrypt. Nesting the
# wrapper triggers a second age passphrase prompt in a subprocess that may
# have no usable TTY, and produces a UX wart in test output even when /dev/tty
# IS accessible.

run_baserow_sync() {
    python3 - <<PY
import os, sys
sys.path.insert(0, os.environ["REPO_ROOT"] + "/skills/shared")
import baserow
cid = baserow.post_client(
    slug=os.environ["NX_SLUG"],
    name=os.environ["NX_NAME"],
    display_name=os.environ["NX_NAME"],
    country=os.environ["NX_COUNTRY"],
    sector=os.environ["NX_SECTOR"],
    pilot=(os.environ["NX_PILOT"] == "true"),
    source="manual",
)
if cid is None:
    print("WARNING: Baserow client row not created — filesystem is source of truth", file=sys.stderr)
    sys.exit(0)
print(f"Baserow client row: id={cid}")
PY
}
export REPO_ROOT NX_SLUG="$SLUG" NX_NAME="$NAME" NX_COUNTRY="$COUNTRY" NX_SECTOR="$SECTOR" NX_PILOT="$PILOT"

if [[ -n "${BASEROW_URL:-}" && -n "${BASEROW_API_TOKEN:-}" ]]; then
    run_baserow_sync || echo "WARNING: Baserow sync failed" >&2
elif [[ -f "$REPO_ROOT/secrets.env.age" && -x "$REPO_ROOT/infra/scripts/run-with-secrets.sh" ]]; then
    export -f run_baserow_sync
    "$REPO_ROOT/infra/scripts/run-with-secrets.sh" bash -c run_baserow_sync \
        || echo "WARNING: Baserow sync skipped (run-with-secrets failed)" >&2
else
    echo "WARNING: secrets.env.age or run-with-secrets.sh missing — Baserow row not created" >&2
fi
