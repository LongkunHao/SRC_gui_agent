import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Sapphire Bay Resort contact
    contact = next((c for c in state.get("contacts", []) if "Sapphire Bay" in c.get("name", "")), None)
    if contact is None:
        return False, "Sapphire Bay Resort contact not found."
    sb_id = contact.get("id")

    # Find new credit note for Sapphire Bay (not existing ones)
    credit_notes = state.get("creditNotes", [])
    new_cn = [
        cn for cn in credit_notes
        if cn.get("contactId") == sb_id
        and cn.get("status") != "deleted"
        and cn.get("number") not in ["CN-0008", "CN-0009", "CN-0010", "CN-0011", "CN-0012"]
    ]

    if not new_cn:
        return False, "No new credit note found for Sapphire Bay Resort."

    cn = new_cn[0]

    # Check total ~$550 ($500 + GST)
    if abs(cn.get("total", 0) - 550.00) > 10.00:
        # Could be $500 without GST if tax-free
        if abs(cn.get("total", 0) - 500.00) > 10.00:
            return False, f"Expected credit note total ~$500-550, got ${cn.get('total', 0):.2f}."

    # Check it's approved (status awaiting_payment or paid)
    if cn.get("status") not in ("awaiting_payment", "paid"):
        return False, f"Expected credit note approved (awaiting_payment/paid), got '{cn.get('status')}'."

    # Check allocated to INV-0054 (Sapphire Bay website invoice)
    allocations = cn.get("allocations", [])
    inv_054_alloc = next(
        (a for a in allocations if a.get("invoiceNumber") == "INV-0054" or a.get("invoiceId") == "inv_013"),
        None
    )
    if inv_054_alloc is None:
        return False, "Credit note not allocated to INV-0054 (Sapphire Bay website invoice)."

    return True, f"Credit note {cn.get('number')} created for Sapphire Bay ($500), approved, and allocated to INV-0054."
