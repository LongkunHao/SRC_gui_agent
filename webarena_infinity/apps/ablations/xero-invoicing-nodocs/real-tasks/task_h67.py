"""Verify: Contact with most expensive paid invoice has all AP invoices paid via Business Cheque."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Most expensive paid invoice: inv_48 Redwood Property Management ($88,550)
    # Redwood's AP invoice: inv_23 ($1,661.75)
    inv_23 = next((i for i in invoices if i["id"] == "inv_23"), None)
    if not inv_23:
        errors.append("INV-0023 not found")
    else:
        if inv_23["status"] != "paid":
            errors.append(f"INV-0023 status is '{inv_23['status']}', expected 'paid'")
        if inv_23.get("amountDue", 1) > 0.01:
            errors.append(f"INV-0023 amountDue is {inv_23.get('amountDue')}, expected 0")
        pays = [p for p in payments if p["invoiceId"] == "inv_23"]
        if not pays:
            errors.append("No payment found for INV-0023")
        elif pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"Payment uses '{pays[-1].get('bankAccountId')}', expected 'bank_1'")

    if errors:
        return False, "; ".join(errors)
    return True, "Redwood PM AP invoices paid via Business Cheque (owner of most expensive paid invoice)"
