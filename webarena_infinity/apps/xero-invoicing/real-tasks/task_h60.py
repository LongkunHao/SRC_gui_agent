import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Pinnacle Construction
    pinnacle = next((c for c in state.get("contacts", []) if "Pinnacle" in c.get("name", "")), None)
    if pinnacle is None:
        return False, "Pinnacle Construction Group contact not found."
    pin_id = pinnacle.get("id")

    # Find new credit note for Pinnacle (not CN-0008 which is the existing one)
    new_cns = [
        cn for cn in state.get("creditNotes", [])
        if cn.get("contactId") == pin_id
        and cn.get("number") != "CN-0008"
        and cn.get("status") != "deleted"
    ]
    if not new_cns:
        return False, "No new credit note found for Pinnacle Construction."

    cn = new_cns[0]

    # Check line items: 10h dev at $185 and 2 days PM at $1,400
    line_items = cn.get("lineItems", [])

    dev_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 10) < 0.01
         and abs(li.get("unitPrice", 0) - 185.00) < 1.00),
        None
    )
    if dev_line is None:
        return False, "No line item with 10 hours at ~$185 (development)."

    pm_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 2) < 0.01
         and abs(li.get("unitPrice", 0) - 1400.00) < 1.00),
        None
    )
    if pm_line is None:
        return False, "No line item with 2 days at ~$1,400 (project management)."

    # Should be approved (not draft)
    if cn.get("status") == "draft":
        return False, "Credit note should be approved (not draft)."

    # Should be allocated to INV-0045 (Pinnacle's partially paid invoice)
    allocations = cn.get("allocations", [])
    alloc_to_045 = next(
        (a for a in allocations if a.get("invoiceNumber") == "INV-0045" or a.get("invoiceId") == "inv_004"),
        None
    )
    if alloc_to_045 is None:
        return False, "Credit note not allocated to INV-0045 (partially paid Pinnacle invoice)."

    return True, f"Credit note {cn.get('number')} for Pinnacle (10h dev + 2d PM), approved, allocated to INV-0045."
