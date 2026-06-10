import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0052"), None)
    if not inv:
        return False, "Invoice INV-0052 not found."

    if inv["status"] != "awaiting_payment":
        return False, f"Invoice INV-0052 status is '{inv['status']}', expected 'awaiting_payment'."

    if len(inv["payments"]) < 1:
        return False, "Invoice INV-0052 has no payments recorded."

    payment = inv["payments"][-1]
    if abs(payment["amount"] - 5000.00) > 0.01:
        return False, f"Payment amount is {payment['amount']}, expected 5000.00."

    expected_due = 27324.00 - 5000.00
    if abs(inv["amountDue"] - expected_due) > 0.01:
        return False, f"Invoice amountDue is {inv['amountDue']}, expected {expected_due}."

    return True, "Partial payment of $5,000 recorded on INV-0052. Amount due: $22,324.00."
