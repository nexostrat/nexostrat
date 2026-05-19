#!/usr/bin/env bash
# Interactive: replace BASEROW_API_TOKEN, BOOKSTACK_API_TOKEN, BOOKSTACK_API_SECRET
# stubs in secrets.env.age with real values generated from the web UIs.
#
# Run AFTER:
#   1. setup-foss-stack-secrets.sh ran successfully
#   2. Stack is up (sudo systemctl start nexostrat-foss-stack.service)
#   3. Baserow admin account + API token created via web UI
#   4. BookStack admin account + API token (Token ID + Token Secret) created via web UI

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
SECRETS_ENC="$NEXOSTRAT/secrets.env.age"
AGE_KEY="$HOME/.config/age/nexostrat.key.age"
RECIPIENTS="$NEXOSTRAT/infra/age-recipients.txt"
PLAIN="$(mktemp -p /dev/shm nexostrat-tokens-XXXX.env)"

cleanup() {
    [ -f "$PLAIN" ] && shred -u "$PLAIN" 2>/dev/null || rm -f "$PLAIN" 2>/dev/null
}
trap cleanup EXIT INT TERM HUP

echo "Decrypting $SECRETS_ENC (will prompt for age passphrase)..."
age -d -i "$AGE_KEY" "$SECRETS_ENC" > "$PLAIN"
chmod 600 "$PLAIN"

if ! grep -q "BASEROW_API_TOKEN=__SET_AFTER_UI_GEN__" "$PLAIN"; then
    echo "WARN: BASEROW_API_TOKEN stub not found in decrypted secrets — already set?"
    grep "^BASEROW_API_TOKEN=" "$PLAIN" | sed 's|=.*|=<existing>|'
    echo "Continuing anyway — you can paste empty string to leave existing values."
fi

echo ""
read -rsp "Paste Baserow API token (or empty to skip): " BASEROW_TOKEN; echo
read -rsp "Paste BookStack API Token ID (or empty to skip): " BOOKSTACK_ID; echo
read -rsp "Paste BookStack API Token Secret (or empty to skip): " BOOKSTACK_SECRET; echo

[ -n "$BASEROW_TOKEN" ] && sed -i "s|^BASEROW_API_TOKEN=.*|BASEROW_API_TOKEN=$BASEROW_TOKEN|" "$PLAIN"
[ -n "$BOOKSTACK_ID" ] && sed -i "s|^BOOKSTACK_API_TOKEN=.*|BOOKSTACK_API_TOKEN=$BOOKSTACK_ID|" "$PLAIN"
[ -n "$BOOKSTACK_SECRET" ] && sed -i "s|^BOOKSTACK_API_SECRET=.*|BOOKSTACK_API_SECRET=$BOOKSTACK_SECRET|" "$PLAIN"

age -e -R "$RECIPIENTS" -o "$SECRETS_ENC.tmp" "$PLAIN"
mv "$SECRETS_ENC.tmp" "$SECRETS_ENC"
echo "Updated $SECRETS_ENC"

unset BASEROW_TOKEN BOOKSTACK_ID BOOKSTACK_SECRET

echo ""
echo "Verify tokens work:"
echo "  /srv/Nexostrat/infra/scripts/run-with-secrets.sh \\"
echo "    sh -c 'curl -sk -H \"Authorization: Token \$BASEROW_API_TOKEN\" \"\$BASEROW_URL/api/database/workspaces/\" | head -c 200; echo'"
