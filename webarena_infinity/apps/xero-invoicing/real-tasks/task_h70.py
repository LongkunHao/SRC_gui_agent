import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    # Check credit note prefix
    cn_prefix = settings.get("creditNotePrefix", "")
    if cn_prefix != "ADJ-":
        return False, f"Expected credit note prefix 'ADJ-', got '{cn_prefix}'."

    # Check quote prefix
    q_prefix = settings.get("quotePrefix", "")
    if q_prefix != "PROP-":
        return False, f"Expected quote prefix 'PROP-', got '{q_prefix}'."

    # Find Fresh Start Catering
    fsc = next((c for c in state.get("contacts", []) if "Fresh Start" in c.get("name", "")), None)
    if fsc is None:
        return False, "Fresh Start Catering contact not found."
    fsc_id = fsc.get("id")

    # Find new quote for Fresh Start
    seed_numbers = {"QU-0022", "QU-0023", "QU-0024", "QU-0025", "QU-0026", "QU-0027", "QU-0028", "QU-0029"}
    new_quotes = [
        q for q in state.get("quotes", [])
        if q.get("contactId") == fsc_id
        and q.get("number") not in seed_numbers
        and q.get("status") != "deleted"
    ]
    if not new_quotes:
        return False, "No new quote found for Fresh Start Catering."

    quo = new_quotes[0]
    line_items = quo.get("lineItems", [])

    # Check 3 days training at $2,200
    training = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 3) < 0.01
         and abs(li.get("unitPrice", 0) - 2200.00) < 1.00),
        None
    )
    if training is None:
        return False, "No line item with 3 days at ~$2,200 (on-site training)."

    return True, f"Prefixes updated (ADJ-, PROP-), quote {quo.get('number')} created for Fresh Start Catering."
