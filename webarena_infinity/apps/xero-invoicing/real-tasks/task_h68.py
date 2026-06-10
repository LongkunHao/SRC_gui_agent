import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    # Cascade Software development sprint invoice: INV-0052 (total $27,324)
    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0052"), None)
    if inv is None:
        return False, "INV-0052 not found."

    total = 27324.00
    expected_payment = total / 4  # $6,831.00

    payments = inv.get("payments", [])
    if not payments:
        return False, "No payments recorded on INV-0052."

    # Check that a payment of ~25% was recorded
    matching = next(
        (p for p in payments if abs(p.get("amount", 0) - expected_payment) < 1.00),
        None
    )
    if matching is None:
        actual_amounts = [p.get("amount", 0) for p in payments]
        return False, f"Expected payment of ~${expected_payment:.2f} (25% of ${total:.2f}), got payments: {actual_amounts}."

    return True, f"Payment of ${expected_payment:.2f} (25% of ${total:.2f}) recorded on INV-0052."
