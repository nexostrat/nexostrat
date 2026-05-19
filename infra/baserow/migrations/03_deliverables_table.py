"""Create the `deliverables` table per spec §4.3."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    clients_tid = get_or_create_table(db, "clients")
    tid = get_or_create_table(db, "deliverables")

    add_field(tid, {"name": "client", "type": "link_row",
                    "link_row_table_id": clients_tid})
    add_field(tid, {"name": "skill", "type": "single_select",
                    "select_options": [
                        {"value": "company-analyst", "color": "blue"},
                        {"value": "industry-analyst", "color": "cyan"},
                        {"value": "competitor-analyst", "color": "purple"},
                        {"value": "discovery-meeting", "color": "yellow"},
                        {"value": "opportunity-report", "color": "green"}
                    ]})
    add_field(tid, {"name": "file_md", "type": "text"})
    add_field(tid, {"name": "file_docx", "type": "text"})
    add_field(tid, {"name": "file_pdf", "type": "text"})
    add_field(tid, {"name": "status", "type": "single_select",
                    "select_options": [
                        {"value": "draft", "color": "gray"},
                        {"value": "internal_review", "color": "yellow"},
                        {"value": "delivered", "color": "green"},
                        {"value": "revised", "color": "orange"}
                    ]})
    add_field(tid, {"name": "created_at", "type": "created_on"})
    add_field(tid, {"name": "delivered_at", "type": "date",
                    "date_format": "ISO", "date_include_time": False})
    add_field(tid, {"name": "delivered_via", "type": "single_select",
                    "select_options": [
                        {"value": "email", "color": "blue"},
                        {"value": "whatsapp", "color": "green"},
                        {"value": "in_person", "color": "purple"},
                        {"value": "not_yet", "color": "gray"}
                    ]})

    print(f"deliverables table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
