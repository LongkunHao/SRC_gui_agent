"""Verify: $1,000 payment on top 3 awaiting-payment invoices by total."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Top 3 AP by total: inv_22 ($250,000), inv_57 ($70,345.50), inv_65 ($49,271.75)
    target_ids = ["inv_22", "inv_57", "inv_65"]

    for inv_id in target_ids:
        inv = next((i for i in invoices if i["id"] == inv_id), None)
        if not inv:
            errors.append(f"Invoice {inv_id} not found")
            continue

        inv_pays = [p for p in payments if p["invoiceId"] == inv_id]
        thousand_pay = [p for p in inv_pays if abs(p["amount"] - 1000) < 0.01]
        if not thousand_pay:
            errors.append(f"No $1,000 payment found for {inv['invoiceNumber']} ({inv_id})")
        elif thousand_pay[0].get("bankAccountId") != "bank_1":
            errors.append(f"Payment for {inv_id} uses '{thousand_pay[0].get('bankAccountId')}', expected 'bank_1'")

        # None should be fully paid ($1k is tiny relative to totals)
        if inv.get("status") == "paid":
            errors.append(f"{inv_id} should not be fully paid (only $1,000 partial)")

    if errors:
        return False, "; ".join(errors)
    return True, "$1,000 partial payment recorded on top 3 awaiting-payment invoices"
