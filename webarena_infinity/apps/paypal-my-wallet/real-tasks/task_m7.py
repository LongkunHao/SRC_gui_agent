import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard")
    if debit_card is None:
        return False, "No PayPal debit card found in state."

    atm_limit = debit_card.get("dailyATMLimit")
    if atm_limit != 200:
        return False, (
            f"Debit card dailyATMLimit is {atm_limit}, expected 200."
        )

    return True, "Debit card daily ATM withdrawal limit successfully lowered to $200."
