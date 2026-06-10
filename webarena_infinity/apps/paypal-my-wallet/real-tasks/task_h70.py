import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    credit = state.get("paypalCredit", {})

    # Seed balance is $1,245.67 which is > $1,000, so agent should pay $500.
    # After payment: balance should be ~$745.67.
    expected_balance = 1245.67 - 500
    actual_balance = credit.get("currentBalance", 0)
    if abs(actual_balance - expected_balance) > 1.0:
        errors.append(
            f"PayPal Credit balance is {actual_balance}, expected ~{expected_balance} "
            f"after $500 payment (balance was > $1,000)."
        )

    # Last payment should be $500
    if credit.get("lastPaymentAmount") != 500:
        errors.append(
            f"Last payment amount is {credit.get('lastPaymentAmount')}, expected 500."
        )

    # Autopay should be disabled
    if credit.get("autopayEnabled") is not False:
        errors.append("Autopay should be disabled.")

    if errors:
        return False, " ".join(errors)
    return True, "Paid $500 on PayPal Credit (balance was > $1,000) and disabled autopay."
