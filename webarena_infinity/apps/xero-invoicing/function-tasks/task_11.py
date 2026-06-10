import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0058"), None)
    if not inv:
        return False, "Invoice INV-0058 not found."

    if inv["reference"] != "MRW-WEB-MARCH":
        return False, f"Invoice INV-0058 reference is '{inv['reference']}', expected 'MRW-WEB-MARCH'."

    return True, "Invoice INV-0058 reference updated to 'MRW-WEB-MARCH'."
