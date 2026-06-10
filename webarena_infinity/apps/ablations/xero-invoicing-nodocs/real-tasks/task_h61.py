"""Verify: Contact with highest total overdue balance has all overdue invoices paid via Business Cheque."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Bloom & Branch Florists (con_15) has highest total overdue: inv_15 ($35,937.50) + inv_40 ($121,725)
    for inv_id, inv_num in [("inv_15", "INV-0015"), ("inv_40", "INV-0040")]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_num} not found")
            continue
        if inv["status"] != "paid":
            errors.append(f"{inv_num} status is '{inv['status']}', expected 'paid'")
        if inv.get("amountDue", 1) > 0.01:
            errors.append(f"{inv_num} amountDue is {inv.get('amountDue')}, expected 0")
        inv_pays = [p for p in payments if p["invoiceId"] == inv_id]
        if not inv_pays:
            errors.append(f"No payment found for {inv_num}")
        elif inv_pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"Payment for {inv_num} uses '{inv_pays[-1].get('bankAccountId')}', expected 'bank_1'")

    if errors:
        return False, "; ".join(errors)
    return True, "All overdue invoices for contact with highest overdue total (Bloom & Branch) paid via Business Cheque"
