import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check SOL quantity increased from 0
    crypto_holdings = state.get("cryptoHoldings", [])
    sol_holding = None
    for c in crypto_holdings:
        if c.get("symbol") == "SOL" or c.get("currency") == "SOL" or c.get("name", "").lower() == "solana":
            sol_holding = c
            break

    if sol_holding is None:
        return False, "No SOL crypto holding found."

    sol_qty = sol_holding.get("quantity", sol_holding.get("amount", 0))
    if sol_qty <= 0:
        return False, f"SOL quantity should have increased from 0, but is {sol_qty}."

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
        return False, f"USD balance should have decreased from 2847.63 after buying $25 of SOL, but is {usd_amount}."

    # Check for crypto_buy transaction containing 'Solana'
    transactions = state.get("transactions", [])
    found_crypto_buy = False
    for t in transactions:
        t_type = t.get("type", "")
        t_desc = t.get("description", "")
        if t_type == "crypto_buy" and "Solana" in t_desc:
            found_crypto_buy = True
            break

    if not found_crypto_buy:
        return False, "No transaction with type 'crypto_buy' and description containing 'Solana' found."

    return True, "Successfully bought $25 of SOL. SOL quantity increased from 0, USD decreased, and transaction recorded."
