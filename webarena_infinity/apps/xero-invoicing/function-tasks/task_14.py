import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0045"), None)
    if not inv:
        return False, "Invoice INV-0045 not found."

    if inv["status"] != "paid":
        return False, f"Invoice INV-0045 status is '{inv['status']}', expected 'paid'."

    if inv["amountDue"] != 0:
        return False, f"Invoice INV-0045 amountDue is {inv['amountDue']}, expected 0."

    if len(inv["payments"]) < 2:
        return False, f"Invoice INV-0045 has {len(inv['payments'])} payment(s), expected at least 2."

    new_payment = inv["payments"][-1]
    if abs(new_payment["amount"] - 10890.00) > 0.01:
        return False, f"New payment amount is {new_payment['amount']}, expected 10890.00."

    return True, "Invoice INV-0045 fully paid with additional $10,890 payment."
