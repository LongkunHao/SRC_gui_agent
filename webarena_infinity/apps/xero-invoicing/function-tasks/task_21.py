import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check that quote QU-0022 is marked as invoiced
    quo = next((q for q in state["quotes"] if q["number"] == "QU-0022"), None)
    if not quo:
        return False, "Quote QU-0022 not found."

    if not quo.get("isInvoiced"):
        return False, "Quote QU-0022 is not marked as invoiced."

    # Check that a new invoice was created
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0067"), None)
    if not inv:
        return False, "New invoice INV-0067 not found (expected from quote conversion)."

    if inv["status"] != "draft":
        return False, f"New invoice status is '{inv['status']}', expected 'draft'."

    if inv["contactId"] != quo["contactId"]:
        return False, f"New invoice contactId '{inv['contactId']}' doesn't match quote contactId '{quo['contactId']}'."

    if len(inv["lineItems"]) != len(quo["lineItems"]):
        return False, f"New invoice has {len(inv['lineItems'])} line items, expected {len(quo['lineItems'])}."

    return True, "Invoice INV-0067 created from quote QU-0022, quote marked as invoiced."
