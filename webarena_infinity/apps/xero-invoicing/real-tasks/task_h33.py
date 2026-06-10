import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    invoices = state.get("invoices", [])

    # INV-0056 and INV-0057 were awaiting approval in seed state
    for num in ["INV-0056", "INV-0057"]:
        inv = next((i for i in invoices if i.get("number") == num), None)
        if inv is None:
            return False, f"Invoice {num} not found."

        if inv.get("status") != "awaiting_payment":
            return False, f"Expected {num} status 'awaiting_payment', got '{inv.get('status')}'."

        if not inv.get("sentAt"):
            return False, f"Expected {num} to be sent (sentAt set), but sentAt is empty."

    # No invoices should still be awaiting approval
    still_awaiting = [i.get("number") for i in invoices if i.get("status") == "awaiting_approval"]
    if still_awaiting:
        return False, f"Invoices still awaiting approval: {', '.join(still_awaiting)}."

    return True, "INV-0056 and INV-0057 approved and sent."
