"""Verify: INV-0107 paid, new approved invoice for Green Valley Organics."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Pay INV-0107
    inv_107 = next((i for i in invoices if i["id"] == "inv_107"), None)
    if not inv_107:
        errors.append("INV-0107 not found")
    else:
        if inv_107["status"] != "paid":
            errors.append(f"INV-0107 status is '{inv_107['status']}', expected 'paid'")
        if inv_107.get("amountDue", 1) > 0.01:
            errors.append(f"INV-0107 amountDue is {inv_107.get('amountDue')}, expected 0")
        pays = [p for p in payments if p["invoiceId"] == "inv_107"]
        if not pays:
            errors.append("No payment found for INV-0107")
        elif pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"INV-0107 payment uses '{pays[-1].get('bankAccountId')}', expected 'bank_1'")

    # New approved invoice for Green Valley Organics (con_7)
    # Seed AP invoices for con_7: inv_7, inv_57
    seed_ap = {"inv_7", "inv_57"}
    new_ap = [i for i in invoices
              if i.get("contactId") == "con_7"
              and i.get("status") == "awaiting_payment"
              and i["id"] not in seed_ap]
    if not new_ap:
        errors.append("No new approved invoice found for Green Valley Organics")
    else:
        inv = new_ap[0]
        if inv.get("issueDate") != "2026-03-18":
            errors.append(f"New invoice issueDate is '{inv.get('issueDate')}', expected '2026-03-18'")
        if inv.get("dueDate") != "2026-05-18":
            errors.append(f"New invoice dueDate is '{inv.get('dueDate')}', expected '2026-05-18'")
        lis = inv.get("lineItems", [])
        if len(lis) < 2:
            errors.append(f"Expected 2 line items, found {len(lis)}")
        else:
            produce = next((l for l in lis if "organic" in (l.get("description") or "").lower()
                            or "produce" in (l.get("description") or "").lower()), None)
            if not produce:
                errors.append("No 'Organic produce supply' line item found")
            elif abs(produce["quantity"] - 20) > 0.01 or abs(produce["unitPrice"] - 175) > 0.01:
                errors.append(f"Produce line: qty={produce['quantity']} price={produce['unitPrice']}, expected 20 x $175")
            delivery = next((l for l in lis if "delivery" in (l.get("description") or "").lower()), None)
            if not delivery:
                errors.append("No 'Delivery charges' line item found")
            elif abs(delivery["quantity"] - 4) > 0.01 or abs(delivery["unitPrice"] - 85) > 0.01:
                errors.append(f"Delivery line: qty={delivery['quantity']} price={delivery['unitPrice']}, expected 4 x $85")

    if errors:
        return False, "; ".join(errors)
    return True, "INV-0107 paid; new approved invoice created for Green Valley Organics"
