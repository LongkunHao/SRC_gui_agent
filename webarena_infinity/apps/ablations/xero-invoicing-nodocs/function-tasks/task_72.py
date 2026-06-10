import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0067"), None)
    if not inv:
        return False, "Invoice INV-0067 not found."
    if inv["status"] != "paid":
        return False, f"Expected status 'paid', got '{inv['status']}'"
    if abs(inv["amountDue"]) > 0.01:
        return False, f"Expected amountDue ~0, got {inv['amountDue']}"
    pay = next((p for p in state["payments"] if p["invoiceId"] == inv["id"] and abs(p["amount"] - 2520) < 0.01), None)
    if not pay:
        return False, "Payment of $2520 not found."
    if pay["bankAccountId"] != "bank_4":
        return False, f"Expected bank 'bank_4' (AUD Holding), got '{pay['bankAccountId']}'"
    return True, "Full payment of $2520 on INV-0067 using AUD Holding Account recorded correctly."
