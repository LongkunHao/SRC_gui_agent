import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    paypal_credit = state.get("paypalCredit")
    if paypal_credit is None:
        return False, "No paypalCredit found in state."

    # Check currentBalance decreased from 1245.67 by ~100
    current_balance = paypal_credit.get("currentBalance")
    expected_balance = 1145.67
    if current_balance is None:
        errors.append("paypalCredit.currentBalance is missing.")
    elif abs(current_balance - expected_balance) > 0.02:
        errors.append(
            f"paypalCredit.currentBalance is {current_balance}, expected ~{expected_balance} "
            f"(original 1245.67 minus 100)."
        )

    # Check availableCredit increased accordingly
    available_credit = paypal_credit.get("availableCredit")
    expected_available = 3854.33  # 5000 - 1145.67
    if available_credit is None:
        errors.append("paypalCredit.availableCredit is missing.")
    elif abs(available_credit - expected_available) > 0.02:
        errors.append(
            f"paypalCredit.availableCredit is {available_credit}, expected ~{expected_available}."
        )

    # Check lastPaymentAmount is 100
    last_payment = paypal_credit.get("lastPaymentAmount")
    if last_payment is None:
        errors.append("paypalCredit.lastPaymentAmount is missing.")
    elif abs(last_payment - 100) > 0.02:
        errors.append(
            f"paypalCredit.lastPaymentAmount is {last_payment}, expected 100."
        )

    # Check USD balance decreased from 2847.63
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2747.63  # 2847.63 - 100
        if abs(usd_balance - expected_usd) > 0.02:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 100 payment)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully paid $100 toward PayPal Credit balance."
