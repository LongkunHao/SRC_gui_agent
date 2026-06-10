import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    balances = state.get("balances", [])

    # AUD should be removed
    aud_exists = any(b.get("currency") == "AUD" for b in balances)
    if aud_exists:
        errors.append("Australian Dollar should have been removed from currencies.")

    # Should have a currency_convert transaction from AUD
    transactions = state.get("transactions", [])
    found_convert = any(
        t.get("type") == "currency_convert"
        and "AUD" in (t.get("description") or "").upper()
        for t in transactions
    )
    if not found_convert:
        errors.append("No currency_convert transaction from AUD found.")

    # ETH quantity should have increased (from seed 0.852)
    crypto_holdings = state.get("cryptoHoldings", [])
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
                f"after buying $100."
            )

    # Should have a crypto_buy transaction for Ethereum
    found_buy = any(
        t.get("type") == "crypto_buy" and "Ethereum" in (t.get("description") or "")
        for t in transactions
    )
    if not found_buy:
        errors.append("No crypto_buy transaction for Ethereum found.")

    if errors:
        return False, " ".join(errors)
    return True, "Converted all AUD to USD, removed AUD currency, and bought $100 of Ethereum."
