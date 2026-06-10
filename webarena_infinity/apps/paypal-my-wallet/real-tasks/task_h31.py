import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    crypto_holdings = state.get("cryptoHoldings", [])
    bch = None
    ltc = None
    for c in crypto_holdings:
        if c.get("symbol") == "BCH":
            bch = c
        elif c.get("symbol") == "LTC":
            ltc = c

    # BCH should have decreased from seed quantity 1.1
    if bch is None:
        errors.append("Bitcoin Cash not found in crypto holdings.")
    else:
        if bch.get("quantity", 1.1) >= 1.09:
            errors.append(
                f"Bitcoin Cash quantity is {bch.get('quantity')}, expected < 1.09 "
                f"after selling $50 worth."
            )

    # LTC should have increased from seed quantity 5.234
    if ltc is None:
        errors.append("Litecoin not found in crypto holdings.")
    else:
        if ltc.get("quantity", 5.234) <= 5.234:
            errors.append(
                f"Litecoin quantity is {ltc.get('quantity')}, expected > 5.234 "
                f"after buying $50 worth."
            )

    # Check for crypto_sell (BCH) and crypto_buy (LTC) transactions
    transactions = state.get("transactions", [])
    found_sell = False
    found_buy = False
    for t in transactions:
        desc = (t.get("description") or "").lower()
        if t.get("type") == "crypto_sell" and "bitcoin cash" in desc:
            found_sell = True
        if t.get("type") == "crypto_buy" and "litecoin" in desc:
            found_buy = True

    if not found_sell:
        errors.append("No crypto_sell transaction for Bitcoin Cash found.")
    if not found_buy:
        errors.append("No crypto_buy transaction for Litecoin found.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully sold $50 of Bitcoin Cash and bought $50 of Litecoin."
