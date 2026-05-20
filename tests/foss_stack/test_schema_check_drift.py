"""Synthetic schema drift → check script must detect."""
import subprocess, os, json, pathlib, pytest

NEXOSTRAT = "/srv/Nexostrat"
CANONICAL = pathlib.Path(f"{NEXOSTRAT}/infra/baserow/schema/canonical.json")


def _run_check():
    if os.environ.get("BASEROW_URL") and os.environ.get("BASEROW_EMAIL"):
        return subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/baserow-schema-check.sh"],
            capture_output=True, text=True
        )
    return subprocess.run(
        [f"{NEXOSTRAT}/infra/scripts/run-with-secrets.sh",
         f"{NEXOSTRAT}/infra/scripts/baserow-schema-check.sh"],
        capture_output=True, text=True
    )


def test_clean_schema_passes():
    r = _run_check()
    assert r.returncode == 0, f"stdout={r.stdout}\nstderr={r.stderr}"


def test_drift_detected(tmp_path):
    """Mutate canonical.json briefly, run check, restore."""
    backup = tmp_path / "canonical.backup.json"
    backup.write_text(CANONICAL.read_text())
    try:
        data = json.loads(CANONICAL.read_text())
        data["tables"]["clients"]["fields"].append(
            {"name": "FAKE_DRIFT_FIELD", "type": "text"}
        )
        CANONICAL.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        r = _run_check()
        assert r.returncode != 0, "drift should have been detected"
        assert "FAKE_DRIFT_FIELD" in (r.stdout + r.stderr)
    finally:
        CANONICAL.write_text(backup.read_text())
