import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    paypal_credit = state.get("paypalCredit")
    if paypal_credit is None:
        return False, "paypalCredit not found in state."

    autopay_amount = paypal_credit.get("autopayAmount")
    if autopay_amount != "full":
        return False, f"PayPal Credit autopayAmount is '{autopay_amount}', expected 'full'."

    return True, "PayPal Credit is set to automatically pay the full balance."
