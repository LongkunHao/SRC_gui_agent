import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0025"), None)
    if not inv:
        return False, "Invoice INV-0025 not found."
    li = next((l for l in inv["lineItems"] if l["description"] == "Network security audit"), None)
    if not li:
        return False, "Line item 'Network security audit' not found."
    if li["unitPrice"] != 150:
        return False, f"Expected unit price 150, got {li['unitPrice']}"
    expected_total = 1 * 150  # qty=1
    if abs(li["lineTotal"] - expected_total) > 0.01:
        return False, f"Expected lineTotal {expected_total}, got {li['lineTotal']}"
    return True, "Unit price of 'Network security audit' on INV-0025 changed to $150 correctly."
