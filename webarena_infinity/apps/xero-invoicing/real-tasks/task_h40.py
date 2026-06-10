import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Outback Adventures contact
    contact = next((c for c in state.get("contacts", []) if "Outback Adventures" in c.get("name", "")), None)
    if contact is None:
        return False, "Outback Adventures Tourism contact not found."
    oa_id = contact.get("id")

    # Find new invoice for Outback Adventures (exclude voided INV-0065)
    invoices = state.get("invoices", [])
    new_inv = next(
        (inv for inv in invoices
         if inv.get("contactId") == oa_id
         and inv.get("number") != "INV-0065"
         and inv.get("status") != "deleted"),
        None
    )
    if new_inv is None:
        return False, "No new invoice found for Outback Adventures Tourism."

    # Should be approved (awaiting_payment)
    if new_inv.get("status") != "awaiting_payment":
        return False, f"Expected invoice status 'awaiting_payment' (approved), got '{new_inv.get('status')}'."

    line_items = new_inv.get("lineItems", [])
    if len(line_items) < 2:
        return False, f"Expected at least 2 line items, found {len(line_items)}."

    # Check for training line: 5 days at $2,200 with 15% discount
    training_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 5) < 0.01
         and abs(li.get("unitPrice", 0) - 2200.00) < 1.00),
        None
    )
    if training_line is None:
        return False, "No line item found with 5 days at ~$2,200 (on-site training)."

    if abs(training_line.get("discountPercent", 0) - 15) > 0.5:
        return False, f"Expected 15% discount on training line, got {training_line.get('discountPercent')}%."

    # Check for dev line: 40 hours at $185
    dev_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 40) < 0.01
         and abs(li.get("unitPrice", 0) - 185.00) < 1.00),
        None
    )
    if dev_line is None:
        return False, "No line item found with 40 hours at ~$185 (development work)."

    return True, f"Invoice {new_inv.get('number')} created for Outback Adventures with training (15% discount) + dev, approved."
