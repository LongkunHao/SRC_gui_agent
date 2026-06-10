import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # BTC has best percentage return (60.22%) in seed data.
    # Agent should have sold $50 of BTC.
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
        if btc.get("quantity", 0) >= seed_quantity:
            errors.append(
                f"Bitcoin quantity is {btc.get('quantity')}, expected < {seed_quantity} "
                f"after selling $50."
            )

        # Check for a new sell transaction
        btc_txns = btc.get("transactions", [])
        seed_tx_ids = {"ctx_001", "ctx_002", "ctx_003"}
        found_sell = False
        for tx in btc_txns:
            if tx.get("type") == "sell" and tx.get("id") not in seed_tx_ids:
                found_sell = True
                break
        if not found_sell:
            errors.append("No new sell transaction found in Bitcoin's transaction history.")

    # Savings should have increased by $50 (from 12450.82 to ~12500.82)
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 50
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $50."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Sold $50 of best-performing crypto (BTC) and deposited $50 into savings."
