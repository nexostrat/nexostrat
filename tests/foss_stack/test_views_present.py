"""Predefined views per spec §4.5 exist after 05_views.py runs."""
import os, sys
import pytest

NEXOSTRAT = os.environ.get("NEXOSTRAT", "/srv/Nexostrat")
sys.path.insert(0, f"{NEXOSTRAT}/infra/baserow/migrations")
import _api  # noqa: E402


def _table_id(name: str) -> int:
    workspaces = _api.get("/api/workspaces/")
    for w in workspaces:
        if w["name"] != "Nexostrat":
            continue
        apps = _api.get(f"/api/applications/workspace/{w['id']}/")
        for app in apps:
            if app["name"] != "nexostrat" or app["type"] != "database":
                continue
            tables = _api.get(f"/api/database/tables/database/{app['id']}/")
            for t in tables:
                if t["name"] == name:
                    return t["id"]
    raise RuntimeError(f"table not found: {name}")


@pytest.mark.parametrize("table_name,expected_views", [
    ("clients", ["Pipeline activo", "Pilotos", "Por país"]),
    ("meetings", ["Próximas", "Esta semana", "Pendientes de transcripción"]),
    ("deliverables", ["Esta semana", "En revisión interna", "Por skill"]),
    ("financials", ["Mes en curso", "Por cobrar"]),
])
def test_expected_views_present(table_name, expected_views):
    tid = _table_id(table_name)
    views = _api.get(f"/api/database/views/table/{tid}/")
    names = {v["name"] for v in views}
    missing = set(expected_views) - names
    assert not missing, (
        f"table {table_name}: missing views {missing}; got: {names}")
