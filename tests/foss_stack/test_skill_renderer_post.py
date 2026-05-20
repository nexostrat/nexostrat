"""End-to-end: a skill renderer writing a .docx also creates a deliverables row.

Smoke-tests skill 01 (company-analyst) as a representative — the patch
template is identical across all 5 renderers, so 01 passing implies the
shape works.
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


def test_skill_01_renderer_creates_deliverable_row(baserow_module):
    slug = f"zz-test-rend-{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")
    try:
        # 1. Scaffold a throwaway client — creates the Baserow client row too.
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Renderer Test SA", "testing"],
            capture_output=True, text=True, cwd=NEXOSTRAT
        )
        assert r.returncode == 0, f"new-client failed: {r.stderr}"
        client = baserow_module._find_one("clients", "slug", slug)
        assert client is not None, "new-client.sh didn't create the Baserow client row"

        # 2. Place a markdown file at the canonical layout so parts[-5] == slug.
        run_dir = folder / "01_company_analysis/runs/2026-05-19_mode-a"
        run_dir.mkdir(parents=True, exist_ok=True)
        md = run_dir / f"{slug}_AnalisisCompania_20260519.md"
        md.write_text(
            "# Test Analysis\n\n"
            "## Sección 1\n\n"
            "Minimal body — enough markdown for the renderer to produce a .docx.\n"
        )
        docx = run_dir / f"{slug}_AnalisisCompania_20260519.docx"

        # 3. Invoke the renderer (no run-with-secrets wrapper — we're inside it).
        r = subprocess.run(
            ["python3",
             f"{NEXOSTRAT}/skills/01_company_analyst/scripts/generate_docx.py",
             str(md), str(docx)],
            capture_output=True, text=True
        )
        assert r.returncode == 0, (
            f"renderer failed: rc={r.returncode}\nstdout={r.stdout}\nstderr={r.stderr}")
        assert docx.exists(), "renderer didn't write the .docx"

        # 4. Assert the deliverables row landed in Baserow.
        deliv = baserow_module._find_one("deliverables", "file_md", str(md))
        assert deliv is not None, (
            f"deliverables row not created. renderer stderr was: {r.stderr}")
        assert deliv["file_docx"] == str(docx)
        # `skill` is a single_select → returned as {"id":..., "value":..., "color":...}
        assert deliv["skill"]["value"] == "company-analyst"
    finally:
        if folder.exists():
            shutil.rmtree(folder)
