import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0061"), None)
    if not inv:
        return False, "Invoice INV-0061 not found."
    if inv["reference"] != "WO-12400":
        return False, f"Expected reference 'WO-12400', got '{inv['reference']}'"
    if inv["notes"] != "Urgent delivery required.":
        return False, f"Expected notes 'Urgent delivery required.', got '{inv['notes']}'"
    return True, "Reference and notes of INV-0061 updated correctly."
