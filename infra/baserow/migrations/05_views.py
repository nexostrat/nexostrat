"""Create predefined views per spec §4.5 (11 views across 4 tables)."""
from _api import get, post, get_or_create_workspace, get_or_create_database


def _table_id(database_id: int, name: str) -> int:
    tables = get(f"/api/database/tables/database/{database_id}/")
    for t in tables:
        if t["name"] == name:
            return t["id"]
    raise RuntimeError(f"table not found: {name}")


def _field_id(table_id: int, name: str) -> int:
    fields = get(f"/api/database/fields/table/{table_id}/")
    for f in fields:
        if f["name"] == name:
            return f["id"]
    raise RuntimeError(f"field not found in table {table_id}: {name}")


def _ensure_view(table_id, view_name, view_type, filters=None, sortings=None):
    existing = get(f"/api/database/views/table/{table_id}/")
    for v in existing:
        if v["name"] == view_name:
            view_id = v["id"]
            # Orphan recovery: a previous run may have created the view but
            # crashed before its filters/sortings landed (e.g., a wrong filter
            # type returns HTTP 400 after view creation). If the desired
            # spec has filters/sortings but the live view has none, attach
            # them now. We don't try to diff-and-update existing filters —
            # that path is for a future migration runner.
            if filters:
                live_filters = get(f"/api/database/views/{view_id}/filters/")
                live_count = len(live_filters.get("results", live_filters)
                                 if isinstance(live_filters, dict)
                                 else live_filters)
                if live_count == 0:
                    for flt in filters:
                        post(f"/api/database/views/{view_id}/filters/", flt)
                    print(f"  VIEW PATCHED: {view_name} "
                          f"(added {len(filters)} filter(s))")
                    if sortings:
                        for srt in sortings:
                            post(f"/api/database/views/{view_id}/sortings/", srt)
                    return view_id
            print(f"  VIEW EXISTS: {view_name}")
            return view_id
    result = post(
        f"/api/database/views/table/{table_id}/",
        {"name": view_name, "type": view_type,
         "filter_type": "AND", "filters_disabled": False},
    )
    view_id = result["id"]
    for flt in (filters or []):
        post(f"/api/database/views/{view_id}/filters/", flt)
    for srt in (sortings or []):
        post(f"/api/database/views/{view_id}/sortings/", srt)
    print(f"  VIEW CREATED: {view_name}")
    return view_id


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")

    clients_tid = _table_id(db, "clients")
    meetings_tid = _table_id(db, "meetings")
    deliverables_tid = _table_id(db, "deliverables")
    financials_tid = _table_id(db, "financials")

    # clients
    phase_fid = _field_id(clients_tid, "phase")
    pilot_fid = _field_id(clients_tid, "pilot")
    print("clients views:")
    _ensure_view(clients_tid, "Pipeline activo", "grid",
                 filters=[{"field": phase_fid, "type": "single_select_not_equal",
                           "value": "dormant"}])
    _ensure_view(clients_tid, "Pilotos", "grid",
                 filters=[{"field": pilot_fid, "type": "boolean",
                           "value": "true"}])
    _ensure_view(clients_tid, "Por país", "grid")

    # meetings
    date_fid = _field_id(meetings_tid, "date")
    mstatus_fid = _field_id(meetings_tid, "status")
    print("meetings views:")
    _ensure_view(meetings_tid, "Próximas", "grid",
                 filters=[{"field": date_fid, "type": "date_after_today",
                           "value": ""}],
                 sortings=[{"field": date_fid, "order": "ASC"}])
    _ensure_view(meetings_tid, "Esta semana", "grid",
                 filters=[{"field": date_fid, "type": "date_within_days",
                           "value": "7"}])
    _ensure_view(meetings_tid, "Pendientes de transcripción", "grid",
                 filters=[{"field": mstatus_fid, "type": "single_select_equal",
                           "value": "recorded"}])

    # deliverables
    created_fid = _field_id(deliverables_tid, "created_at")
    dstatus_fid = _field_id(deliverables_tid, "status")
    print("deliverables views:")
    _ensure_view(deliverables_tid, "Esta semana", "grid",
                 filters=[{"field": created_fid, "type": "date_within_days",
                           "value": "7"}])
    _ensure_view(deliverables_tid, "En revisión interna", "grid",
                 filters=[{"field": dstatus_fid, "type": "single_select_equal",
                           "value": "internal_review"}])
    _ensure_view(deliverables_tid, "Por skill", "grid")

    # financials
    fdate_fid = _field_id(financials_tid, "date")
    fkind_fid = _field_id(financials_tid, "kind")
    fstatus_fid = _field_id(financials_tid, "status")
    print("financials views:")
    _ensure_view(financials_tid, "Mes en curso", "grid",
                 filters=[{"field": fdate_fid, "type": "date_within_days",
                           "value": "30"}])
    _ensure_view(financials_tid, "Por cobrar", "grid",
                 filters=[{"field": fkind_fid, "type": "single_select_equal",
                           "value": "income"},
                          {"field": fstatus_fid, "type": "single_select_equal",
                           "value": "pending"}])

    print("views ready")


if __name__ == "__main__":
    run()
