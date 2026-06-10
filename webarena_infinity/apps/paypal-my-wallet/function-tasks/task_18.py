import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check USD balance decreased from 2847.63
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b
            break

    if usd_balance is None:
        return False, "No USD balance entry found."

    usd_amount = usd_balance.get("amount", 0)
    if usd_amount >= 2847.63:
        return False, f"USD balance should have decreased from 2847.63 after buying $100 of BTC, but is {usd_amount}."

    expected_usd = 2847.63 - 100
    if abs(usd_amount - expected_usd) > 5.0:
        return False, f"USD balance should be around {expected_usd}, but is {usd_amount}."

    # Check BTC quantity increased from 0.04521
    crypto_holdings = state.get("cryptoHoldings", [])
    btc_holding = None
    for c in crypto_holdings:
        if c.get("symbol") == "BTC" or c.get("currency") == "BTC" or c.get("name", "").lower() == "bitcoin":
            btc_holding = c
            break

    if btc_holding is None:
        return False, "No BTC crypto holding found."

    btc_qty = btc_holding.get("quantity", btc_holding.get("amount", 0))
    if btc_qty <= 0.04521:
        return False, f"BTC quantity should have increased from 0.04521, but is {btc_qty}."

    # Check for crypto_buy transaction
    transactions = state.get("transactions", [])
    found_crypto_buy = False
    for t in transactions:
        t_type = t.get("type", "")
        t_desc = t.get("description", "")
        if t_type == "crypto_buy" and "Bitcoin" in t_desc:
            found_crypto_buy = True
            break

    if not found_crypto_buy:
        return False, "No transaction with type 'crypto_buy' and description containing 'Bitcoin' found."

    # Check BTC transactions array for a new buy entry
    btc_transactions = btc_holding.get("transactions", [])
    found_btc_buy = False
    for t in btc_transactions:
        if t.get("type") == "buy":
            found_btc_buy = True
            break

    if not found_btc_buy:
        return False, "No entry with type 'buy' found in BTC transactions array."

    return True, "Successfully bought $100 of BTC. USD decreased, BTC quantity increased, and transactions recorded."
