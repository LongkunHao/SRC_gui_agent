import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # INV-0055 has title "Cloud Migration Phase 2"
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0055"), None)
    if inv is None:
        return False, "INV-0055 not found."

    # Check for $15,000 payment
    payments = inv.get("payments", [])
    pay_15k = next((p for p in payments if abs(p.get("amount", 0) - 15000.00) < 1.00), None)
    if pay_15k is None:
        return False, "No $15,000 payment found on INV-0055."

    # amountDue should be reduced
    expected_due = 41800.00 - 15000.00
    if abs(inv.get("amountDue", 0) - expected_due) > 1.00:
        return False, f"Expected amountDue ~${expected_due:.2f}, got ${inv.get('amountDue'):.2f}."

    return True, "INV-0055 ('Cloud Migration Phase 2') has $15,000 partial payment recorded."
