import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0054"), None)
    if not inv:
        return False, "Invoice INV-0054 not found."
    li = next((l for l in inv["lineItems"] if l["description"] == "Staff training workshop - 2 days"), None)
    if not li:
        return False, "Line item 'Staff training workshop - 2 days' not found."
    if li["taxRateId"] != "tax_3":
        return False, f"Expected tax rate 'tax_3' (No GST), got '{li['taxRateId']}'"
    return True, "Tax rate of 'Staff training workshop - 2 days' on INV-0054 changed to No GST correctly."
