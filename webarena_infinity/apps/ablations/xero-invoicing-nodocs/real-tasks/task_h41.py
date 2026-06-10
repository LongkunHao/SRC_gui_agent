"""Verify: Canterbury contact — approve AA invoice (inv_56), pay remaining on partial AP (inv_6)."""
import requests


def verify(server_url: str) -> tuple[bool, str]:
    state = requests.get(f"{server_url}/api/state", timeout=5).json()
    invoices = state.get("invoices", [])
    payments = state.get("payments", [])
    errors = []

    # Canterbury contact is Summit Financial Advisors (con_6)
    # Their AA invoice: inv_56 should now be awaiting_payment
    inv_56 = next((i for i in invoices if i["id"] == "inv_56"), None)
    if not inv_56:
        errors.append("Invoice inv_56 not found")
    elif inv_56["status"] != "awaiting_payment":
        errors.append(f"inv_56 status is '{inv_56['status']}', expected 'awaiting_payment'")

    # Their partially-paid AP invoice: inv_6 should now be fully paid
    inv_6 = next((i for i in invoices if i["id"] == "inv_6"), None)
    if not inv_6:
        errors.append("Invoice inv_6 not found")
    else:
        if inv_6["status"] != "paid":
            errors.append(f"inv_6 status is '{inv_6['status']}', expected 'paid'")
        if inv_6["amountDue"] > 0.01:
            errors.append(f"inv_6 amountDue is {inv_6['amountDue']}, expected 0")
        # Check a payment of ~4875.84 exists
        inv6_pays = [p for p in payments if p["invoiceId"] == "inv_6"]
        new_pay = [p for p in inv6_pays if abs(p["amount"] - 4875.84) < 0.02]
        if not new_pay:
            errors.append("No payment of ~$4,875.84 found for inv_6")
        elif new_pay[0].get("bankAccountId") != "bank_1":
            errors.append(f"Payment bankAccountId is '{new_pay[0].get('bankAccountId')}', expected 'bank_1'")

    if errors:
        return False, "; ".join(errors)
    return True, "Canterbury contact: inv_56 approved, inv_6 fully paid"
