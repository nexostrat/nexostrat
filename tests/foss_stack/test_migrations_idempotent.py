"""Migrations are idempotent and produce the expected schema state."""
import subprocess, os, sys, pathlib

NEXOSTRAT = os.environ.get("NEXOSTRAT", "/srv/Nexostrat")
EXPECTED_TABLES = {"clients", "meetings", "deliverables", "financials"}


def run_migrations():
    # If the parent already sourced secrets (typical when this file is invoked
    # via run-with-secrets.sh), call run_all.py directly so we avoid a second
    # age passphrase prompt per test.
    if os.environ.get("BASEROW_URL") and os.environ.get("BASEROW_EMAIL"):
        cmd = ["python3", f"{NEXOSTRAT}/infra/baserow/migrations/run_all.py"]
    else:
        cmd = [f"{NEXOSTRAT}/infra/scripts/run-with-secrets.sh",
               "python3", f"{NEXOSTRAT}/infra/baserow/migrations/run_all.py"]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _api():
    sys.path.insert(0, f"{NEXOSTRAT}/infra/baserow/migrations")
    import _api
    return _api


def test_migrations_run_successfully():
    r = run_migrations()
    assert r.returncode == 0, f"stderr={r.stderr}"


def test_second_run_is_noop():
    r = run_migrations()
    assert r.returncode == 0, f"stderr={r.stderr}"
    assert r.stdout.count("CREATED") == 0, (
        f"second run must not create anything; saw:\n{r.stdout}")
    assert r.stdout.count("EXISTS") >= 4


def test_expected_tables_present_in_baserow():
    """Behavioral check: query the live API and assert the schema matches."""
    api = _api()
    ws = api.get_or_create_workspace("Nexostrat")
    db = api.get_or_create_database(ws, "nexostrat")
    tables = api.get(f"/api/database/tables/database/{db}/")
    names = {t["name"] for t in tables}
    assert EXPECTED_TABLES <= names, (
        f"missing tables: {EXPECTED_TABLES - names}; got: {names}")
