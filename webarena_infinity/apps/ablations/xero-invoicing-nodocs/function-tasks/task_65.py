import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0082"), None)
    if not inv:
        return False, "Invoice INV-0082 not found."
    li = next((l for l in inv["lineItems"] if l["description"] == "IT infrastructure assessment"), None)
    if not li:
        return False, "Line item 'IT infrastructure assessment' not found."
    if li["quantity"] != 50:
        return False, f"Expected quantity 50, got {li['quantity']}"
    expected_total = 50 * 1000
    if abs(li["lineTotal"] - expected_total) > 0.01:
        return False, f"Expected lineTotal {expected_total}, got {li['lineTotal']}"
    return True, "Quantity of 'IT infrastructure assessment' on INV-0082 changed to 50 correctly."
