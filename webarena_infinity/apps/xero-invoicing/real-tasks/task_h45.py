import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Redback Mining Supplies (con_010) is the Perth-based customer+supplier
    redback = next((c for c in state.get("contacts", []) if "Redback" in c.get("name", "")), None)
    if redback is None:
        return False, "Redback Mining Supplies contact not found."
    rb_id = redback.get("id")

    # Find new invoice for Redback (not INV-0060 which is the existing draft)
    new_inv = next(
        (i for i in state.get("invoices", [])
         if i.get("contactId") == rb_id
         and i.get("number") != "INV-0060"
         and i.get("status") != "deleted"),
        None
    )
    if new_inv is None:
        return False, "No new invoice found for Redback Mining Supplies."

    # Should be submitted for approval
    if new_inv.get("status") != "awaiting_approval":
        return False, f"Expected status 'awaiting_approval', got '{new_inv.get('status')}'."

    line_items = new_inv.get("lineItems", [])

    # Check for consulting line: 8 hours at $250
    consult = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 8) < 0.01
         and abs(li.get("unitPrice", 0) - 250.00) < 1.00),
        None
    )
    if consult is None:
        return False, "No line item with 8 hours at ~$250 (consulting)."

    # Check for data migration line: 1 at $3,800
    migration = next(
        (li for li in line_items
         if abs(li.get("unitPrice", 0) - 3800.00) < 1.00),
        None
    )
    if migration is None:
        return False, "No line item with data migration (~$3,800)."

    return True, f"Invoice {new_inv.get('number')} created for Redback Mining with consulting + data migration, submitted for approval."
