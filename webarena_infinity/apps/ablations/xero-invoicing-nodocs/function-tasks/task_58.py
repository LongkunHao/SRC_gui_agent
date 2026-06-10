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

    con = next((c for c in state["contacts"] if c["name"] == "Atlas Import/Export Ltd"), None)
    if not con:
        return False, "Contact 'Atlas Import/Export Ltd' not found."
    if inv["contactId"] != con["id"]:
        return False, f"Wrong contact: expected {con['id']}, got {inv['contactId']}"
    if inv["status"] != "draft":
        return False, f"Expected status 'draft', got '{inv['status']}'"
    if inv["issueDate"] != "2026-01-15":
        return False, f"Expected issue date '2026-01-15', got '{inv['issueDate']}'"
    if inv["dueDate"] != "2026-02-15":
        return False, f"Expected due date '2026-02-15', got '{inv['dueDate']}'"

    li = next((l for l in inv["lineItems"] if l["description"] == "Freight and logistics services"), None)
    if not li:
        return False, "Line item 'Freight and logistics services' not found."
    if li["quantity"] != 10 or li["unitPrice"] != 85:
        return False, f"Expected qty 10 @ $85, got qty {li['quantity']} @ ${li['unitPrice']}"

    return True, "Draft invoice for Atlas Import/Export Ltd with specific dates created correctly."
