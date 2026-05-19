"""Run migrations twice. Second run must be a clean no-op."""
import subprocess, os
import pytest

NEXOSTRAT = os.environ.get("NEXOSTRAT", "/srv/Nexostrat")

def run_migrations():
    return subprocess.run(
        [f"{NEXOSTRAT}/infra/scripts/run-with-secrets.sh",
         "python3", f"{NEXOSTRAT}/infra/baserow/migrations/run_all.py"],
        capture_output=True, text=True, check=False
    )

def test_first_run_creates_tables():
    r = run_migrations()
    assert r.returncode == 0, f"stderr={r.stderr}"
    assert "CREATED" in r.stdout.upper() or "EXISTS" in r.stdout.upper()

def test_second_run_is_noop():
    r = run_migrations()
    assert r.returncode == 0, f"stderr={r.stderr}"
    assert r.stdout.count("CREATED") == 0
    assert r.stdout.count("EXISTS") >= 4  # at least 4 tables
