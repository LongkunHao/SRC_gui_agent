"""Verify: Contacts starting with 'S' — all AA approved, all overdue paid via Business Cheque."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Summit Financial Advisors (con_6): approve AA inv_56
    inv_56 = next((i for i in invoices if i["id"] == "inv_56"), None)
    if not inv_56:
        errors.append("INV-0056 not found")
    elif inv_56["status"] != "awaiting_payment":
        errors.append(f"INV-0056 status is '{inv_56['status']}', expected 'awaiting_payment'")

    # Swift Courier Services (con_12): approve AA inv_112, pay overdue inv_87
    inv_112 = next((i for i in invoices if i["id"] == "inv_112"), None)
    if not inv_112:
        errors.append("INV-0112 not found")
    elif inv_112["status"] != "awaiting_payment":
        errors.append(f"INV-0112 status is '{inv_112['status']}', expected 'awaiting_payment'")

    inv_87 = next((i for i in invoices if i["id"] == "inv_87"), None)
    if not inv_87:
        errors.append("INV-0087 not found")
    else:
        if inv_87["status"] != "paid":
            errors.append(f"INV-0087 status is '{inv_87['status']}', expected 'paid'")
        if inv_87.get("amountDue", 1) > 0.01:
            errors.append(f"INV-0087 amountDue is {inv_87.get('amountDue')}, expected 0")
        pays = [p for p in payments if p["invoiceId"] == "inv_87"]
        if not pays:
            errors.append("No payment found for INV-0087")
        elif pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"INV-0087 payment uses '{pays[-1].get('bankAccountId')}', expected 'bank_1'")

    if errors:
        return False, "; ".join(errors)
    return True, "S-contacts: Summit AA approved, Swift AA approved + overdue paid"
