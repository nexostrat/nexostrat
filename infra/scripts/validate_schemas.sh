#!/usr/bin/env bash
# Validate tasks.json + calendar.json against their schemas.
set -euo pipefail
cd /srv/Nexostrat

python3 - <<'PYEOF'
import json, sys
import jsonschema

failures = []

for data_path, schema_path, label in [
    ("tasks.json",    "infra/schemas/tasks.schema.json",    "tasks"),
    ("calendar.json", "infra/schemas/calendar.schema.json", "calendar"),
]:
    try:
        with open(data_path) as f: data = json.load(f)
        with open(schema_path) as f: schema = json.load(f)
        jsonschema.validate(instance=data, schema=schema)
        print(f"PASS  {label} ({data_path} validates against {schema_path})")
    except FileNotFoundError as e:
        failures.append(f"FAIL  {label} — file missing: {e}")
        print(failures[-1])
    except jsonschema.ValidationError as e:
        failures.append(f"FAIL  {label} — schema violation: {e.message}")
        print(failures[-1])
    except Exception as e:
        failures.append(f"FAIL  {label} — {type(e).__name__}: {e}")
        print(failures[-1])

if failures: sys.exit(1)
PYEOF
