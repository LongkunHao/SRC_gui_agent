import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Canberra-based contact: Cascade Software Solutions (con_020)
    cascade = next((c for c in state.get("contacts", []) if "Cascade" in c.get("name", "")), None)
    if cascade is None:
        return False, "Cascade Software Solutions contact not found."
    cs_id = cascade.get("id")

    # Find new invoice for Cascade (not INV-0052)
    seed_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    new_invs = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == cs_id
        and i.get("number") not in seed_numbers
        and i.get("status") != "deleted"
    ]
    if not new_invs:
        return False, "No new invoice found for Cascade Software."

    inv = new_invs[0]
    line_items = inv.get("lineItems", [])

    # Check 40 hours consulting at $250
    consult = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 40) < 0.01
         and abs(li.get("unitPrice", 0) - 250.00) < 1.00),
        None
    )
    if consult is None:
        return False, "No line item with 40 hours at ~$250 (consulting)."

    # Check 3 days PM at $1,400
    pm = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 3) < 0.01
         and abs(li.get("unitPrice", 0) - 1400.00) < 1.00),
        None
    )
    if pm is None:
        return False, "No line item with 3 days at ~$1,400 (project management)."

    # Should be approved
    if inv.get("status") not in ("awaiting_payment", "paid"):
        return False, f"Expected approved status, got '{inv.get('status')}'."

    return True, f"Invoice {inv.get('number')} for Cascade Software (40h consulting + 3d PM), approved."
