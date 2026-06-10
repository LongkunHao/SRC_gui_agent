import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # The most expensive un-invoiced accepted quote is QU-0022 ($52,360)
    quo = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0022"), None)
    if quo is None:
        return False, "QU-0022 not found."
    if not quo.get("isInvoiced"):
        return False, "QU-0022 should be marked as invoiced."

    # Find the new invoice created from this quote for Pinnacle (con_001)
    pinnacle_id = quo.get("contactId")
    seed_invoice_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    new_invs = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == pinnacle_id
        and i.get("number") not in seed_invoice_numbers
        and i.get("status") != "deleted"
    ]
    if not new_invs:
        return False, "No new invoice found for Pinnacle Construction from QU-0022."

    inv = new_invs[0]

    # Should be approved and sent
    if inv.get("status") != "awaiting_payment":
        return False, f"Expected new invoice status 'awaiting_payment', got '{inv.get('status')}'."
    if not inv.get("sentAt"):
        return False, "New invoice should be sent (sentAt should be set)."

    # Total should match the quote
    if abs(inv.get("total", 0) - quo.get("total", 0)) > 1.00:
        return False, f"Invoice total ${inv.get('total'):.2f} doesn't match quote total ${quo.get('total'):.2f}."

    return True, f"Invoice {inv.get('number')} created from QU-0022, approved, and sent."
