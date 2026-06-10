import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    invoices = state.get("invoices", [])

    # Find CloudNine Analytics contact
    contact = next((c for c in state.get("contacts", []) if "CloudNine" in c.get("name", "")), None)
    if contact is None:
        return False, "CloudNine Analytics contact not found."

    cn_id = contact.get("id")

    # Find all CloudNine invoices
    cn_invoices = [inv for inv in invoices if inv.get("contactId") == cn_id and inv.get("status") != "deleted"]
    if len(cn_invoices) < 2:
        return False, "Expected at least 2 CloudNine invoices."

    # The one with earliest due date is INV-0047 (due 2026-02-15)
    earliest = min(cn_invoices, key=lambda i: i.get("dueDate", "9999"))
    inv_num = earliest.get("number")

    if earliest.get("status") != "paid":
        return False, f"Expected {inv_num} status 'paid', got '{earliest.get('status')}'."

    if abs(earliest.get("amountDue", 9999)) > 0.01:
        return False, f"Expected {inv_num} amountDue=0, got {earliest.get('amountDue')}."

    return True, f"{inv_num} (earliest due CloudNine invoice) fully paid."
