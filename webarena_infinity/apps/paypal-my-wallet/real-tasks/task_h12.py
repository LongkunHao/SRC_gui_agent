import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check savings balance increased from 12450.82 by 500
    savings = state.get("savingsAccount")
    if savings is None:
        errors.append("No savingsAccount found in state.")
    else:
        savings_balance = savings.get("balance")
        expected_savings = 12950.82  # 12450.82 + 500
        if savings_balance is None:
            errors.append("savingsAccount.balance is missing.")
        elif abs(savings_balance - expected_savings) > 0.10:
            errors.append(
                f"savingsAccount.balance is {savings_balance}, expected ~{expected_savings} "
                f"(original 12450.82 plus 500 deposit)."
            )

    # Check USD balance decreased by 500
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2347.63  # 2847.63 - 500
        if abs(usd_balance - expected_usd) > 0.10:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 500 savings deposit)."
            )

    # Check debit card ATM limit changed to 1000
    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        errors.append("No paypalDebitCard found in state.")
    else:
        atm_limit = debit_card.get("dailyATMLimit")
        if atm_limit is None:
            errors.append("paypalDebitCard.dailyATMLimit is missing.")
        elif atm_limit != 1000:
            errors.append(
                f"paypalDebitCard.dailyATMLimit is {atm_limit}, expected 1000."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully deposited $500 into savings and set debit card ATM limit to $1,000."
