import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    cn = next((c for c in state["creditNotes"] if c["number"] == "CN-0013"), None)
    if not cn:
        return False, "New credit note CN-0013 not found."

    if cn["status"] != "awaiting_payment":
        return False, f"Credit note status is '{cn['status']}', expected 'awaiting_payment' (approved)."

    contact = next((c for c in state["contacts"] if c["name"] == "TechVault Solutions Pty Ltd"), None)
    if not contact:
        return False, "Contact 'TechVault Solutions Pty Ltd' not found."

    if cn["contactId"] != contact["id"]:
        return False, f"Credit note contactId is '{cn['contactId']}', expected '{contact['id']}'."

    if len(cn["lineItems"]) < 1:
        return False, "Credit note has no line items."

    li = cn["lineItems"][0]
    if li["quantity"] != 4:
        return False, f"Line item quantity is {li['quantity']}, expected 4."

    if abs(li["unitPrice"] - 25.00) > 0.01:
        return False, f"Line item unit price is {li['unitPrice']}, expected 25.00."

    return True, "New credit note CN-0013 created for TechVault and approved."
