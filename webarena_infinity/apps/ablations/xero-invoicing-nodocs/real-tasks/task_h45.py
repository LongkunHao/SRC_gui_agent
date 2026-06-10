"""Verify: Full payment on every overdue invoice with 4+ line items."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Overdue invoices with 4+ line items: inv_59, inv_63, inv_100, inv_102
    target_ids = ["inv_59", "inv_63", "inv_100", "inv_102"]

    for inv_id in target_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue
        if inv["status"] != "paid":
            errors.append(f"{inv['invoiceNumber']} ({inv_id}) status is '{inv['status']}', expected 'paid'")
        if inv.get("amountDue", 1) > 0.01:
            errors.append(f"{inv_id} amountDue is {inv.get('amountDue')}, expected 0")
        inv_pays = [p for p in payments if p["invoiceId"] == inv_id]
        if not inv_pays:
            errors.append(f"No payment found for {inv_id}")
        else:
            for p in inv_pays:
                if p.get("bankAccountId") != "bank_1":
                    errors.append(f"Payment for {inv_id} uses '{p.get('bankAccountId')}', expected 'bank_1'")
                    break

    # Overdue invoices with <4 line items should NOT be paid
    should_not_pay = ["inv_87", "inv_68", "inv_15", "inv_40", "inv_39", "inv_107", "inv_33", "inv_79", "inv_89", "inv_104"]
    for inv_id in should_not_pay:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if inv and inv["status"] == "paid":
            errors.append(f"{inv_id} was paid but should not have been (has <4 line items)")

    if errors:
        return False, "; ".join(errors)
    return True, f"All {len(target_ids)} overdue invoices with 4+ line items paid via Business Cheque Account"
