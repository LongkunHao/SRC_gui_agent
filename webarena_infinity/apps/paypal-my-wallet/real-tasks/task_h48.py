import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    crypto_holdings = state.get("cryptoHoldings", [])

    # Worst performer by return % is PYUSD (0%).
    # Agent should have sold $100 of PYUSD.
    pyusd = None
    for c in crypto_holdings:
        if c.get("symbol") == "PYUSD":
            pyusd = c
            break

    if pyusd is None:
        errors.append("PYUSD not found in crypto holdings.")
    else:
        seed_quantity = 250.0
        if pyusd.get("quantity", 0) >= seed_quantity:
            errors.append(
                f"PYUSD quantity is {pyusd.get('quantity')}, expected < {seed_quantity} "
                f"after selling $100."
            )

        # Check for sell transaction
        pyusd_txns = pyusd.get("transactions", [])
        seed_tx_ids = {"ctx_012"}
        found_sell = False
        for tx in pyusd_txns:
            if tx.get("type") == "sell" and tx.get("id") not in seed_tx_ids:
                found_sell = True
                break
        if not found_sell:
            errors.append("No new sell transaction found in PYUSD's transaction history.")

    # Best performer by return % is BTC (60.22%).
    # Agent should have bought $100 of BTC.
    btc = None
    for c in crypto_holdings:
        if c.get("symbol") == "BTC":
            btc = c
            break

    if btc is None:
        errors.append("Bitcoin not found in crypto holdings.")
    else:
        seed_quantity = 0.04521
        if btc.get("quantity", 0) <= seed_quantity:
            errors.append(
                f"Bitcoin quantity is {btc.get('quantity')}, expected > {seed_quantity} "
                f"after investing $100."
            )

        btc_txns = btc.get("transactions", [])
        seed_tx_ids = {"ctx_001", "ctx_002", "ctx_003"}
        found_buy = False
        for tx in btc_txns:
            if tx.get("type") == "buy" and tx.get("id") not in seed_tx_ids:
                found_buy = True
                break
        if not found_buy:
            errors.append("No new buy transaction found in Bitcoin's transaction history.")

    if errors:
        return False, " ".join(errors)
    return True, "Sold $100 of worst performer (PYUSD) and invested $100 in best performer (BTC)."
