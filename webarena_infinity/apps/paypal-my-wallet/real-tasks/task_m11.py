import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check USD balance decreased by ~50
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break

    if usd_balance is None:
        errors.append("No USD balance found in state.")
    else:
        expected_balance = 2847.63 - 50
        if not (expected_balance - 5 <= usd_balance <= expected_balance + 5):
            errors.append(
                f"USD balance is {usd_balance}, expected approximately {expected_balance} "
                f"(original 2847.63 minus ~50)."
            )

    # Check ETH quantity increased from 0.85200
    crypto_holdings = state.get("cryptoHoldings", [])
    eth_holding = None
    for c in crypto_holdings:
        if c.get("symbol") == "ETH":
            eth_holding = c
            break

    if eth_holding is None:
        errors.append("No Ethereum (ETH) holding found in state.")
    else:
        eth_quantity = eth_holding.get("quantity", 0)
        if eth_quantity <= 0.85200:
            errors.append(
                f"ETH quantity is {eth_quantity}, expected it to have increased from 0.85200."
            )

    # Check for a crypto_buy transaction containing "Ethereum"
    transactions = state.get("transactions", [])
    found_crypto_buy = False
    for txn in transactions:
        if txn.get("type") == "crypto_buy" and "Ethereum" in txn.get("description", ""):
            found_crypto_buy = True
            break

    if not found_crypto_buy:
        errors.append(
            "No transaction with type 'crypto_buy' containing 'Ethereum' in description found."
        )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully invested $50 in Ethereum: USD balance decreased, ETH quantity increased, and crypto_buy transaction recorded."
