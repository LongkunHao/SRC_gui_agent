import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # Check PayPal Credit autopay settings
    paypal_credit = state.get("paypalCredit")
    if paypal_credit is None:
        errors.append("No paypalCredit found in state.")
    else:
        if paypal_credit.get("autopayEnabled") is not True:
            errors.append(
                f"paypalCredit.autopayEnabled is {paypal_credit.get('autopayEnabled')}, expected True."
            )

        autopay_amount = paypal_credit.get("autopayAmount", "")
        if autopay_amount != "full":
            errors.append(
                f"paypalCredit.autopayAmount is '{autopay_amount}', expected 'full'."
            )

    # Check debit card spending limit
    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        errors.append("No paypalDebitCard found in state.")
    else:
        limit = debit_card.get("dailySpendingLimit")
        if limit != 7000:
            errors.append(
                f"paypalDebitCard.dailySpendingLimit is {limit}, expected 7000."
            )

    if errors:
        return False, " ".join(errors)
    return True, "PayPal Credit autopay set to full balance and debit card daily spending limit raised to $7,000."
