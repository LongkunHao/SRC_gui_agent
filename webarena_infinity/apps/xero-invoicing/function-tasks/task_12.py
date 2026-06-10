import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0057"), None)
    if not inv:
        return False, "Invoice INV-0057 not found."

    if inv["status"] != "awaiting_payment":
        return False, f"Invoice INV-0057 status is '{inv['status']}', expected 'awaiting_payment'."

    if not inv.get("sentAt"):
        return False, "Invoice INV-0057 sentAt is not set."

    return True, "Invoice INV-0057 marked as sent (status awaiting_payment, sentAt set)."
