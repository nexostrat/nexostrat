#!/usr/bin/env bash
# Interactive setup for the Nexostrat FOSS stack.
#
# Generates random passwords for Postgres/MySQL/Laravel, writes them to
# infra/docker/foss-stack/.env (host-only, mode 600, gitignored).
#
# Appends Baserow + BookStack URL + token stubs to secrets.env.age (the encrypted
# vault file). After this script: services can be brought up; user then generates
# API tokens via web UI and replaces stubs (Steps 6-9 of Plan 02a Task 3).
#
# Uses `age` directly (no run-with-secrets.sh modes). Decrypt step prompts for
# Ricardo's age key passphrase.

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
ENV_FILE="$NEXOSTRAT/infra/docker/foss-stack/.env"
SECRETS_ENC="$NEXOSTRAT/secrets.env.age"
AGE_KEY="$HOME/.config/age/nexostrat.key.age"
RECIPIENTS="$NEXOSTRAT/infra/age-recipients.txt"
PLAIN="$(mktemp -p /dev/shm nexostrat-secrets-XXXX.env)"

cleanup() {
    [ -f "$PLAIN" ] && shred -u "$PLAIN" 2>/dev/null || rm -f "$PLAIN" 2>/dev/null
}
trap cleanup EXIT INT TERM HUP

# Sanity checks
[ -f "$AGE_KEY" ] || { echo "ERROR: $AGE_KEY not found" >&2; exit 1; }
[ -f "$RECIPIENTS" ] || { echo "ERROR: $RECIPIENTS not found" >&2; exit 1; }
[ -f "$SECRETS_ENC" ] || { echo "ERROR: $SECRETS_ENC not found" >&2; exit 1; }

if [ -f "$ENV_FILE" ]; then
    echo "WARN: $ENV_FILE already exists; refusing to overwrite." >&2
    echo "      Delete it manually if you want to regenerate the stack passwords." >&2
    exit 1
fi

# ── Generate random secrets ─────────────────────────────────────
gen() { openssl rand -hex 32; }
BASEROW_DATABASE_PASSWORD=$(gen)
BASEROW_SECRET_KEY=$(gen)
BASEROW_JWT_SIGNING_KEY=$(gen)
BOOKSTACK_DB_PASSWORD=$(gen)
BOOKSTACK_DB_ROOT_PASSWORD=$(gen)
BOOKSTACK_APP_KEY="base64:$(openssl rand -base64 32)"

# ── Write .env (mode 600) ───────────────────────────────────────
cat > "$ENV_FILE" <<ENV_EOF
BASEROW_PUBLIC_URL=https://baserow.nexostrat.local
BASEROW_DATABASE_PASSWORD=$BASEROW_DATABASE_PASSWORD
BASEROW_SECRET_KEY=$BASEROW_SECRET_KEY
BASEROW_JWT_SIGNING_KEY=$BASEROW_JWT_SIGNING_KEY

BOOKSTACK_APP_URL=https://docs.nexostrat.local
BOOKSTACK_DB_PASSWORD=$BOOKSTACK_DB_PASSWORD
BOOKSTACK_DB_ROOT_PASSWORD=$BOOKSTACK_DB_ROOT_PASSWORD
BOOKSTACK_APP_KEY=$BOOKSTACK_APP_KEY

CADDY_LOCAL_CA=internal
COMPOSE_PROJECT_NAME=nexostrat-foss
ENV_EOF
chmod 600 "$ENV_FILE"
echo "Wrote $ENV_FILE (mode 600)"

# ── Append stubs to secrets.env.age ─────────────────────────────
echo "Decrypting $SECRETS_ENC (will prompt for age passphrase)..."
age -d -i "$AGE_KEY" "$SECRETS_ENC" > "$PLAIN"
chmod 600 "$PLAIN"

if grep -q "^BASEROW_URL=" "$PLAIN"; then
    echo "secrets.env.age already has Baserow/BookStack entries — leaving as-is"
else
    cat >> "$PLAIN" <<STUB_EOF

# FOSS stack — URLs + token stubs (real tokens added after web-UI gen)
BASEROW_URL=https://baserow.nexostrat.local
BASEROW_API_TOKEN=__SET_AFTER_UI_GEN__
BOOKSTACK_URL=https://docs.nexostrat.local
BOOKSTACK_API_TOKEN=__SET_AFTER_UI_GEN__
BOOKSTACK_API_SECRET=__SET_AFTER_UI_GEN__
STUB_EOF
    age -e -R "$RECIPIENTS" -o "$SECRETS_ENC.tmp" "$PLAIN"
    mv "$SECRETS_ENC.tmp" "$SECRETS_ENC"
    echo "Appended URL + token stubs to $SECRETS_ENC"
fi

echo ""
echo "NEXT (manual):"
echo "  1. Add /etc/hosts entry (if not already):"
echo "     sudo sh -c \"grep -q baserow.nexostrat.local /etc/hosts || echo '100.64.121.80 baserow.nexostrat.local docs.nexostrat.local' >> /etc/hosts\""
echo "  2. Start the stack:"
echo "     sudo systemctl enable --now nexostrat-foss-stack.service"
echo "  3. Wait ~90s, verify containers healthy:"
echo "     docker compose -f $NEXOSTRAT/infra/docker/foss-stack/docker-compose.yml ps"
echo "  4. Browser: create Baserow admin + API token (https://baserow.nexostrat.local)"
echo "  5. Browser: create BookStack admin + API token (https://docs.nexostrat.local)"
echo "  6. Run: $NEXOSTRAT/infra/scripts/write-foss-tokens.sh  (script that follows in Step 8)"
