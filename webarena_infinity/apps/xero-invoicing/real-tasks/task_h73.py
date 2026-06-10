import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Murray River Winery draft invoice: INV-0058
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0058"), None)
    if inv is None:
        return False, "INV-0058 not found."

    # Check title updated
    title = inv.get("title", "")
    if title != "Website Redesign & Setup":
        return False, f"Expected title 'Website Redesign & Setup', got '{title}'."

    # Check for setup fee line item (~$500)
    line_items = inv.get("lineItems", [])
    setup_fee = next(
        (li for li in line_items if abs(li.get("unitPrice", 0) - 500.00) < 1.00),
        None
    )
    if setup_fee is None:
        return False, "No line item with setup fee (~$500) found on INV-0058."

    # Should have more than the original line items (at least 2 now)
    if len(line_items) < 2:
        return False, f"Expected at least 2 line items (original + setup fee), got {len(line_items)}."

    return True, "INV-0058 updated: title 'Website Redesign & Setup', setup fee line item added."
