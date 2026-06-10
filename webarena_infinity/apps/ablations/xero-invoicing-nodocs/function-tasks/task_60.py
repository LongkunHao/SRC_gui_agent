import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv4 = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0004"), None)
    if not inv4:
        return False, "Invoice INV-0004 not found."
    if not inv4.get("sentAt"):
        return False, "INV-0004: sentAt is null — invoice was not sent."
    sent4 = [a for a in inv4.get("activity", []) if a.get("type") == "sent"]
    if len(sent4) < 2:
        return False, f"INV-0004: expected at least 2 'sent' activity entries (seed + agent send), found {len(sent4)}."

    inv13 = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0013"), None)
    if not inv13:
        return False, "Invoice INV-0013 not found."
    if not inv13.get("sentAt"):
        return False, "INV-0013: sentAt is null — invoice was not sent."
    sent13 = [a for a in inv13.get("activity", []) if a.get("type") == "sent"]
    if len(sent13) < 2:
        return False, f"INV-0013: expected at least 2 'sent' activity entries (seed + agent send), found {len(sent13)}."

    return True, "Invoices INV-0004 and INV-0013 bulk sent successfully."
