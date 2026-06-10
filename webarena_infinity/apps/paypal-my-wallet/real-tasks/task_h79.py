import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Step 1: BTC quantity should have decreased (from seed 0.04521)
    crypto_holdings = state.get("cryptoHoldings", [])
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
                f"after selling $150."
            )

    # Step 2: PayPal Credit balance should have decreased by $100
    credit = state.get("paypalCredit", {})
    expected_balance = 1245.67 - 100
    if abs(credit.get("currentBalance", 0) - expected_balance) > 1.0:
        errors.append(
            f"PayPal Credit balance is {credit.get('currentBalance')}, "
            f"expected ~{expected_balance} after paying $100."
        )
    if credit.get("lastPaymentAmount") != 100:
        errors.append(
            f"Last payment amount is {credit.get('lastPaymentAmount')}, expected 100."
        )

    # Step 3: Savings should have increased by $50
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("Savings account not found.")
    else:
        expected_savings = 12450.82 + 50
        if abs(savings.get("balance", 0) - expected_savings) > 1.0:
            errors.append(
                f"Savings balance is {savings.get('balance')}, expected ~{expected_savings} "
                f"after depositing $50."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Sold $150 BTC, paid $100 on PayPal Credit, deposited $50 into savings."
