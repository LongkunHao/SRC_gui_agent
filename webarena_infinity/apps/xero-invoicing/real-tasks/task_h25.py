import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find contact with largest outstanding balance (TechVault, $28,160)
    contacts = state.get("contacts", [])
    max_contact = max(contacts, key=lambda c: c.get("outstandingBalance", 0))
    max_id = max_contact.get("id")
    max_name = max_contact.get("name")

    # Find new credit note for this contact
    credit_notes = state.get("creditNotes", [])
    new_cn = [
        cn for cn in credit_notes
        if cn.get("contactId") == max_id
        and cn.get("status") != "deleted"
        and cn.get("number") not in ["CN-0008", "CN-0009", "CN-0010", "CN-0011", "CN-0012"]
    ]

    if not new_cn:
        return False, f"No new credit note found for {max_name} (highest outstanding balance)."

    cn = new_cn[0]
    line_items = cn.get("lineItems", [])

    # Check for 5 hours of consulting at $250
    consult_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 5) < 0.01
         and abs(li.get("unitPrice", 0) - 250.00) < 1.00),
        None
    )
    if consult_line is None:
        return False, f"No line item found with 5 hours at ~$250 on new credit note for {max_name}."

    return True, f"Credit note {cn.get('number')} created for {max_name} (highest outstanding) with 5 hours consulting."
