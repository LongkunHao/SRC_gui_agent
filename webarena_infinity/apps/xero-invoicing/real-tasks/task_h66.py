import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Alice Springs contact: Outback Adventures Tourism (con_015)
    outback = next((c for c in state.get("contacts", []) if "Outback" in c.get("name", "")), None)
    if outback is None:
        return False, "Outback Adventures Tourism contact not found."
    oa_id = outback.get("id")

    # Find new repeating invoice for this contact
    seed_rep_ids = {"rep_001", "rep_002", "rep_003", "rep_004", "rep_005"}
    new_reps = [
        r for r in state.get("repeatingInvoices", [])
        if r.get("contactId") == oa_id
        and r.get("id") not in seed_rep_ids
    ]
    if not new_reps:
        return False, "No new repeating invoice found for Outback Adventures."

    rep = new_reps[0]

    if rep.get("frequency") != "monthly":
        return False, f"Expected frequency 'monthly', got '{rep.get('frequency')}'."

    if rep.get("saveAs") != "approved_for_sending":
        return False, f"Expected saveAs 'approved_for_sending', got '{rep.get('saveAs')}'."

    # Check for hosting and support line items
    line_items = rep.get("lineItems", [])
    hosting = next(
        (li for li in line_items if abs(li.get("unitPrice", 0) - 299.00) < 1.00),
        None
    )
    if hosting is None:
        return False, "No hosting line item (~$299) found."

    support = next(
        (li for li in line_items if abs(li.get("unitPrice", 0) - 450.00) < 1.00),
        None
    )
    if support is None:
        return False, "No support line item (~$450) found."

    return True, f"Monthly repeating invoice created for Outback Adventures with hosting + support, approved for sending."
