import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Northern Territory Power Corp (con_017)
    ntp = next((c for c in state.get("contacts", []) if "Northern Territory" in c.get("name", "")), None)
    if ntp is None:
        return False, "Northern Territory Power Corp contact not found."
    ntp_id = ntp.get("id")

    # Find new quote
    seed_numbers = {"QU-0022", "QU-0023", "QU-0024", "QU-0025", "QU-0026", "QU-0027", "QU-0028", "QU-0029"}
    new_quotes = [
        q for q in state.get("quotes", [])
        if q.get("contactId") == ntp_id
        and q.get("number") not in seed_numbers
        and q.get("status") != "deleted"
    ]
    if not new_quotes:
        return False, "No new quote found for Northern Territory Power Corp."

    quo = new_quotes[0]
    line_items = quo.get("lineItems", [])

    # Check security audit at $5,500
    audit = next(
        (li for li in line_items if abs(li.get("unitPrice", 0) - 5500.00) < 1.00),
        None
    )
    if audit is None:
        return False, "No line item with security audit (~$5,500)."

    # Check 30 hours development at $185 with 10% discount
    dev = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 30) < 0.01
         and abs(li.get("unitPrice", 0) - 185.00) < 1.00),
        None
    )
    if dev is None:
        return False, "No line item with 30 hours at ~$185 (development)."

    if abs(dev.get("discountPercent", 0) - 10) > 0.5:
        return False, f"Expected 10% discount on development, got {dev.get('discountPercent')}%."

    # Check Professional Services theme
    if quo.get("brandingThemeId") != "theme_professional":
        return False, f"Expected Professional Services branding theme."

    return True, f"Quote {quo.get('number')} for NTP: audit + 30h dev (10% discount), Professional Services theme."
