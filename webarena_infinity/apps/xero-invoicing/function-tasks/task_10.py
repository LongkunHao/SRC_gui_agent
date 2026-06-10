import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0067"), None)
    if not inv:
        return False, "New invoice INV-0067 not found."

    if inv["status"] != "draft":
        return False, f"Invoice status is '{inv['status']}', expected 'draft'."

    contact = next((c for c in state["contacts"] if c["name"] == "TechVault Solutions Pty Ltd"), None)
    if not contact:
        return False, "Contact 'TechVault Solutions Pty Ltd' not found."

    if inv["contactId"] != contact["id"]:
        return False, f"Invoice contactId is '{inv['contactId']}', expected '{contact['id']}'."

    if len(inv["lineItems"]) < 1:
        return False, "Invoice has no line items."

    li = inv["lineItems"][0]
    if li["quantity"] != 10:
        return False, f"Line item quantity is {li['quantity']}, expected 10."

    if abs(li["unitPrice"] - 185.00) > 0.01:
        return False, f"Line item unit price is {li['unitPrice']}, expected 185.00."

    return True, "New invoice INV-0067 created for TechVault Solutions with 10x DEV-HOUR."
