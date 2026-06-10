import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        return False, "No PayPal debit card found in state."

    if debit_card.get("cashBackEnabled") is not False:
        return False, f"Cash back is still enabled on the debit card (cashBackEnabled={debit_card.get('cashBackEnabled')})."

    return True, "Cash back has been successfully disabled on the debit card."
