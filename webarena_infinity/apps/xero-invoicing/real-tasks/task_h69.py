import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Perth-based contacts: Pacific Freight (con_006), Redback Mining (con_010), Vanguard Security (con_023)
    perth_ids = set()
    for c in state.get("contacts", []):
        addr = c.get("address", "")
        if "Perth" in addr:
            perth_ids.add(c.get("id"))

    if not perth_ids:
        return False, "No Perth-based contacts found."

    # Check that all awaiting_payment invoices for Perth contacts are now paid
    # In seed: INV-0048 (Pacific Freight, $4,180) and INV-0053 (Vanguard, $823.90)
    paid_count = 0
    for inv in state.get("invoices", []):
        if inv.get("contactId") not in perth_ids:
            continue
        num = inv.get("number", "")
        # Only check invoices that were awaiting_payment in seed state
        if num == "INV-0048":
            if inv.get("status") != "paid":
                return False, f"Expected INV-0048 (Pacific Freight) to be paid, got '{inv.get('status')}'."
            paid_count += 1
        elif num == "INV-0053":
            if inv.get("status") != "paid":
                return False, f"Expected INV-0053 (Vanguard Security) to be paid, got '{inv.get('status')}'."
            paid_count += 1

    if paid_count < 2:
        return False, f"Expected 2 Perth invoices paid, found {paid_count}."

    return True, "Full payment recorded on INV-0048 (Pacific Freight) and INV-0053 (Vanguard Security)."
