import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    inv = next((i for i in state.get("invoices", []) if i.get("number") == "INV-0055"), None)
    if inv is None:
        return False, "Invoice INV-0055 not found."

    # Check $10,000 payment
    payments = inv.get("payments", [])
    pay_10k = next((p for p in payments if abs(p.get("amount", 0) - 10000.00) < 1.00), None)
    if pay_10k is None:
        return False, "No payment of ~$10,000 found on INV-0055."

    # Check amountDue ~31800 (41800 - 10000)
    expected_due = 41800.00 - 10000.00
    if abs(inv.get("amountDue", 0) - expected_due) > 1.00:
        return False, f"Expected amountDue ~${expected_due:.2f}, got ${inv.get('amountDue', 0):.2f}."

    # Check summary
    expected_summary = "Partial payment received for Phase 2 development"
    if inv.get("summary") != expected_summary:
        return False, f"Expected summary '{expected_summary}', got '{inv.get('summary')}'."

    return True, "INV-0055: $10,000 partial payment recorded and summary updated."
