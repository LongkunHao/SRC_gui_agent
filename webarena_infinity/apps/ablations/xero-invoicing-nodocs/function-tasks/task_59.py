import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0011"), None)
    if not inv:
        return False, "Invoice INV-0011 not found."
    if inv["status"] != "awaiting_payment":
        return False, f"Expected status 'awaiting_payment', got '{inv['status']}'"
    if not inv.get("sentAt"):
        return False, "sentAt is null — invoice was not sent."
    sent_activities = [a for a in inv.get("activity", []) if a.get("type") == "sent"]
    if len(sent_activities) < 2:
        return False, f"Expected at least 2 'sent' activity entries (seed + agent send), found {len(sent_activities)}."
    return True, "Invoice INV-0011 sent successfully."
