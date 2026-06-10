import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Total remaining balance across seed gift cards:
    # Amazon gc_001: $50.00
    # Starbucks gc_002: $12.50
    # Target gc_003: $0.00
    # Netflix gc_004: $30.00
    # Home Depot gc_005: $75.00
    # Total: $167.50

    # Savings should have increased by $167.50 (from 12450.82 to ~12618.32)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 167.50
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $167.50 (total gift card remaining balance)."
            )

    # Should have a savings_deposit transaction
    transactions = state.get("transactions", [])
    found_deposit = any(
        t.get("type") == "savings_deposit"
        for t in transactions
        if t.get("id", "").startswith("txn_") and t.get("id") not in {
            "txn_017"  # seed savings deposit
        }
    )
    if not found_deposit:
        errors.append("No new savings_deposit transaction found.")

    if errors:
        return False, " ".join(errors)
    return True, "Deposited total gift card remaining balance ($167.50) into savings."
