import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Invoice with reference containing 'WO': INV-0048 (ref PF-WO-3301)
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0048"), None)
    if inv is None:
        return False, "INV-0048 not found."

    ref = inv.get("reference", "")
    if "WO" not in ref:
        return False, f"INV-0048 reference '{ref}' does not contain 'WO'."

    payments = inv.get("payments", [])
    if not payments:
        return False, "No payments recorded on INV-0048."

    matching = next(
        (p for p in payments if abs(p.get("amount", 0) - 1500.00) < 1.00),
        None
    )
    if matching is None:
        actual_amounts = [p.get("amount", 0) for p in payments]
        return False, f"Expected $1,500 payment on INV-0048, got payments: {actual_amounts}."

    return True, "Payment of $1,500 recorded on INV-0048 (reference PF-WO-3301)."
