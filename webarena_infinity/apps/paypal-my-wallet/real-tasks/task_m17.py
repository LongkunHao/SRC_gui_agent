import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    paypal_credit = state.get("paypalCredit")
    if paypal_credit is None:
        return False, "No paypalCredit found in state."

    autopay_amount = paypal_credit.get("autopayAmount")
    if autopay_amount != "statement":
        return False, (
            f"paypalCredit.autopayAmount is '{autopay_amount}', expected 'statement'."
        )

    return True, "PayPal Credit autopay has been successfully switched to statement balance."
