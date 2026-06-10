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

    # Check currentBalance decreased from 1245.67 by ~200
    current_balance = paypal_credit.get("currentBalance")
    expected_balance = 1045.67  # 1245.67 - 200
    if current_balance is None:
        errors.append("paypalCredit.currentBalance is missing.")
    elif abs(current_balance - expected_balance) > 0.10:
        errors.append(
            f"paypalCredit.currentBalance is {current_balance}, expected ~{expected_balance} "
            f"(original 1245.67 minus 200 payment)."
        )

    # Check lastPaymentAmount == 200
    last_payment = paypal_credit.get("lastPaymentAmount")
    if last_payment is None:
        errors.append("paypalCredit.lastPaymentAmount is missing.")
    elif abs(last_payment - 200) > 0.10:
        errors.append(
            f"paypalCredit.lastPaymentAmount is {last_payment}, expected 200."
        )

    # Check autopayAmount == "full"
    autopay = paypal_credit.get("autopayAmount")
    if autopay is None:
        errors.append("paypalCredit.autopayAmount is missing.")
    elif autopay != "full":
        errors.append(
            f"paypalCredit.autopayAmount is '{autopay}', expected 'full'."
        )

    # Check USD balance decreased by 200
    balances = state.get("balances", [])
    usd_balance = None
    for bal in balances:
        if bal.get("currency") == "USD":
            usd_balance = bal.get("amount")
            break

    if usd_balance is None:
        errors.append("USD balance not found in state.")
    else:
        expected_usd = 2647.63  # 2847.63 - 200
        if abs(usd_balance - expected_usd) > 0.10:
            errors.append(
                f"USD balance is {usd_balance}, expected ~{expected_usd} "
                f"(original 2847.63 minus 200 credit payment)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully made $200 PayPal Credit payment and changed autopay to full balance."
