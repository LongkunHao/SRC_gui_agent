import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # QU-0028 should be accepted
    quo = next((q for q in state.get("quotes", []) if q.get("number") == "QU-0028"), None)
    if quo is None:
        return False, "Quote QU-0028 not found."
    if quo.get("status") != "accepted":
        return False, f"Expected QU-0028 status 'accepted', got '{quo.get('status')}'."

    # Find Metro Fabrication contact
    contact = next((c for c in state.get("contacts", []) if "Metro Fabrication" in c.get("name", "")), None)
    if contact is None:
        return False, "Metro Fabrication Works contact not found."
    metro_id = contact.get("id")

    # Find new invoice for Metro Fabrication with matching total (~$14,410)
    invoices = state.get("invoices", [])
    new_inv = next(
        (inv for inv in invoices
         if inv.get("contactId") == metro_id
         and abs(inv.get("total", 0) - 14410.00) < 5.00),
        None
    )
    if new_inv is None:
        return False, "No new invoice found for Metro Fabrication Works with total ~$14,410."

    return True, f"QU-0028 accepted and invoice {new_inv.get('number')} created for Metro Fabrication."
