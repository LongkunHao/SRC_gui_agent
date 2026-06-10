import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Step 1: Savings should have decreased by $1000 (from 12450.82 to ~11450.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 - 1000
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings}."
            )

    # Step 2: EUR balance should have increased (from seed 523.18)
    balances = state.get("balances", [])
    eur_bal = None
    for b in balances:
        if b.get("currency") == "EUR":
            eur_bal = b
            break

    if eur_bal is None:
        errors.append("EUR balance not found.")
    else:
        if eur_bal.get("amount", 0) <= 523.18:
            errors.append(
                f"EUR balance is {eur_bal.get('amount')}, expected > 523.18 "
                f"after converting $500."
            )

    # Step 3: BTC quantity should have increased (from seed 0.04521)
    crypto_holdings = state.get("cryptoHoldings", [])
    btc = None
    for c in crypto_holdings:
        if c.get("symbol") == "BTC":
            btc = c
            break

    if btc is None:
        errors.append("Bitcoin not found in crypto holdings.")
    else:
        seed_quantity = 0.04521
        if btc.get("quantity", 0) <= seed_quantity:
            errors.append(
                f"Bitcoin quantity is {btc.get('quantity')}, expected > {seed_quantity} "
                f"after investing $500."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Withdrew $1000 from savings, converted $500 to EUR, invested $500 in BTC."
