"""Integration: skills/shared/baserow.py round-trip against live Baserow.

Requires BASEROW_URL + BASEROW_API_TOKEN in env (set by run-with-secrets.sh).
Leaves residue rows in Baserow — Stage 1 acceptable; cleanup deferred.
"""
import os
import sys
import time

import pytest

NEXOSTRAT = os.environ.get("NEXOSTRAT", "/srv/Nexostrat")
sys.path.insert(0, f"{NEXOSTRAT}/skills/shared")


pytestmark = pytest.mark.skipif(
    not (os.environ.get("BASEROW_URL") and os.environ.get("BASEROW_API_TOKEN")),
    reason="BASEROW_URL and BASEROW_API_TOKEN required (run under run-with-secrets.sh)",
)


@pytest.fixture
def br():
    import baserow
    baserow._TABLE_ID_CACHE.clear()
    return baserow


def test_post_client_round_trip(br):
    slug = f"_test_integration_{int(time.time())}"
    first = br.post_client(
        slug=slug, name=f"Integration {slug}", display_name="Integration Test",
        country="CO", sector="test", pilot=True, source="outbound",
    )
    assert first is not None, "first post_client returned None"

    second = br.post_client(
        slug=slug, name=f"Integration {slug}", display_name="Integration Test",
        country="CO", sector="test", pilot=True, source="outbound",
    )
    assert second == first, f"idempotent post_client returned {second} != {first}"


def test_post_deliverable_round_trip(br):
    slug = f"_test_deliverable_{int(time.time())}"
    client_id = br.post_client(
        slug=slug, name=f"Deliverable host {slug}", display_name="Deliverable Host",
        country="CO", sector="test", pilot=True, source="outbound",
    )
    assert client_id is not None

    file_md = f"/tmp/_test_{slug}.md"
    first = br.post_deliverable(
        client_id=client_id, skill="company-analyst",
        file_md=file_md, file_docx=f"/tmp/_test_{slug}.docx",
        file_pdf=f"/tmp/_test_{slug}.pdf",
    )
    assert first is not None, "first post_deliverable returned None"

    second = br.post_deliverable(
        client_id=client_id, skill="company-analyst",
        file_md=file_md, file_docx=f"/tmp/_test_{slug}.docx",
        file_pdf=f"/tmp/_test_{slug}.pdf",
    )
    assert second == first, f"dedupe by file_md returned {second} != {first}"
