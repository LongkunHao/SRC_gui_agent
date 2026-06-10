import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check ETH quantity decreased from 0.85200
    crypto_holdings = state.get("cryptoHoldings", [])
    eth_holding = None
    for c in crypto_holdings:
        if c.get("symbol") == "ETH" or c.get("currency") == "ETH" or c.get("name", "").lower() == "ethereum":
            eth_holding = c
            break

    if eth_holding is None:
        return False, "No ETH crypto holding found."

    eth_qty = eth_holding.get("quantity", eth_holding.get("amount", 0))
    if eth_qty >= 0.85200:
        return False, f"ETH quantity should have decreased from 0.85200, but is {eth_qty}."

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
        return False, f"USD balance should have increased from 2847.63 after selling $50 of ETH, but is {usd_amount}."

    # Check for crypto_sell transaction containing 'Ethereum'
    transactions = state.get("transactions", [])
    found_crypto_sell = False
    for t in transactions:
        t_type = t.get("type", "")
        t_desc = t.get("description", "")
        if t_type == "crypto_sell" and "Ethereum" in t_desc:
            found_crypto_sell = True
            break

    if not found_crypto_sell:
        return False, "No transaction with type 'crypto_sell' and description containing 'Ethereum' found."

    # Check ETH transactions array for a new sell entry
    eth_transactions = eth_holding.get("transactions", [])
    found_eth_sell = False
    for t in eth_transactions:
        if t.get("type") == "sell":
            found_eth_sell = True
            break

    if not found_eth_sell:
        return False, "No entry with type 'sell' found in ETH transactions array."

    return True, "Successfully sold $50 of ETH. ETH quantity decreased, USD increased, and transactions recorded."
