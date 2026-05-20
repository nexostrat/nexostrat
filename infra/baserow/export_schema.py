"""Dump live Baserow schema to deterministic JSON for drift detection.

Reads workspace → database → tables → fields → views via the same JWT-auth
REST client used by migrations (_api.get). Strips API IDs (not stable across
re-creation) and keeps only the structural attributes that matter for diff:
field name, field type, select_options (sorted by value), and formula string
when present. Tables and views are sorted by name; fields are sorted by name.

Usage:
    run-with-secrets.sh python3 infra/baserow/export_schema.py

Writes canonical JSON to infra/baserow/schema/canonical.json.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent / "migrations"))
from _api import get  # noqa: E402


def _field_entry(field: dict) -> dict:
    """Strip API IDs; keep name, type, sorted select_options, formula."""
    entry = {"name": field["name"], "type": field["type"]}
    opts = field.get("select_options")
    if opts:
        entry["select_options"] = sorted(
            [{"value": o["value"]} for o in opts],
            key=lambda o: o["value"],
        )
    formula = field.get("formula")
    if formula:
        entry["formula"] = formula
    return entry


def dump_schema(workspace_name: str = "Nexostrat",
                database_name: str = "nexostrat") -> dict:
    """Return canonical schema dict: workspace → database → tables → fields/views."""
    workspaces = get("/api/workspaces/")
    ws = next((w for w in workspaces if w["name"] == workspace_name), None)
    if ws is None:
        raise RuntimeError(f"workspace not found: {workspace_name}")

    apps = get(f"/api/applications/workspace/{ws['id']}/")
    db = next(
        (a for a in apps
         if a["name"] == database_name and a["type"] == "database"),
        None,
    )
    if db is None:
        raise RuntimeError(f"database not found: {database_name}")

    tables = get(f"/api/database/tables/database/{db['id']}/")
    tables_sorted = sorted(tables, key=lambda t: t["name"])

    out_tables: dict = {}
    for t in tables_sorted:
        fields = get(f"/api/database/fields/table/{t['id']}/")
        fields_sorted = sorted(fields, key=lambda f: f["name"])
        field_entries = [_field_entry(f) for f in fields_sorted]

        views = get(f"/api/database/views/table/{t['id']}/")
        view_names = sorted(v["name"] for v in views)

        out_tables[t["name"]] = {
            "fields": field_entries,
            "views": view_names,
        }

    return {
        "workspace": workspace_name,
        "database": database_name,
        "tables": out_tables,
    }


def main() -> None:
    out_dir = pathlib.Path(__file__).parent / "schema"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "canonical.json"
    data = dump_schema()
    payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
    out_path.write_text(payload, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
