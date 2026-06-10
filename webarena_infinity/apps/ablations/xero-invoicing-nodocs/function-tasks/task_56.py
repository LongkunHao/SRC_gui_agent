import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    original_ids = {f"inv_{i}" for i in range(1, 114)}
    new_invs = [i for i in state["invoices"] if i["id"] not in original_ids]
    if not new_invs:
        return False, "No new invoice found."
    inv = new_invs[0]

    con = next((c for c in state["contacts"] if c["name"] == "Ironclad Security Systems"), None)
    if not con:
        return False, "Contact 'Ironclad Security Systems' not found."
    if inv["contactId"] != con["id"]:
        return False, f"Wrong contact: expected {con['id']}, got {inv['contactId']}"
    if inv["status"] != "draft":
        return False, f"Expected status 'draft', got '{inv['status']}'"
    if inv["currency"] != "GBP":
        return False, f"Expected currency 'GBP', got '{inv['currency']}'"
    if len(inv["lineItems"]) != 3:
        return False, f"Expected 3 line items, got {len(inv['lineItems'])}"

    li1 = next((l for l in inv["lineItems"] if l["description"] == "Database optimization"), None)
    if not li1:
        return False, "Line item 'Database optimization' not found."
    if li1["quantity"] != 2 or li1["unitPrice"] != 500:
        return False, f"Database optimization: expected qty 2 @ $500, got qty {li1['quantity']} @ ${li1['unitPrice']}"
    if li1["accountCode"] != "280":
        return False, f"Database optimization: expected account 280, got {li1['accountCode']}"

    li2 = next((l for l in inv["lineItems"] if l["description"] == "Software onboarding training"), None)
    if not li2:
        return False, "Line item 'Software onboarding training' not found."
    if li2["quantity"] != 1 or li2["unitPrice"] != 1200:
        return False, f"Software onboarding training: expected qty 1 @ $1200, got qty {li2['quantity']} @ ${li2['unitPrice']}"
    if li2["accountCode"] != "310":
        return False, f"Software onboarding training: expected account 310, got {li2['accountCode']}"

    li3 = next((l for l in inv["lineItems"] if l["description"] == "Help desk support - monthly retainer"), None)
    if not li3:
        return False, "Line item 'Help desk support - monthly retainer' not found."
    if li3["quantity"] != 3 or li3["unitPrice"] != 200:
        return False, f"Help desk support: expected qty 3 @ $200, got qty {li3['quantity']} @ ${li3['unitPrice']}"
    if li3["accountCode"] != "270":
        return False, f"Help desk support: expected account 270, got {li3['accountCode']}"

    return True, "Draft invoice for Ironclad Security Systems in GBP with 3 line items created correctly."
