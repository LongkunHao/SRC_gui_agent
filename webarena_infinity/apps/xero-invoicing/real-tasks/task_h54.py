import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # The invoice with the smallest outstanding balance is INV-0053 (Vanguard, $823.90)
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0053"), None)
    if inv is None:
        return False, "INV-0053 not found."

    if inv.get("status") != "paid":
        return False, f"Expected INV-0053 status 'paid', got '{inv.get('status')}'."

    if inv.get("amountDue", 0) > 0.01:
        return False, f"Expected INV-0053 amountDue ~0, got ${inv.get('amountDue'):.2f}."

    return True, "INV-0053 (smallest outstanding, $823.90) paid in full."
