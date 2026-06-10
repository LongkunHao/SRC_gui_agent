import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    inv = next((i for i in state["invoices"] if i["invoiceNumber"] == "INV-0074"), None)
    if not inv:
        return False, "Invoice INV-0074 not found."
    if inv["status"] != "paid":
        return False, f"Expected status 'paid', got '{inv['status']}'"
    if abs(inv["amountDue"]) > 0.01:
        return False, f"Expected amountDue ~0, got {inv['amountDue']}"
    if not inv.get("paidAt"):
        return False, "paidAt is null."
    # Should have at least 2 payments (original partial + new)
    pays = [p for p in state["payments"] if p["invoiceId"] == inv["id"]]
    if len(pays) < 2:
        return False, f"Expected at least 2 payments, got {len(pays)}"
    return True, "Invoice INV-0074 fully paid with second payment of $802.82."
