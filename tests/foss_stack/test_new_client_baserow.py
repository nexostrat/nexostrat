"""new-client.sh creates folder + Baserow row. Re-run is idempotent."""
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


def test_new_client_creates_folder_and_baserow_row(baserow_module):
    # new-client.sh enforces lowercase + dashes only (no underscores, no
    # leading/trailing dash). Use a dash-form throwaway slug. The "zz-" prefix
    # sorts these to the bottom of any pipeline/clients/ listing.
    slug = f"zz-test-nc-{int(time.time())}"
    folder = pathlib.Path(f"{NEXOSTRAT}/pipeline/clients/{slug}")
    try:
        r = subprocess.run(
            [f"{NEXOSTRAT}/infra/scripts/new-client.sh",
             slug, "MX", "Test Cliente SA", "testing"],
            capture_output=True, text=True, cwd=NEXOSTRAT
        )
        assert r.returncode == 0, f"new-client failed: {r.stderr}"
        assert folder.exists(), "folder not created"
        assert (folder / "state.json").exists(), "state.json not created"

        row = baserow_module._find_one("clients", "slug", slug)
        assert row is not None, "Baserow client row not created"
        assert row["name"] == "Test Cliente SA"

        # Idempotency: re-run refuses to overwrite folder (existing behavior),
        # so we cannot fire new-client.sh twice. Instead verify only one row
        # exists in Baserow for this slug (i.e., the first invocation didn't
        # somehow duplicate). Use the same filter syntax baserow.py uses —
        # filter__<name>__equal, NOT filter__field_<name>__equal which silently
        # returns unfiltered results.
        tid = baserow_module._table_id("clients")
        path = (f"/api/database/rows/table/{tid}/?user_field_names=true"
                f"&filter__slug__equal={slug}")
        resp = baserow_module._request("GET", path)
        assert len(resp.get("results", [])) == 1, (
            f"expected 1 row for slug={slug!r}, got "
            f"{len(resp.get('results', []))}")
    finally:
        if folder.exists():
            shutil.rmtree(folder)
