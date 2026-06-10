import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    cn = next((c for c in state["creditNotes"] if c["number"] == "CN-0013"), None)
    if not cn:
        return False, "New credit note CN-0013 not found."

    if cn["status"] != "draft":
        return False, f"Credit note status is '{cn['status']}', expected 'draft'."

    contact = next((c for c in state["contacts"] if c["name"] == "Greenfield Organics"), None)
    if not contact:
        return False, "Contact 'Greenfield Organics' not found."

    if cn["contactId"] != contact["id"]:
        return False, f"Credit note contactId is '{cn['contactId']}', expected '{contact['id']}'."

    if len(cn["lineItems"]) < 1:
        return False, "Credit note has no line items."

    li = cn["lineItems"][0]
    if abs(li["unitPrice"] - 100.00) > 0.01:
        return False, f"Line item unit price is {li['unitPrice']}, expected 100.00."

    return True, "New credit note CN-0013 created for Greenfield Organics."
