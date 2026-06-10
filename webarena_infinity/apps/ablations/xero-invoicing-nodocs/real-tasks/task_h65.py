"""Verify: Waikato contacts — Hamilton Plumbing: approve AA + pay overdue; Velocity: delete drafts."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Hamilton Plumbing (alphabetically first): approve inv_77 (AA), pay inv_102 (overdue)
    inv_77 = next((i for i in invoices if i["id"] == "inv_77"), None)
    if not inv_77:
        errors.append("INV-0077 not found")
    elif inv_77["status"] != "awaiting_payment":
        errors.append(f"INV-0077 status is '{inv_77['status']}', expected 'awaiting_payment'")

    inv_102 = next((i for i in invoices if i["id"] == "inv_102"), None)
    if not inv_102:
        errors.append("INV-0102 not found")
    else:
        if inv_102["status"] != "paid":
            errors.append(f"INV-0102 status is '{inv_102['status']}', expected 'paid'")
        if inv_102.get("amountDue", 1) > 0.01:
            errors.append(f"INV-0102 amountDue is {inv_102.get('amountDue')}, expected 0")
        pays = [p for p in payments if p["invoiceId"] == "inv_102"]
        if not pays:
            errors.append("No payment found for INV-0102")
        elif pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"INV-0102 payment uses '{pays[-1].get('bankAccountId')}', expected 'bank_1'")

    # Velocity Sports (alphabetically second): delete draft inv_25
    inv_25 = next((i for i in invoices if i["id"] == "inv_25"), None)
    if inv_25:
        errors.append(f"INV-0025 still exists with status '{inv_25['status']}', expected deleted")

    if errors:
        return False, "; ".join(errors)
    return True, "Hamilton Plumbing AA approved + overdue paid; Velocity drafts deleted"
