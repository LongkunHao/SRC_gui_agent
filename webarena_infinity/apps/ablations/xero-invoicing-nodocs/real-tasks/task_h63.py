"""Verify: Smallest-balance awaiting-payment invoice paid via Credit Card."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # inv_55 (Bright Spark Electrical) has smallest AP amountDue ($37.20)
    inv = next((i for i in invoices if i["id"] == "inv_55"), None)
    if not inv:
        errors.append("Invoice INV-0055 not found")
    else:
        if inv["status"] != "paid":
            errors.append(f"INV-0055 status is '{inv['status']}', expected 'paid'")
        if inv.get("amountDue", 1) > 0.01:
            errors.append(f"INV-0055 amountDue is {inv.get('amountDue')}, expected 0")
        inv_pays = [p for p in payments if p["invoiceId"] == "inv_55"]
        if not inv_pays:
            errors.append("No payment found for INV-0055")
        else:
            last_pay = inv_pays[-1]
            if last_pay.get("bankAccountId") != "bank_5":
                errors.append(f"Payment uses '{last_pay.get('bankAccountId')}', expected 'bank_5' (Credit Card)")

    if errors:
        return False, "; ".join(errors)
    return True, "Smallest AP balance (INV-0055) paid via Credit Card"
