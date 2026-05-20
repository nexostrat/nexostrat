"""Unit tests for skills/shared/baserow.py — _request is mocked, no live HTTP."""
import importlib
import os
import sys
from unittest.mock import patch

import pytest

# Env must be populated before baserow is imported (it reads env at request time,
# but tests assume the module exists in a clean state per test).
os.environ.setdefault("BASEROW_URL", "https://baserow.test")
os.environ.setdefault("BASEROW_API_TOKEN", "dummy")

# Ensure skills/shared/ is importable as a package.
_SHARED = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

import baserow  # noqa: E402


# _table_id walks workspaces → apps → tables. When the cache is empty, a single
# call to a public function fires THREE _request calls for the walk (workspaces,
# applications/workspace/{wid}, tables/database/{aid}) before any CRUD call. We
# either consume those three or pre-populate _TABLE_ID_CACHE to skip the walk.


@pytest.fixture(autouse=True)
def _clear_cache():
    baserow._TABLE_ID_CACHE.clear()
    yield
    baserow._TABLE_ID_CACHE.clear()


_WORKSPACE_PAYLOAD = [{"id": 1, "name": "Nexostrat"}]
_APP_PAYLOAD = [{"id": 10, "name": "nexostrat", "type": "database"}]
_TABLES_PAYLOAD = [
    {"id": 571, "name": "clients"},
    {"id": 572, "name": "meetings"},
    {"id": 573, "name": "deliverables"},
    {"id": 574, "name": "financials"},
]


def test_post_client_new():
    """Cold cache: 3 walk calls + find_one (empty) + insert. Returns new id."""
    with patch.object(baserow, "_request") as mock_req:
        mock_req.side_effect = [
            _WORKSPACE_PAYLOAD,
            _APP_PAYLOAD,
            _TABLES_PAYLOAD,
            {"results": []},               # _find_one — no existing slug
            {"id": 42, "slug": "trixx"},   # _insert
        ]
        result = baserow.post_client(
            slug="trixx", name="Trixx Corp", display_name="Trixx",
            country="CO", sector="tech", pilot=False, source="outbound",
        )
    assert result == 42
    # Last call is the POST insert
    last_call = mock_req.call_args_list[-1]
    assert last_call.args[0] == "POST"
    assert "/api/database/rows/table/571/" in last_call.args[1]


def test_post_client_idempotent():
    """Cache pre-populated — _table_id short-circuits; only _find_one fires."""
    baserow._TABLE_ID_CACHE["clients"] = 571
    with patch.object(baserow, "_request") as mock_req:
        mock_req.side_effect = [
            {"results": [{"id": 99, "slug": "trixx"}]},
        ]
        result = baserow.post_client(
            slug="trixx", name="Trixx Corp", display_name="Trixx",
            country="CO", sector="tech", pilot=False, source="outbound",
        )
    assert result == 99
    # Exactly one call: the find_one query. No insert.
    assert mock_req.call_count == 1
    assert mock_req.call_args.args[0] == "GET"


def test_post_deliverable_new():
    """Cache pre-populated; find_one empty → POST."""
    baserow._TABLE_ID_CACHE["deliverables"] = 573
    with patch.object(baserow, "_request") as mock_req:
        mock_req.side_effect = [
            {"results": []},                # find_one — no existing file_md
            {"id": 7, "file_md": "x.md"},   # insert
        ]
        result = baserow.post_deliverable(
            client_id=42, skill="company-analyst",
            file_md="x.md", file_docx="x.docx", file_pdf="x.pdf",
        )
    assert result == 7
    methods = [c.args[0] for c in mock_req.call_args_list]
    assert methods == ["GET", "POST"]


def test_post_deliverable_dedupe():
    """Existing file_md → PATCH (update) not POST. Returns same id."""
    baserow._TABLE_ID_CACHE["deliverables"] = 573
    with patch.object(baserow, "_request") as mock_req:
        mock_req.side_effect = [
            {"results": [{"id": 7, "file_md": "x.md"}]},   # find_one — exists
            {"id": 7, "file_md": "x.md"},                  # update
        ]
        result = baserow.post_deliverable(
            client_id=42, skill="company-analyst",
            file_md="x.md", file_docx="x.docx", file_pdf="x.pdf",
        )
    assert result == 7
    methods = [c.args[0] for c in mock_req.call_args_list]
    assert methods == ["GET", "PATCH"]


def test_network_error_does_not_crash():
    """ConnectionError inside _request is swallowed by @_safe → returns None."""
    baserow._TABLE_ID_CACHE["deliverables"] = 573
    with patch.object(baserow, "_request") as mock_req:
        mock_req.side_effect = ConnectionError("boom")
        result = baserow.post_deliverable(
            client_id=42, skill="company-analyst",
            file_md="x.md", file_docx="x.docx", file_pdf="x.pdf",
        )
    assert result is None
