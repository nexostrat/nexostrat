#!/usr/bin/env bash
# Interactive: add BASEROW_EMAIL + BASEROW_PASSWORD to secrets.env.age.
#
# Why: Baserow's Database API Token (BASEROW_API_TOKEN, scope=row-CRUD) cannot
# create workspaces/databases/tables/fields/views. Schema operations require
# JWT auth obtained via /api/user/token-auth/ with email + password.
#
# Plan 02a Task 4 (and Tasks 5-6) uses these credentials in
# infra/baserow/migrations/_api.py to log in once per run, then carries the
# JWT in Authorization: JWT <token>.
#
# After this script: re-encrypted secrets.env.age contains
#   BASEROW_EMAIL=<admin email>
#   BASEROW_PASSWORD=<admin password>

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
SECRETS_ENC="$NEXOSTRAT/secrets.env.age"
AGE_KEY="$HOME/.config/age/nexostrat.key.age"
RECIPIENTS="$NEXOSTRAT/infra/age-recipients.txt"
PLAIN="$(mktemp -p /dev/shm nexostrat-jwt-XXXX.env)"

cleanup() {
    [ -f "$PLAIN" ] && shred -u "$PLAIN" 2>/dev/null || rm -f "$PLAIN" 2>/dev/null
}
trap cleanup EXIT INT TERM HUP

[ -f "$AGE_KEY" ]    || { echo "ERROR: $AGE_KEY not found" >&2; exit 1; }
[ -f "$RECIPIENTS" ] || { echo "ERROR: $RECIPIENTS not found" >&2; exit 1; }
[ -f "$SECRETS_ENC" ] || { echo "ERROR: $SECRETS_ENC not found" >&2; exit 1; }

echo "Decrypting $SECRETS_ENC (will prompt for age passphrase)..."
age -d -i "$AGE_KEY" "$SECRETS_ENC" > "$PLAIN"
chmod 600 "$PLAIN"

# Sanity: the URL must already be present (set during setup-foss-stack-secrets.sh)
if ! grep -q "^BASEROW_URL=" "$PLAIN"; then
    echo "ERROR: BASEROW_URL missing from secrets — run setup-foss-stack-secrets.sh first" >&2
    exit 1
fi

# Prompt
read -rp  "Baserow admin email: " EMAIL
read -rsp "Baserow admin password: " PASSWORD; echo

[ -n "$EMAIL" ]    || { echo "ERROR: email cannot be empty" >&2; exit 1; }
[ -n "$PASSWORD" ] || { echo "ERROR: password cannot be empty" >&2; exit 1; }

# Verify credentials by hitting the live JWT endpoint BEFORE persisting them
BASEROW_URL_VAL=$(grep "^BASEROW_URL=" "$PLAIN" | head -1 | cut -d= -f2-)
echo "Verifying credentials against $BASEROW_URL_VAL/api/user/token-auth/ ..."
JWT_RESP=$(curl -sk -w "\n%{http_code}" \
    -X POST "$BASEROW_URL_VAL/api/user/token-auth/" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
HTTP_CODE=$(echo "$JWT_RESP" | tail -n1)
BODY=$(echo "$JWT_RESP" | sed '$d')

if [ "$HTTP_CODE" != "200" ]; then
    echo "ERROR: JWT login failed (HTTP $HTTP_CODE)" >&2
    echo "  response: $BODY" >&2
    exit 1
fi
echo "OK: JWT login succeeded (HTTP 200)"

# Upsert lines into the decrypted plaintext
upsert() {
    local key="$1" value="$2"
    if grep -q "^${key}=" "$PLAIN"; then
        # Escape sed special chars in the value (|, &, /)
        local esc; esc=$(printf '%s' "$value" | sed 's/[|&/\]/\\&/g')
        sed -i "s|^${key}=.*|${key}=${esc}|" "$PLAIN"
    else
        printf '%s=%s\n' "$key" "$value" >> "$PLAIN"
    fi
}

upsert BASEROW_EMAIL "$EMAIL"
upsert BASEROW_PASSWORD "$PASSWORD"

# Re-encrypt
age -e -R "$RECIPIENTS" -o "$SECRETS_ENC.tmp" "$PLAIN"
mv "$SECRETS_ENC.tmp" "$SECRETS_ENC"
echo "Updated $SECRETS_ENC with BASEROW_EMAIL + BASEROW_PASSWORD"

unset EMAIL PASSWORD JWT_RESP HTTP_CODE BODY BASEROW_URL_VAL

echo ""
echo "Verify the JWT flow from a Python repl (Task 4 _api.py will do the same):"
echo "  $NEXOSTRAT/infra/scripts/run-with-secrets.sh \\"
echo "    python3 -c 'import os, json, urllib.request, ssl; "
echo "ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE; "
echo "r=urllib.request.urlopen(urllib.request.Request("
echo "  os.environ[\"BASEROW_URL\"]+\"/api/user/token-auth/\", "
echo "  data=json.dumps({\"email\":os.environ[\"BASEROW_EMAIL\"],"
echo "    \"password\":os.environ[\"BASEROW_PASSWORD\"]}).encode(),"
echo "  headers={\"Content-Type\":\"application/json\"}, method=\"POST\"), context=ctx); "
echo "print(\"JWT len:\", len(json.loads(r.read())[\"token\"]))'"
