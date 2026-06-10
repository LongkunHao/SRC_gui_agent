"""Verify: San Francisco contact AP invoices paid via USD Holding, AA invoices approved."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # DataFlow Analytics (con_11) based in San Francisco
    # AP invoices: inv_11 ($2,415), inv_36 ($7,020.75) → pay via bank_3 (USD Holding)
    for inv_id, inv_num in [("inv_11", "INV-0011"), ("inv_36", "INV-0036")]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} not found")
            continue
        if inv["status"] != "paid":
            errors.append(f"{inv_num} status is '{inv['status']}', expected 'paid'")
        if inv.get("amountDue", 1) > 0.01:
            errors.append(f"{inv_num} amountDue is {inv.get('amountDue')}, expected 0")
        pays = [p for p in payments if p["invoiceId"] == inv_id]
        if not pays:
            errors.append(f"No payment found for {inv_num}")
        elif pays[-1].get("bankAccountId") != "bank_3":
            errors.append(f"{inv_num} payment uses '{pays[-1].get('bankAccountId')}', expected 'bank_3' (USD Holding)")

    # AA invoice: inv_111 → approved
    inv_111 = next((i for i in invoices if i["id"] == "inv_111"), None)
    if not inv_111:
        errors.append("INV-0111 not found")
    elif inv_111["status"] != "awaiting_payment":
        errors.append(f"INV-0111 status is '{inv_111['status']}', expected 'awaiting_payment'")

    if errors:
        return False, "; ".join(errors)
    return True, "DataFlow AP invoices paid via USD Holding; AA invoice approved"
