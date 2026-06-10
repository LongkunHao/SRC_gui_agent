import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0052"), None)
    if not inv:
        return False, "Invoice INV-0052 not found."

    if inv["title"] != "March 2026 Development Sprint":
        return False, f"Invoice INV-0052 title is '{inv['title']}', expected 'March 2026 Development Sprint'."

    return True, "Invoice INV-0052 title updated to 'March 2026 Development Sprint'."
