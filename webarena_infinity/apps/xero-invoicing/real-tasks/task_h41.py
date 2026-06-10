import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # INV-0046 is Baxter & Associates overdue invoice — should be paid
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0046"), None)
    if inv is None:
        return False, "INV-0046 not found."
    if inv.get("status") != "paid":
        return False, f"Expected INV-0046 status 'paid', got '{inv.get('status')}'."
    if inv.get("amountDue", 0) > 0.01:
        return False, f"Expected INV-0046 amountDue ~0, got {inv.get('amountDue')}."

    # Find copy: another invoice for same contact (con_005) that is draft with reference BAX-Q2-2026
    baxter_id = inv.get("contactId")
    copies = [
        i for i in state.get("invoices", [])
        if i.get("contactId") == baxter_id
        and i.get("number") != "INV-0046"
        and i.get("status") == "draft"
        and i.get("reference") == "BAX-Q2-2026"
    ]
    if not copies:
        return False, "No draft copy of INV-0046 found with reference 'BAX-Q2-2026' for Baxter & Associates."

    return True, "INV-0046 paid, copy created as draft with reference 'BAX-Q2-2026'."
