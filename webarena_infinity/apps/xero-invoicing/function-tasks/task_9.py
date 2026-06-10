import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    inv = next((i for i in state["invoices"] if i["number"] == "INV-0045"), None)
    if not inv:
        return False, "Invoice INV-0045 not found."

    if len(inv["payments"]) != 0:
        return False, f"Invoice INV-0045 still has {len(inv['payments'])} payment(s), expected 0."

    if abs(inv["amountPaid"]) > 0.01:
        return False, f"Invoice INV-0045 amountPaid is {inv['amountPaid']}, expected 0."

    if abs(inv["amountDue"] - 15840.00) > 0.01:
        return False, f"Invoice INV-0045 amountDue is {inv['amountDue']}, expected 15840.00."

    return True, "Payment removed from INV-0045. Amount due restored to $15,840.00."
