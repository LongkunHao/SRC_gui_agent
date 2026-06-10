"""Verify: $2,000 partial payment on each overdue invoice for INV-0079's contact via Business Savings."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # INV-0079 belongs to Nexus Technologies (con_4). Overdue: inv_79, inv_104
    for inv_id, inv_num, orig_due in [("inv_79", "INV-0079", 6603.88), ("inv_104", "INV-0104", 7038)]:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"{inv_num} not found")
            continue
        inv_pays = [p for p in payments if p["invoiceId"] == inv_id]
        new_pays = [p for p in inv_pays if abs(p.get("amount", 0) - 2000) < 0.01]
        if not new_pays:
            errors.append(f"No $2,000 payment found for {inv_num}")
        else:
            pay = new_pays[-1]
            if pay.get("bankAccountId") != "bank_2":
                errors.append(f"{inv_num} payment uses '{pay.get('bankAccountId')}', expected 'bank_2' (Business Savings)")
        # Should still be overdue (partial payment)
        expected_due = round(orig_due - 2000, 2)
        if inv.get("amountDue") is not None and abs(inv["amountDue"] - expected_due) > 0.02:
            errors.append(f"{inv_num} amountDue is {inv['amountDue']}, expected ~{expected_due}")

    if errors:
        return False, "; ".join(errors)
    return True, "$2,000 partial payments on Nexus Tech overdue invoices via Business Savings"
