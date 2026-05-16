#!/usr/bin/env bash
# Validate tasks.json + calendar.json against their schemas.
set -euo pipefail
cd /srv/Nexostrat

python3 - <<'PYEOF'
import json, sys
from jsonschema import Draft202012Validator, FormatChecker

failures = []

for data_path, schema_path, label in [
    ("tasks.json",    "infra/schemas/tasks.schema.json",    "tasks"),
    ("calendar.json", "infra/schemas/calendar.schema.json", "calendar"),
]:
    try:
        with open(data_path) as f: data = json.load(f)
        with open(schema_path) as f: schema = json.load(f)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            for e in errors:
                path = "$" + "".join(f"[{p!r}]" if isinstance(p, str) else f"[{p}]" for p in e.absolute_path)
                msg = f"FAIL  {label} — {path}: {e.message}"
                failures.append(msg); print(msg)
        else:
            print(f"PASS  {label} ({data_path} validates against {schema_path})")
    except FileNotFoundError as e:
        failures.append(f"FAIL  {label} — file missing: {e}"); print(failures[-1])
    except Exception as e:
        failures.append(f"FAIL  {label} — {type(e).__name__}: {e}"); print(failures[-1])

if failures: sys.exit(1)
PYEOF
