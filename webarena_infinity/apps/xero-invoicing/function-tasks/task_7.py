import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0053"), None)
    if not inv:
        return False, "Invoice INV-0053 not found."

    if inv["status"] != "paid":
        return False, f"Invoice INV-0053 status is '{inv['status']}', expected 'paid'."

    if inv["amountDue"] != 0:
        return False, f"Invoice INV-0053 amountDue is {inv['amountDue']}, expected 0."

    if len(inv["payments"]) < 1:
        return False, "Invoice INV-0053 has no payments recorded."

    payment = inv["payments"][-1]
    if abs(payment["amount"] - 823.90) > 0.01:
        return False, f"Payment amount is {payment['amount']}, expected 823.90."

    return True, "Invoice INV-0053 fully paid with $823.90 payment."
