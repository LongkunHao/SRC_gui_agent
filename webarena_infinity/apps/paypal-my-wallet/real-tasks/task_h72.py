import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    crypto_holdings = state.get("cryptoHoldings", [])

    # Returns: BTC 60.22%, ETH 55.39%, LTC 35.79%, LINK 32.04%, BCH 27.64%
    # Second-highest return: ETH (55.39%) — should buy $75
    # Lowest positive return: BCH (27.64%) — should sell $75

    # ETH quantity should have increased (from seed 0.852)
    eth = None
    for c in crypto_holdings:
        if c.get("symbol") == "ETH":
            eth = c
            break

    if eth is None:
        errors.append("Ethereum not found in crypto holdings.")
    else:
        seed_quantity = 0.852
        if eth.get("quantity", 0) <= seed_quantity:
            errors.append(
                f"Ethereum quantity is {eth.get('quantity')}, expected > {seed_quantity} "
                f"after buying $75 (second-highest return)."
            )

    # BCH quantity should have decreased (from seed 1.1)
    bch = None
    for c in crypto_holdings:
        if c.get("symbol") == "BCH":
            bch = c
            break

    if bch is None:
        errors.append("Bitcoin Cash not found in crypto holdings.")
    else:
        seed_quantity = 1.1
        if bch.get("quantity", 0) >= seed_quantity:
            errors.append(
                f"Bitcoin Cash quantity is {bch.get('quantity')}, expected < {seed_quantity} "
                f"after selling $75 (lowest positive return)."
            )

    # Should have both buy and sell transactions
    transactions = state.get("transactions", [])
    found_buy = any(
        t.get("type") == "crypto_buy" and "Ethereum" in (t.get("description") or "")
        for t in transactions
    )
    found_sell = any(
        t.get("type") == "crypto_sell" and "Bitcoin Cash" in (t.get("description") or "")
        for t in transactions
    )
    if not found_buy:
        errors.append("No crypto_buy transaction for Ethereum found.")
    if not found_sell:
        errors.append("No crypto_sell transaction for Bitcoin Cash found.")

    if errors:
        return False, " ".join(errors)
    return True, "Bought $75 ETH (second-highest return) and sold $75 BCH (lowest positive return)."
