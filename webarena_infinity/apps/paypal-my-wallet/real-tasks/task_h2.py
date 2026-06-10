import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check SOL quantity increased from 0
    crypto_holdings = state.get("cryptoHoldings", [])
    sol = None
    for c in crypto_holdings:
        if c.get("symbol") == "SOL":
            sol = c
            break

    if sol is None:
        errors.append("Solana (SOL) not found in crypto holdings.")
    else:
        if sol.get("quantity", 0) <= 0:
            errors.append(
                f"SOL quantity is {sol.get('quantity', 0)}, expected > 0 after buying $25 worth."
            )

    # Check USD balance decreased from 2847.63
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        actual_usd = usd_bal.get("amount", 0)
        if actual_usd >= 2847.63:
            errors.append(
                f"USD balance is {actual_usd}, expected it to have decreased from seed value 2847.63."
            )

    # Check for crypto_buy transaction mentioning Solana
    transactions = state.get("transactions", [])
    buy_txn = None
    for t in transactions:
        if t.get("type") == "crypto_buy":
            desc = t.get("description", "").lower()
            if "solana" in desc or "sol" in desc:
                buy_txn = t
                break

    if buy_txn is None:
        errors.append("No crypto_buy transaction found with 'Solana' in description.")

    if errors:
        return False, " ".join(errors)
    return True, "Successfully bought $25 worth of Solana. SOL quantity > 0 and USD balance decreased."
