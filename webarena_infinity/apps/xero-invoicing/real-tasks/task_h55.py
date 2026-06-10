import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Check NZ Export theme exists
    themes = state.get("brandingThemes", [])
    nz_theme = next((t for t in themes if t.get("name") == "NZ Export"), None)
    if nz_theme is None:
        return False, "'NZ Export' branding theme not found."

    if "Net 60" not in nz_theme.get("paymentTerms", ""):
        return False, f"Expected 'Net 60' in payment terms, got '{nz_theme.get('paymentTerms')}'."

    nz_theme_id = nz_theme.get("id")

    # Find Wellington & Partners
    contact = next((c for c in state.get("contacts", []) if "Wellington" in c.get("name", "")), None)
    if contact is None:
        return False, "Wellington & Partners contact not found."
    wp_id = contact.get("id")

    # Find new invoice for Wellington in NZD using NZ Export theme
    seed_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    new_invs = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == wp_id
        and i.get("number") not in seed_numbers
        and i.get("status") != "deleted"
    ]
    if not new_invs:
        return False, "No new invoice found for Wellington & Partners."

    inv = new_invs[0]

    if inv.get("currency") != "NZD":
        return False, f"Expected currency 'NZD', got '{inv.get('currency')}'."

    if inv.get("brandingThemeId") != nz_theme_id:
        return False, f"Invoice should use 'NZ Export' theme."

    # Check for 8 hours consulting at $250
    line_items = inv.get("lineItems", [])
    consult = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 8) < 0.01
         and abs(li.get("unitPrice", 0) - 250.00) < 1.00),
        None
    )
    if consult is None:
        return False, "No line item with 8 hours at ~$250 (consulting)."

    return True, f"'NZ Export' theme created, invoice {inv.get('number')} for Wellington in NZD using it."
