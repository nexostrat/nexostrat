#!/usr/bin/env bash
# baserow-schema-check.sh — Nexostrat
#
# Compares the live Baserow schema against infra/baserow/schema/canonical.json.
# Exit 0 on match, 1 on drift, 2 on missing canonical.
#
# Normally invoked under run-with-secrets.sh (which sources BASEROW_URL,
# BASEROW_EMAIL, BASEROW_PASSWORD into env). The systemd unit's ExecStart
# wraps with that. Local manual runs:
#
#   infra/scripts/run-with-secrets.sh infra/scripts/baserow-schema-check.sh

set -euo pipefail
NEXOSTRAT=${NEXOSTRAT:-/srv/Nexostrat}
CANONICAL="$NEXOSTRAT/infra/baserow/schema/canonical.json"
TMP_LIVE=$(mktemp)
trap "rm -f $TMP_LIVE" EXIT

python3 -c "
import sys, json, pathlib
sys.path.insert(0, '$NEXOSTRAT/infra/baserow')
from export_schema import dump_schema
print(json.dumps(dump_schema(), indent=2, sort_keys=True))
" > "$TMP_LIVE"

if [ ! -f "$CANONICAL" ]; then
    echo "ERROR: $CANONICAL not found — run export_schema.py first" >&2
    exit 2
fi

if diff -u "$CANONICAL" "$TMP_LIVE"; then
    echo "OK: schema matches canonical.json"
    exit 0
else
    echo "DRIFT DETECTED — see diff above" >&2
    exit 1
fi
