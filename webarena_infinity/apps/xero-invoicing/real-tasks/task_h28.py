import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check quote prefix changed to EST-
    settings = state.get("invoiceSettings", {})
    if settings.get("quotePrefix") != "EST-":
        return False, f"Expected quote prefix 'EST-', got '{settings.get('quotePrefix')}'."

    # Find Outback Adventures contact
    contact = next((c for c in state.get("contacts", []) if "Outback Adventures" in c.get("name", "")), None)
    if contact is None:
        return False, "Outback Adventures Tourism contact not found."
    outback_id = contact.get("id")

    # Find new quote for Outback Adventures
    quotes = state.get("quotes", [])
    new_quo = next(
        (q for q in quotes
         if q.get("contactId") == outback_id
         and q.get("status") != "deleted"),
        None
    )
    if new_quo is None:
        return False, "No new quote found for Outback Adventures Tourism."

    # Check for 10 days of PM at $1,400
    line_items = new_quo.get("lineItems", [])
    pm_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 10) < 0.01
         and abs(li.get("unitPrice", 0) - 1400.00) < 1.00),
        None
    )
    if pm_line is None:
        return False, "No line item found with 10 days at ~$1,400 (project management)."

    # Check quote number starts with EST-
    if not new_quo.get("number", "").startswith("EST-"):
        return False, f"Expected quote number to start with 'EST-', got '{new_quo.get('number')}'."

    return True, f"Quote prefix changed to 'EST-' and quote {new_quo.get('number')} created for Outback Adventures."
