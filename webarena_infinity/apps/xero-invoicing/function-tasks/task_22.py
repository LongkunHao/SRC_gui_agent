import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    quo = next((q for q in state["quotes"] if q["number"] == "QU-0030"), None)
    if not quo:
        return False, "New quote QU-0030 not found."

    if quo["status"] != "draft":
        return False, f"Quote status is '{quo['status']}', expected 'draft'."

    contact = next((c for c in state["contacts"] if c["name"] == "Southern Cross Veterinary"), None)
    if not contact:
        return False, "Contact 'Southern Cross Veterinary' not found."

    if quo["contactId"] != contact["id"]:
        return False, f"Quote contactId is '{quo['contactId']}', expected '{contact['id']}'."

    if len(quo["lineItems"]) < 1:
        return False, "Quote has no line items."

    li = quo["lineItems"][0]
    if li["quantity"] != 8:
        return False, f"Line item quantity is {li['quantity']}, expected 8."

    if abs(li["unitPrice"] - 250.00) > 0.01:
        return False, f"Line item unit price is {li['unitPrice']}, expected 250.00."

    return True, "New quote QU-0030 created for Southern Cross Veterinary with 8x CONSULT-HR."
