import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Bitcoin (BTC) has the best percentage return in seed data (60.22%)
    # Verify that BTC quantity increased (investment of $100)
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
                f"after investing $100."
            )

        # Check for a new buy transaction
        btc_txns = btc.get("transactions", [])
        seed_tx_ids = {"ctx_001", "ctx_002", "ctx_003"}
        found_buy = False
        for tx in btc_txns:
            if tx.get("type") == "buy" and tx.get("id") not in seed_tx_ids:
                found_buy = True
                break
        if not found_buy:
            errors.append("No new buy transaction found in Bitcoin's transaction history.")

    # Check USD balance decreased by ~$100
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = 2847.63 - 100
        if abs(usd_bal.get("amount", 0) - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd} "
                f"after investing $100."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully invested $100 in Bitcoin (best percentage return crypto)."
