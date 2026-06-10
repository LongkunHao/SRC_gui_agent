import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])

    # Step 1: SEK should exist with positive balance (from converting $200)
    sek_bal = None
    for b in balances:
        if b.get("currency") == "SEK":
            sek_bal = b
            break

    if sek_bal is None:
        errors.append("Swedish Krona (SEK) not found in balances — should have been added.")
    elif sek_bal.get("amount", 0) <= 0:
        errors.append(
            f"SEK balance is {sek_bal.get('amount')}, expected > 0 after converting $200."
        )

    # Step 2: Check for currency_convert transaction
    transactions = state.get("transactions", [])
    found_convert = False
    for t in transactions:
        if t.get("type") == "currency_convert":
            desc = (t.get("description") or "").upper()
            if "SEK" in desc:
                found_convert = True
                break
    if not found_convert:
        errors.append("No currency_convert transaction to SEK found.")

    # Step 3: Savings should have increased by $200 (from 12450.82 to ~12650.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 200
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $200."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Added SEK, converted $200 to krona, and deposited $200 into savings."
