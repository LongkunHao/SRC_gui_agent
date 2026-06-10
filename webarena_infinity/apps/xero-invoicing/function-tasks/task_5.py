import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0059"), None)
    if not inv:
        return False, "Invoice INV-0059 not found."

    if inv["status"] != "deleted":
        return False, f"Invoice INV-0059 status is '{inv['status']}', expected 'deleted'."

    return True, "Invoice INV-0059 deleted successfully."
