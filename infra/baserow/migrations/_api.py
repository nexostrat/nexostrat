"""Thin Baserow REST client for schema migrations. JWT auth via email+password."""
import os, json, ssl, urllib.request, urllib.error

BASE_URL = os.environ["BASEROW_URL"]
_EMAIL = os.environ["BASEROW_EMAIL"]
_PASSWORD = os.environ["BASEROW_PASSWORD"]

# Caddy local CA — Tailscale-only network is the security boundary.
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

_JWT: str | None = None


def _raw_post(path: str, body: dict, headers: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, context=_CTX, timeout=30) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"POST {path} -> {e.code}: {err_body}") from e


def _login() -> str:
    """POST /api/user/token-auth/ with email+password, return JWT. Module-cached."""
    global _JWT
    if _JWT is not None:
        return _JWT
    result = _raw_post("/api/user/token-auth/",
                       {"email": _EMAIL, "password": _PASSWORD})
    # Baserow returns either {"token": ...} (older) or {"access_token": ...} (newer);
    # prefer access_token if present, fall back to token.
    _JWT = result.get("access_token") or result.get("token")
    if not _JWT:
        raise RuntimeError(f"token-auth response missing token: {result}")
    return _JWT


def _req(method: str, path: str, body: dict | None = None):
    url = f"{BASE_URL}{path}"
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"JWT {_login()}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=_CTX, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {err_body}") from e


def get(path: str): return _req("GET", path)
def post(path: str, body: dict): return _req("POST", path, body)
def patch(path: str, body: dict): return _req("PATCH", path, body)


def get_or_create_workspace(name: str = "Nexostrat") -> int:
    """Returns workspace_id. Idempotent by name."""
    workspaces = get("/api/workspaces/")
    for w in workspaces:
        if w["name"] == name:
            print(f"WORKSPACE EXISTS: {name} (id={w['id']})")
            return w["id"]
    result = post("/api/workspaces/", {"name": name})
    print(f"WORKSPACE CREATED: {name} (id={result['id']})")
    return result["id"]


def get_or_create_database(workspace_id: int, name: str = "nexostrat") -> int:
    """Returns database_id (called 'application' in Baserow API). Idempotent by name."""
    apps = get(f"/api/applications/workspace/{workspace_id}/")
    for app in apps:
        if app["name"] == name and app["type"] == "database":
            print(f"DATABASE EXISTS: {name} (id={app['id']})")
            return app["id"]
    result = post(
        f"/api/applications/workspace/{workspace_id}/",
        {"name": name, "type": "database"}
    )
    print(f"DATABASE CREATED: {name} (id={result['id']})")
    return result["id"]


def get_or_create_table(database_id: int, name: str) -> int:
    """Returns table_id. Idempotent by name. Caller adds fields via add_field().

    Baserow 1.27.2's CreateTableSerializer rejects `data: []` (allow_empty=False)
    but both `data` and `first_row_header` are required=False — omitting them
    creates a truly empty table that we then populate via add_field() calls.
    """
    tables = get(f"/api/database/tables/database/{database_id}/")
    for t in tables:
        if t["name"] == name:
            print(f"TABLE EXISTS: {name} (id={t['id']})")
            return t["id"]
    result = post(
        f"/api/database/tables/database/{database_id}/",
        {"name": name}
    )
    print(f"TABLE CREATED: {name} (id={result['id']})")
    return result["id"]


def get_fields(table_id: int) -> list[dict]:
    return get(f"/api/database/fields/table/{table_id}/")


def add_field(table_id: int, spec: dict) -> int:
    """Returns field_id. Idempotent by spec['name']."""
    existing = {f["name"]: f["id"] for f in get_fields(table_id)}
    if spec["name"] in existing:
        print(f"  FIELD EXISTS: {spec['name']}")
        return existing[spec["name"]]
    result = post(f"/api/database/fields/table/{table_id}/", spec)
    print(f"  FIELD CREATED: {spec['name']} ({spec['type']})")
    return result["id"]
