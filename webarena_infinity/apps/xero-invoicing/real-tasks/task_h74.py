import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Southern Cross Veterinary (con_024)
    scv = next((c for c in state.get("contacts", []) if "Southern Cross" in c.get("name", "")), None)
    if scv is None:
        return False, "Southern Cross Veterinary contact not found."
    scv_id = scv.get("id")

    # Find new invoice
    seed_numbers = {
        "INV-0042", "INV-0043", "INV-0044", "INV-0045", "INV-0046", "INV-0047",
        "INV-0048", "INV-0049", "INV-0050", "INV-0051", "INV-0052", "INV-0053",
        "INV-0054", "INV-0055", "INV-0056", "INV-0057", "INV-0058", "INV-0059",
        "INV-0060", "INV-0061", "INV-0062", "INV-0063", "INV-0064", "INV-0065",
        "INV-0066",
    }
    new_invs = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == scv_id
        and i.get("number") not in seed_numbers
        and i.get("status") != "deleted"
    ]
    if not new_invs:
        return False, "No new invoice found for Southern Cross Veterinary."

    inv = new_invs[0]
    line_items = inv.get("lineItems", [])

    # Check security audit line item (~$5,500)
    audit = next(
        (li for li in line_items if abs(li.get("unitPrice", 0) - 5500.00) < 1.00),
        None
    )
    if audit is None:
        return False, "No line item with security audit (~$5,500)."

    # Check 10 hours consulting at $250
    consult = next(
        (li for li in line_items
         if abs(li.get("quantity", 0) - 10) < 0.01
         and abs(li.get("unitPrice", 0) - 250.00) < 1.00),
        None
    )
    if consult is None:
        return False, "No line item with 10 hours at ~$250 (consulting)."

    # Should be approved and sent
    if inv.get("status") not in ("awaiting_payment", "paid"):
        return False, f"Expected approved status, got '{inv.get('status')}'."

    if not inv.get("sentAt"):
        return False, "Invoice has not been sent."

    return True, f"Invoice {inv.get('number')} for Southern Cross Vet (audit + 10h consulting), approved and sent."
