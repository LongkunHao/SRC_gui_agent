import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0093"), None)
    if not inv:
        return False, "Invoice INV-0093 not found."
    removed = next((l for l in inv["lineItems"] if l["description"] == "Social media campaign management"), None)
    if removed:
        return False, "Line item 'Social media campaign management' still present — should have been removed."
    if len(inv["lineItems"]) != 3:
        return False, f"Expected 3 line items after removal, got {len(inv['lineItems'])}"
    return True, "Line item 'Social media campaign management' removed from INV-0093 correctly."
