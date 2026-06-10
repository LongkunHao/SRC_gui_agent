import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0054"), None)
    if not inv:
        return False, "Invoice INV-0054 not found."

    if inv["status"] != "voided":
        return False, f"Invoice INV-0054 status is '{inv['status']}', expected 'voided'."

    if inv["amountDue"] != 0:
        return False, f"Invoice INV-0054 amountDue is {inv['amountDue']}, expected 0."

    return True, "Invoice INV-0054 voided successfully."
