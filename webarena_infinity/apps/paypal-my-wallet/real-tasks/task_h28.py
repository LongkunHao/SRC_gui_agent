import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check savings decreased by $3,000 from 12450.82
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("No savingsAccount found.")
    else:
        expected_savings = round(12450.82 - 3000, 2)
        actual_savings = savings.get("balance", 0)
        if abs(actual_savings - expected_savings) > 5.0:
            errors.append(
                f"Savings balance is {actual_savings}, expected ~{expected_savings} "
                f"after withdrawing $3,000."
            )

    # Check BTC quantity increased
    crypto_holdings = state.get("cryptoHoldings", [])
    btc = None
    eth = None
    for c in crypto_holdings:
        if c.get("symbol") == "BTC":
            btc = c
        elif c.get("symbol") == "ETH":
            eth = c

    if btc is None:
        errors.append("Bitcoin not found in crypto holdings.")
    else:
        if btc.get("quantity", 0) <= 0.04521:
            errors.append(
                f"Bitcoin quantity is {btc.get('quantity')}, expected > 0.04521 "
                f"after investing $100."
            )

    if eth is None:
        errors.append("Ethereum not found in crypto holdings.")
    else:
        if eth.get("quantity", 0) <= 0.85200:
            errors.append(
                f"Ethereum quantity is {eth.get('quantity')}, expected > 0.85200 "
                f"after investing $100."
            )

    # USD balance: seed 2847.63 + 3000 (from savings) - 100 (BTC) - 100 (ETH) = 5647.63
    balances = state.get("balances", [])
    usd_bal = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_bal = b
            break

    if usd_bal is None:
        errors.append("USD balance not found.")
    else:
        expected_usd = round(2847.63 + 3000 - 100 - 100, 2)
        if abs(usd_bal.get("amount", 0) - expected_usd) > 10.0:
            errors.append(
                f"USD balance is {usd_bal.get('amount')}, expected ~{expected_usd}."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully withdrew $3,000 from savings and invested $100 each in BTC and ETH."
