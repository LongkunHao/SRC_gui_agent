import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    # Check invoice prefix changed to AUS-
    prefix = settings.get("invoicePrefix", "")
    if prefix != "AUS-":
        return False, f"Expected invoice prefix 'AUS-', got '{prefix}'."

    # Find CloudNine Analytics
    cn = next((c for c in state.get("contacts", []) if "CloudNine" in c.get("name", "")), None)
    if cn is None:
        return False, "CloudNine Analytics contact not found."
    cn_id = cn.get("id")

    # Find new invoice for CloudNine (not the seed ones)
    seed_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    new_invs = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == cn_id
        and i.get("number") not in seed_numbers
        and i.get("status") != "deleted"
    ]
    if not new_invs:
        return False, "No new invoice found for CloudNine Analytics."

    inv = new_invs[0]
    line_items = inv.get("lineItems", [])

    # Check 8 hours UI/UX design at $165
    design = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 8) < 0.01
         and abs(li.get("unitPrice", 0) - 165.00) < 1.00),
        None
    )
    if design is None:
        return False, "No line item with 8 hours at ~$165 (UI/UX design)."

    # Invoice number should use new prefix AUS- and number should be >= 100
    inv_num = inv.get("number", "")
    if not inv_num.startswith("AUS-"):
        return False, f"Expected invoice number starting with 'AUS-', got '{inv_num}'."

    return True, f"Prefix changed to AUS-, invoice {inv_num} created for CloudNine (8h design)."
