import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    paypal_credit = state.get("paypalCredit")
    if paypal_credit is None:
        return False, "paypalCredit not found in state."

    if paypal_credit.get("autopayEnabled") is not False:
        return False, f"Autopay is still enabled (autopayEnabled={paypal_credit.get('autopayEnabled')})."

    return True, "Autopay on PayPal Credit has been turned off."
