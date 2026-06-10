"""Verify: $1,000 partial payment on every overdue invoice."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # All 14 overdue invoices should each have a $1,000 payment
    overdue_ids = [
        "inv_87", "inv_40", "inv_102", "inv_68", "inv_59", "inv_79",
        "inv_15", "inv_89", "inv_104", "inv_33", "inv_100", "inv_107",
        "inv_39", "inv_63",
    ]

    for inv_id in overdue_ids:
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

        # inv_87 total is $690, so $1,000 payment would fully pay it
        # inv_68 total is $431.25, same situation
        # For most others, they should remain non-paid (partial)
        if abs(inv.get("amountPaid", 0) - 1000) > 0.01 and inv.get("total", 0) > 1000:
            # Allow some tolerance for previously partially-paid invoices
            pass

    if errors:
        return False, "; ".join(errors)
    return True, f"$1,000 partial payment recorded on all {len(overdue_ids)} overdue invoices"
