import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check LTC quantity decreased from 5.23400
    crypto_holdings = state.get("cryptoHoldings", [])
    ltc_holding = None
    for c in crypto_holdings:
        if c.get("symbol") == "LTC":
            ltc_holding = c
            break

    if ltc_holding is None:
        errors.append("No Litecoin (LTC) holding found in state.")
    else:
        ltc_quantity = ltc_holding.get("quantity", 0)
        if ltc_quantity >= 5.23400:
            errors.append(
                f"LTC quantity is {ltc_quantity}, expected it to have decreased from 5.23400."
            )

    # Check USD balance increased from 2847.63
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break

    if usd_balance is None:
        errors.append("No USD balance found in state.")
    else:
        if usd_balance <= 2847.63:
            errors.append(
                f"USD balance is {usd_balance}, expected it to have increased from 2847.63 "
                f"after selling Litecoin."
            )

    # Check for a crypto_sell transaction containing "Litecoin"
    transactions = state.get("transactions", [])
    found_crypto_sell = False
    for txn in transactions:
        if txn.get("type") == "crypto_sell" and "Litecoin" in txn.get("description", ""):
            found_crypto_sell = True
            break

    if not found_crypto_sell:
        errors.append(
            "No transaction with type 'crypto_sell' containing 'Litecoin' in description found."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully sold $75 of Litecoin: LTC quantity decreased, USD balance increased, and crypto_sell transaction recorded."
