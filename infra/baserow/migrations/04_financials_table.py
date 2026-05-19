"""Create the `financials` table per spec §4.4."""
from _api import (get_or_create_workspace, get_or_create_database,
                  get_or_create_table, add_field)


def run():
    ws = get_or_create_workspace("Nexostrat")
    db = get_or_create_database(ws, "nexostrat")
    clients_tid = get_or_create_table(db, "clients")
    tid = get_or_create_table(db, "financials")

    add_field(tid, {"name": "client", "type": "link_row",
                    "link_row_table_id": clients_tid})
    add_field(tid, {"name": "kind", "type": "single_select",
                    "select_options": [
                        {"value": "income", "color": "green"},
                        {"value": "expense", "color": "red"}
                    ]})
    add_field(tid, {"name": "amount", "type": "number",
                    "number_decimal_places": 2})
    add_field(tid, {"name": "currency", "type": "single_select",
                    "select_options": [
                        {"value": "MXN", "color": "green"},
                        {"value": "COP", "color": "yellow"},
                        {"value": "USD", "color": "blue"}
                    ]})
    add_field(tid, {"name": "date", "type": "date",
                    "date_format": "ISO", "date_include_time": False})
    add_field(tid, {"name": "status", "type": "single_select",
                    "select_options": [
                        {"value": "pending", "color": "gray"},
                        {"value": "received", "color": "green"},
                        {"value": "paid", "color": "blue"},
                        {"value": "cancelled", "color": "red"}
                    ]})
    add_field(tid, {"name": "description", "type": "text"})
    add_field(tid, {"name": "invoice_path", "type": "text"})

    print(f"financials table ready (id={tid})")
    return tid


if __name__ == "__main__":
    run()
