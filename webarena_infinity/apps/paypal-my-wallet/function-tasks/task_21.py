import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check LTC quantity decreased from 5.23400
    crypto_holdings = state.get("cryptoHoldings", [])
    ltc_holding = None
    for c in crypto_holdings:
        if c.get("symbol") == "LTC" or c.get("currency") == "LTC" or c.get("name", "").lower() == "litecoin":
            ltc_holding = c
            break

    if ltc_holding is None:
        return False, "No LTC crypto holding found."

    ltc_qty = ltc_holding.get("quantity", ltc_holding.get("amount", 0))
    if ltc_qty >= 5.23400:
        return False, f"LTC quantity should have decreased from 5.23400, but is {ltc_qty}."

    # Check USD balance increased from 2847.63
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b
            break

    if usd_balance is None:
        return False, "No USD balance entry found."

    usd_amount = usd_balance.get("amount", 0)
    if usd_amount <= 2847.63:
        return False, f"USD balance should have increased from 2847.63 after selling $100 of LTC, but is {usd_amount}."

    # Check for crypto_sell transaction containing 'Litecoin'
    transactions = state.get("transactions", [])
    found_crypto_sell = False
    for t in transactions:
        t_type = t.get("type", "")
        t_desc = t.get("description", "")
        if t_type == "crypto_sell" and "Litecoin" in t_desc:
            found_crypto_sell = True
            break

    if not found_crypto_sell:
        return False, "No transaction with type 'crypto_sell' and description containing 'Litecoin' found."

    # Check LTC transactions array for a new sell entry
    ltc_transactions = ltc_holding.get("transactions", [])
    found_ltc_sell = False
    for t in ltc_transactions:
        if t.get("type") == "sell":
            found_ltc_sell = True
            break

    if not found_ltc_sell:
        return False, "No entry with type 'sell' found in LTC transactions array."

    return True, "Successfully sold $100 of LTC. LTC quantity decreased, USD increased, and transactions recorded."
