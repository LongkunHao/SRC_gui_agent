import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # QU-0023 should be accepted
    quo = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0023"), None)
    if quo is None:
        return False, "QU-0023 not found."
    if quo.get("status") != "accepted":
        return False, f"Expected QU-0023 status 'accepted', got '{quo.get('status')}'."
    if not quo.get("isInvoiced"):
        return False, "QU-0023 should be marked as invoiced."

    # Find new invoice for Redback Mining (con_010)
    redback_id = quo.get("contactId")
    seed_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    new_invs = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == redback_id
        and i.get("number") not in seed_numbers
        and i.get("status") != "deleted"
    ]
    if not new_invs:
        return False, "No new invoice found for Redback Mining from QU-0023."

    inv = new_invs[0]

    # Should have $5,000 partial payment
    payments = inv.get("payments", [])
    pay_5k = next((p for p in payments if abs(p.get("amount", 0) - 5000.00) < 1.00), None)
    if pay_5k is None:
        return False, f"No $5,000 payment found on new invoice {inv.get('number')}."

    return True, f"QU-0023 accepted, invoice {inv.get('number')} created, $5,000 payment recorded."
