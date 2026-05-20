#!/usr/bin/env bash
# Discover Baserow table IDs via JWT login + walk, then upsert them as
# BASEROW_TABLE_<NAME>_ID env vars into secrets.env.age.
#
# Why: the Database API Token in vault is row-CRUD scoped; it can't list
# workspaces/databases/tables. skills/shared/baserow.py needs the IDs to
# address /api/database/rows/table/{id}/, so we discover them once via JWT
# (BASEROW_EMAIL/PASSWORD) and persist into the encrypted env file.
#
# Re-runnable: if the IDs change (Baserow database recreated, table renumbered),
# re-run and the new IDs overwrite the old.

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
SECRETS_ENC="$NEXOSTRAT/secrets.env.age"
AGE_KEY="$HOME/.config/age/nexostrat.key.age"
RECIPIENTS="$NEXOSTRAT/infra/age-recipients.txt"
PLAIN="$(mktemp -p /dev/shm nexostrat-tableids-XXXX.env)"

cleanup() {
    [ -f "$PLAIN" ] && shred -u "$PLAIN" 2>/dev/null || rm -f "$PLAIN" 2>/dev/null
}
trap cleanup EXIT INT TERM HUP

[ -f "$AGE_KEY" ]     || { echo "ERROR: $AGE_KEY not found" >&2; exit 1; }
[ -f "$RECIPIENTS" ]  || { echo "ERROR: $RECIPIENTS not found" >&2; exit 1; }
[ -f "$SECRETS_ENC" ] || { echo "ERROR: $SECRETS_ENC not found" >&2; exit 1; }

echo "Decrypting $SECRETS_ENC (will prompt for age passphrase)..."
age -d -i "$AGE_KEY" "$SECRETS_ENC" > "$PLAIN"
chmod 600 "$PLAIN"

# Discover IDs by sourcing the env vars into a Python subprocess that uses
# the existing _api.py (JWT auth) to walk the schema.
IDS_OUT="$(mktemp)"
trap "rm -f $IDS_OUT; cleanup" EXIT INT TERM HUP

(
    set -a
    # shellcheck disable=SC1090
    source "$PLAIN"
    set +a
    python3 - "$IDS_OUT" <<'PY'
import sys, json, pathlib
sys.path.insert(0, "/srv/Nexostrat/infra/baserow/migrations")
from _api import get_or_create_workspace, get_or_create_database, get

ws = get_or_create_workspace("Nexostrat")
db = get_or_create_database(ws, "nexostrat")
tables = get(f"/api/database/tables/database/{db}/")
out = pathlib.Path(sys.argv[1])
ids = {}
for t in tables:
    if t["name"] in {"clients", "meetings", "deliverables", "financials"}:
        ids[t["name"]] = t["id"]
out.write_text(json.dumps(ids, sort_keys=True))
print("Discovered:", ids)
PY
)

# Now upsert each BASEROW_TABLE_<NAME>_ID line into the decrypted plaintext.
KEYS_FILE="$IDS_OUT" PLAIN_FILE="$PLAIN" python3 - <<'PYEOF'
import json, os, pathlib
ids = json.loads(pathlib.Path(os.environ["KEYS_FILE"]).read_text())
plain = pathlib.Path(os.environ["PLAIN_FILE"])
lines = plain.read_text().splitlines()

for table, tid in ids.items():
    key = f"BASEROW_TABLE_{table.upper()}_ID"
    new = f"{key}={tid}"
    replaced = False
    for i, ln in enumerate(lines):
        if ln.startswith(f"{key}="):
            lines[i] = new
            replaced = True
            break
    if not replaced:
        lines.append(new)
    print(f"  upserted: {new}")

plain.write_text("\n".join(lines) + "\n")
PYEOF

age -e -R "$RECIPIENTS" -o "$SECRETS_ENC.tmp" "$PLAIN"
mv "$SECRETS_ENC.tmp" "$SECRETS_ENC"
echo "Re-encrypted $SECRETS_ENC with table-id env vars"
