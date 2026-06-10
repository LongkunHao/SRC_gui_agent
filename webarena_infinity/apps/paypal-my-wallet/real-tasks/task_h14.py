import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check BTC quantity increased from 0.04521
    crypto_holdings = state.get("cryptoHoldings", [])
    btc = None
    eth = None
    for holding in crypto_holdings:
        if holding.get("symbol") == "BTC":
            btc = holding
        if holding.get("symbol") == "ETH":
            eth = holding

    if btc is None:
        errors.append("Bitcoin (BTC) holding not found in cryptoHoldings.")
    else:
        btc_qty = btc.get("quantity", 0)
        if btc_qty <= 0.04521:
            errors.append(
                f"BTC quantity is {btc_qty}, expected it to increase from 0.04521 "
                f"after investing $50."
            )

    # Check ETH quantity increased from 0.85200
    if eth is None:
        errors.append("Ethereum (ETH) holding not found in cryptoHoldings.")
    else:
        eth_qty = eth.get("quantity", 0)
        if eth_qty <= 0.85200:
            errors.append(
                f"ETH quantity is {eth_qty}, expected it to increase from 0.85200 "
                f"after investing $50."
            )

    # Check USD balance decreased by ~100
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2847.63 - 100  # 2747.63
        if abs(usd_balance - expected_usd) > 10.0:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus ~100 for two $50 crypto purchases, "
                f"plus possible fees)."
            )

    # Check for two crypto_buy transactions (one Bitcoin, one Ethereum)
    transactions = state.get("transactions", [])
    btc_buy_found = False
    eth_buy_found = False
    for txn in transactions:
        if txn.get("type") == "crypto_buy":
            desc = (txn.get("description") or "").lower()
            if "bitcoin" in desc or "btc" in desc:
                btc_buy_found = True
            if "ethereum" in desc or "eth" in desc:
                eth_buy_found = True

    if not btc_buy_found:
        errors.append(
            "No crypto_buy transaction found for Bitcoin in transactions."
        )
    if not eth_buy_found:
        errors.append(
            "No crypto_buy transaction found for Ethereum in transactions."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully invested $50 in Bitcoin and $50 in Ethereum."
