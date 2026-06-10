import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # INV-0049 (Coastal Living) contains USB-C Cable 2m line items
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0049"), None)
    if inv is None:
        return False, "INV-0049 not found."

    if inv.get("status") != "voided":
        return False, f"Expected INV-0049 status 'voided', got '{inv.get('status')}'."

    return True, "INV-0049 (containing USB-C cables) voided successfully."
