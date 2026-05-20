"""baserow-reconcile.sh — synthetic orphan .md → reconcile creates the row.

Skips cleanly when BASEROW_URL+BASEROW_API_TOKEN are absent (subagent /
no-secrets context). When live, the test:
  1. Scaffolds a throwaway client (creates the Baserow `clients` row).
  2. Synthesizes a .md + .docx under 01_company_analysis/runs/<date>/ WITHOUT
     calling post_deliverable — simulating a renderer bypass or hand-edit.
  3. Confirms no deliverables row yet.
  4. Runs baserow-reconcile.sh.
  5. Asserts the row landed with the right `skill` (single_select) and
     `file_docx` path.
"""
import os, subprocess, sys, time, shutil, pathlib
import pytest

NEXOSTRAT = "/srv/Nexostrat"
sys.path.insert(0, f"{NEXOSTRAT}/skills/shared")


@pytest.fixture
def baserow_module():
    if not (os.environ.get("BASEROW_URL") and os.environ.get("BASEROW_API_TOKEN")):
        pytest.skip("Baserow env not set — run under run-with-secrets.sh")
    import baserow
    return baserow


def _run_reconcile():
    """Invoke baserow-reconcile.sh directly when env is already populated;
    otherwise spawn the wrapper. Mirrors the script's own dual-mode logic.
    """
    if os.environ.get("BASEROW_URL") and os.environ.get("BASEROW_API_TOKEN"):
        cmd = [f"{NEXOSTRAT}/infra/scripts/baserow-reconcile.sh"]
    else:
        cmd = [
            f"{NEXOSTRAT}/infra/scripts/run-with-secrets.sh",
            f"{NEXOSTRAT}/infra/scripts/baserow-reconcile.sh",
        ]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_reconcile_creates_orphan_row(baserow_module):
    slug = f"zz-test-rec-{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")
    try:
        # 1. Scaffold a client (creates Baserow client row via new-client.sh).
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Reconcile Test SA", "testing"],
            capture_output=True, text=True, cwd=NEXOSTRAT,
        )
        assert r.returncode == 0, f"new-client failed: {r.stderr}"

        # 2. Synthesize an orphan .md (no post_deliverable was called).
        run_dir = folder / "01_company_analysis/runs/2026-05-19_mode-a"
        run_dir.mkdir(parents=True, exist_ok=True)
        md = run_dir / f"{slug}_AnalisisCompania_20260519.md"
        docx = run_dir / f"{slug}_AnalisisCompania_20260519.docx"
        md.write_text("orphan body — written without invoking the renderer")
        docx.write_text("dummy bytes — pretending to be a .docx")

        # 3. Confirm no deliverable row exists yet.
        assert baserow_module._find_one("deliverables", "file_md", str(md)) is None, (
            "deliverables row already exists pre-reconcile — test fixture is dirty")

        # 4. Run reconcile.
        r = _run_reconcile()
        assert r.returncode == 0, (
            f"reconcile failed: rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}")
        assert "orphan(s) added" in r.stdout, (
            f"summary line missing from stdout:\n{r.stdout}")

        # 5. Row now present with the right shape.
        row = baserow_module._find_one("deliverables", "file_md", str(md))
        assert row is not None, "reconcile didn't pick up the orphan"
        # `skill` is a single_select → {"id":..., "value":..., "color":...}
        assert row["skill"]["value"] == "company-analyst"
        assert row["file_docx"] == str(docx)
    finally:
        if folder.exists():
            shutil.rmtree(folder)
