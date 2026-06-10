import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    orig = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0007"), None)
    if not orig:
        return False, "Original invoice INV-0007 not found."

    original_ids = {f"inv_{i}" for i in range(1, 114)}
    new_invs = [i for i in state["invoices"] if i["id"] not in original_ids]
    if not new_invs:
        return False, "No new invoice found (copy of INV-0007)."
    inv = new_invs[0]

    if inv["status"] != "draft":
        return False, f"Copy should be 'draft', got '{inv['status']}'"
    if inv["contactId"] != orig["contactId"]:
        return False, f"Copy contactId '{inv['contactId']}' doesn't match original '{orig['contactId']}'"
    if len(inv["lineItems"]) != len(orig["lineItems"]):
        return False, f"Copy has {len(inv['lineItems'])} line items, original has {len(orig['lineItems'])}"

    return True, "Awaiting_payment invoice INV-0007 copied to new draft successfully."
