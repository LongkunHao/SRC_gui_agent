import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check PayPal Credit current balance decreased by ~35
    paypal_credit = state.get("paypalCredit")
    if paypal_credit is None:
        errors.append("No paypalCredit found in state.")
    else:
        current_balance = paypal_credit.get("currentBalance")
        expected_balance = 1245.67 - 35.0
        if current_balance is None:
            errors.append("paypalCredit.currentBalance is missing.")
        elif abs(current_balance - expected_balance) > 1.0:
            errors.append(
                f"PayPal Credit currentBalance is {current_balance}, expected approximately "
                f"{expected_balance} (original 1245.67 minus 35)."
            )

        # Check lastPaymentAmount == 35
        last_payment = paypal_credit.get("lastPaymentAmount")
        if last_payment is None:
            errors.append("paypalCredit.lastPaymentAmount is missing.")
        else:
            try:
                if abs(float(last_payment) - 35.0) > 0.01:
                    errors.append(
                        f"paypalCredit.lastPaymentAmount is {last_payment}, expected 35."
                    )
            except (ValueError, TypeError):
                errors.append(
                    f"paypalCredit.lastPaymentAmount is '{last_payment}', expected 35."
                )

    # Check USD balance decreased by ~35
    balances = state.get("balances", [])
    usd_balance = None
    for b in balances:
        if b.get("currency") == "USD":
            usd_balance = b.get("amount")
            break

    if usd_balance is None:
        errors.append("No USD balance found in state.")
    else:
        expected_usd = 2847.63 - 35.0
        if abs(usd_balance - expected_usd) > 5.0:
            errors.append(
                f"USD balance is {usd_balance}, expected approximately {expected_usd} "
                f"(original 2847.63 minus 35)."
            )

    if errors:
        return False, " ".join(errors)
    return True, "Successfully paid the minimum amount due ($35) on PayPal Credit: credit balance decreased, lastPaymentAmount is 35, and USD balance decreased."
