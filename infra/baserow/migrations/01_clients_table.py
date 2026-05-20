"""Create the `clients` table per spec §4.1."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    tid = get_or_create_table(db, "clients")

    add_field(tid, {"name": "slug", "type": "text"})
    add_field(tid, {"name": "name", "type": "text"})
    add_field(tid, {"name": "display_name", "type": "text"})
    add_field(tid, {"name": "country", "type": "single_select",
                    "select_options": [{"value": "CO", "color": "blue"},
                                       {"value": "MX", "color": "green"}]})
    add_field(tid, {"name": "rfc_nit", "type": "text"})
    add_field(tid, {"name": "sector", "type": "text"})
    add_field(tid, {"name": "phase", "type": "single_select",
                    "select_options": [
                        {"value": "prospect", "color": "gray"},
                        {"value": "intake", "color": "blue"},
                        {"value": "diagnostico_in_progress", "color": "yellow"},
                        {"value": "diagnostico_delivered", "color": "cyan"},
                        {"value": "roadmap_offered", "color": "orange"},
                        {"value": "roadmap_in_progress", "color": "red"},
                        {"value": "retainer_active", "color": "green"},
                        {"value": "dormant", "color": "dark-gray"}
                    ]})
    add_field(tid, {"name": "pilot", "type": "boolean"})
    add_field(tid, {"name": "source", "type": "single_select",
                    "select_options": [
                        {"value": "inbound", "color": "blue"},
                        {"value": "outbound", "color": "orange"},
                        {"value": "referido", "color": "green"},
                        {"value": "marketing", "color": "purple"},
                        {"value": "manual", "color": "gray"}
                    ]})
    add_field(tid, {"name": "decisor_name", "type": "text"})
    add_field(tid, {"name": "decisor_role", "type": "text"})
    add_field(tid, {"name": "contact_name", "type": "text"})
    add_field(tid, {"name": "contact_phone", "type": "text"})
    add_field(tid, {"name": "contact_email", "type": "email"})
    add_field(tid, {"name": "folder_path", "type": "formula",
                    "formula": "concat('pipeline/clients/', field('slug'), '/')"})
    add_field(tid, {"name": "created_at", "type": "created_on"})
    add_field(tid, {"name": "updated_at", "type": "last_modified"})

    print(f"clients table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
