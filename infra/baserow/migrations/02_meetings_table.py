"""Create the `meetings` table per spec §4.2."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    clients_tid = get_or_create_table(db, "clients")  # ensure clients exists for link
    tid = get_or_create_table(db, "meetings")

    add_field(tid, {"name": "client", "type": "link_row",
                    "link_row_table_id": clients_tid})
    add_field(tid, {"name": "date", "type": "date",
                    "date_format": "ISO", "date_include_time": True,
                    "date_time_format": "24"})
    add_field(tid, {"name": "location", "type": "text"})
    add_field(tid, {"name": "kind", "type": "single_select",
                    "select_options": [
                        {"value": "discovery", "color": "blue"},
                        {"value": "feedback", "color": "cyan"},
                        {"value": "roadmap_kickoff", "color": "orange"},
                        {"value": "check_in", "color": "yellow"},
                        {"value": "internal_r_jp", "color": "purple"}
                    ]})
    add_field(tid, {"name": "attendees_text", "type": "long_text"})
    add_field(tid, {"name": "status", "type": "single_select",
                    "select_options": [
                        {"value": "planned", "color": "gray"},
                        {"value": "confirmed", "color": "blue"},
                        {"value": "recorded", "color": "yellow"},
                        {"value": "transcribed", "color": "cyan"},
                        {"value": "extracted", "color": "green"},
                        {"value": "cancelled", "color": "red"}
                    ]})
    add_field(tid, {"name": "recording_path", "type": "text"})
    add_field(tid, {"name": "transcript_path", "type": "text"})
    add_field(tid, {"name": "notes_path", "type": "text"})
    add_field(tid, {"name": "duration_min", "type": "number",
                    "number_decimal_places": 0})
    add_field(tid, {"name": "created_at", "type": "created_on"})

    print(f"meetings table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
