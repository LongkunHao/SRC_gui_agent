"""Verify: Most recent overdue voided, second most recent paid."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Most recent overdue by issue date: inv_63 (2026-03-26) → void
    inv_63 = next((i for i in invoices if i["id"] == "inv_63"), None)
    if not inv_63:
        errors.append("Invoice inv_63 not found")
    else:
        if inv_63["status"] != "voided":
            errors.append(f"inv_63 (most recent overdue) status is '{inv_63['status']}', expected 'voided'")
        if not inv_63.get("voidedAt"):
            errors.append("inv_63 voidedAt is null")

    # Second most recent: inv_39 (2026-03-23) → full payment
    inv_39 = next((i for i in invoices if i["id"] == "inv_39"), None)
    if not inv_39:
        errors.append("Invoice inv_39 not found")
    else:
        if inv_39["status"] != "paid":
            errors.append(f"inv_39 (second most recent overdue) status is '{inv_39['status']}', expected 'paid'")
        if inv_39.get("amountDue", 1) > 0.01:
            errors.append(f"inv_39 amountDue is {inv_39.get('amountDue')}, expected 0")
        inv39_pays = [p for p in payments if p["invoiceId"] == "inv_39"]
        if not inv39_pays:
            errors.append("No payment found for inv_39")
        elif inv39_pays[-1].get("bankAccountId") != "bank_1":
            errors.append(f"Payment for inv_39 uses '{inv39_pays[-1].get('bankAccountId')}', expected 'bank_1'")

    if errors:
        return False, "; ".join(errors)
    return True, "Most recent overdue (inv_63) voided; second most recent (inv_39) fully paid"
