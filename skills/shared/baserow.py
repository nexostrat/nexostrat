"""Baserow row-CRUD helper for skills.

Auth: Database API Token (Authorization: Token <token>) — row-scope.
Distinct from infra/baserow/migrations/_api.py which uses JWT for schema ops.

Public surface (all decorated with @_safe — never raise, return None on error):
    post_client(slug, name, display_name, country, sector, pilot, source, **kw) -> int|None
    post_meeting(client_id, date, kind, **kw) -> int|None
    post_deliverable(client_id, skill, file_md, file_docx, file_pdf, **kw) -> int|None
    update_status(table, row_id, status) -> bool|None

Reads BASEROW_URL + BASEROW_API_TOKEN from env (sourced by run-with-secrets.sh).
"""
import functools
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


def _log(msg: str) -> None:
    print(f"[baserow] {msg}", file=sys.stderr)


def _ctx() -> ssl.SSLContext:
    c = ssl.create_default_context()
    if os.environ.get("BASEROW_INSECURE_TLS", "1") == "1":
        c.check_hostname = False
        c.verify_mode = ssl.CERT_NONE
    return c


def _request(method: str, path: str, body: dict | None = None) -> dict:
    base = os.environ.get("BASEROW_URL")
    token = os.environ.get("BASEROW_API_TOKEN")
    if not base or not token:
        raise RuntimeError("BASEROW_URL and BASEROW_API_TOKEN must be set")
    url = f"{base}{path}"
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Token {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=15) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {err_body}") from e


# In-process cache so the workspaces → applications → tables walk runs once
# per table name per process. Tests must clear this between cases.
_TABLE_ID_CACHE: dict[str, int] = {}


def _table_id(name: str) -> int:
    """Resolve table name to id.

    Database API Tokens can only call /api/database/rows/... endpoints — they
    return 401 on /api/workspaces/, /api/applications/, and the tables-list
    endpoints. So the helper reads table IDs from env vars
    (BASEROW_TABLE_<NAME>_ID) seeded by infra/scripts/write-baserow-table-ids.sh.
    """
    if name in _TABLE_ID_CACHE:
        return _TABLE_ID_CACHE[name]
    env_key = f"BASEROW_TABLE_{name.upper()}_ID"
    if env_key in os.environ:
        tid = int(os.environ[env_key])
        _TABLE_ID_CACHE[name] = tid
        return tid
    raise RuntimeError(
        f"table id missing: set {env_key} in secrets.env.age via "
        f"infra/scripts/write-baserow-table-ids.sh, or pre-populate "
        f"_TABLE_ID_CACHE in a test fixture")


def _find_one(table: str, field: str, value) -> dict | None:
    """Return first row where `field == value`, or None.

    With user_field_names=true, the filter param uses the field NAME directly
    (filter__<name>__equal=). The old `field_<name>` form is for field-id
    addressing and silently no-ops here (Baserow returns unfiltered results
    instead of erroring), so getting this wrong is dangerously quiet.
    """
    tid = _table_id(table)
    encoded = urllib.parse.quote(str(value), safe="")
    path = (f"/api/database/rows/table/{tid}/?user_field_names=true"
            f"&filter__{field}__equal={encoded}&size=1")
    result = _request("GET", path)
    rows = result.get("results", [])
    return rows[0] if rows else None


def _insert(table: str, fields: dict) -> dict:
    tid = _table_id(table)
    return _request(
        "POST",
        f"/api/database/rows/table/{tid}/?user_field_names=true",
        fields,
    )


def _update(table: str, row_id: int, fields: dict) -> dict:
    tid = _table_id(table)
    return _request(
        "PATCH",
        f"/api/database/rows/table/{tid}/{row_id}/?user_field_names=true",
        fields,
    )


def _safe(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            _log(f"{fn.__name__} failed: {exc}")
            return None
    return wrapper


_CLIENT_OPTIONAL = (
    "rfc_nit", "decisor_name", "decisor_role",
    "contact_name", "contact_phone", "contact_email",
)
_MEETING_OPTIONAL = (
    "location", "attendees_text", "recording_path",
    "transcript_path", "notes_path", "duration_min",
)
_DELIVERABLE_OPTIONAL = ("delivered_at", "delivered_via")


@_safe
def post_client(slug, name, display_name, country, sector, pilot, source, **kwargs) -> int | None:
    existing = _find_one("clients", "slug", slug)
    if existing:
        _log(f"client slug={slug!r} exists (id={existing['id']}) — skipping insert")
        return existing["id"]
    fields = {
        "slug": slug,
        "name": name,
        "display_name": display_name,
        "country": country,
        "sector": sector,
        "pilot": pilot,
        "source": source,
        "phase": kwargs.get("phase", "prospect"),
    }
    for k in _CLIENT_OPTIONAL:
        if k in kwargs:
            fields[k] = kwargs[k]
    row = _insert("clients", fields)
    return row["id"]


@_safe
def post_meeting(client_id, date, kind, **kwargs) -> int | None:
    fields = {
        "client": [client_id],
        "date": date,
        "kind": kind,
        "status": kwargs.get("status", "planned"),
    }
    for k in _MEETING_OPTIONAL:
        if k in kwargs:
            fields[k] = kwargs[k]
    row = _insert("meetings", fields)
    return row["id"]


@_safe
def post_deliverable(client_id, skill, file_md, file_docx, file_pdf, **kwargs) -> int | None:
    existing = _find_one("deliverables", "file_md", file_md)
    fields = {
        "client": [client_id],
        "skill": skill,
        "file_md": file_md,
        "file_docx": file_docx,
        "file_pdf": file_pdf,
        "status": kwargs.get("status", "draft"),
    }
    for k in _DELIVERABLE_OPTIONAL:
        if k in kwargs:
            fields[k] = kwargs[k]
    if existing:
        row = _update("deliverables", existing["id"], fields)
        return row["id"]
    row = _insert("deliverables", fields)
    return row["id"]


@_safe
def update_status(table, row_id, status) -> bool:
    _update(table, row_id, {"status": status})
    return True
