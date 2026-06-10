import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Find Bright Spark Electrical
    contact = next((c for c in state.get("contacts", []) if "Bright Spark" in c.get("name", "")), None)
    if contact is None:
        return False, "Bright Spark Electrical contact not found."
    bs_id = contact.get("id")

    # Find new quote for Bright Spark (no existing quotes for them in seed data)
    seed_quote_numbers = {"QU-0022", "QU-0023", "QU-0024", "QU-0025", "QU-0026", "QU-0027", "QU-0028", "QU-0029"}
    new_quotes = [
        q for q in state.get("quotes", [])
        if q.get("contactId") == bs_id
        and q.get("number") not in seed_quote_numbers
        and q.get("status") != "deleted"
    ]
    if not new_quotes:
        return False, "No new quote found for Bright Spark Electrical."

    quo = new_quotes[0]

    # Should be sent
    if quo.get("status") != "sent":
        return False, f"Expected quote status 'sent', got '{quo.get('status')}'."

    line_items = quo.get("lineItems", [])

    # Check for dev line: 20 hours at $185 with 5% discount
    dev_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 20) < 0.01
         and abs(li.get("unitPrice", 0) - 185.00) < 1.00),
        None
    )
    if dev_line is None:
        return False, "No line item with 20 hours at ~$185 (development)."
    if abs(dev_line.get("discountPercent", 0) - 5) > 0.5:
        return False, f"Expected 5% discount on development line, got {dev_line.get('discountPercent')}%."

    # Check for training line: 2 days at $2,200
    training_line = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 2) < 0.01
         and abs(li.get("unitPrice", 0) - 2200.00) < 1.00),
        None
    )
    if training_line is None:
        return False, "No line item with 2 days at ~$2,200 (training)."

    return True, f"Quote {quo.get('number')} created for Bright Spark with dev (5% disc) + training, sent."
