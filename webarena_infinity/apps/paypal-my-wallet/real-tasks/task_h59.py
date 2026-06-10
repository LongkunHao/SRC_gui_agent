import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    crypto_holdings = state.get("cryptoHoldings", [])

    # Check ETH quantity decreased (from seed 0.852)
    eth = None
    for c in crypto_holdings:
        if c.get("symbol") == "ETH":
            eth = c
            break

    if eth is None:
        errors.append("Ethereum not found in crypto holdings.")
    else:
        seed_quantity = 0.852
        if eth.get("quantity", 0) >= seed_quantity:
            errors.append(
                f"Ethereum quantity is {eth.get('quantity')}, expected < {seed_quantity} "
                f"after selling $100."
            )

    # Check BTC quantity decreased (from seed 0.04521)
    btc = None
    for c in crypto_holdings:
        if c.get("symbol") == "BTC":
            btc = c
            break

    if btc is None:
        errors.append("Bitcoin not found in crypto holdings.")
    else:
        seed_quantity = 0.04521
        if btc.get("quantity", 0) >= seed_quantity:
            errors.append(
                f"Bitcoin quantity is {btc.get('quantity')}, expected < {seed_quantity} "
                f"after selling $100."
            )

    # Check credit balance decreased by $200 (from 1245.67 to ~1045.67)
    credit = state.get("paypalCredit")
    if credit is None:
        errors.append("PayPal Credit not found.")
    else:
        expected_balance = 1245.67 - 200
        if abs(credit.get("currentBalance", 0) - expected_balance) > 1.0:
            errors.append(
                f"PayPal Credit balance is {credit.get('currentBalance')}, "
                f"expected ~{expected_balance} after paying $200."
            )
        if credit.get("lastPaymentAmount") != 200:
            errors.append(
                f"Last payment amount is {credit.get('lastPaymentAmount')}, expected 200."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Sold $100 ETH and $100 BTC, then paid $200 toward PayPal Credit."
