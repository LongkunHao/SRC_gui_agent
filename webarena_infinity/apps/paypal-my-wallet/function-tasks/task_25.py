import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard", {})
    daily_atm_limit = debit_card.get("dailyATMLimit")

    if daily_atm_limit != 300:
        return False, f"paypalDebitCard.dailyATMLimit should be 300, but got {daily_atm_limit}."

    return True, "Daily ATM limit was successfully set to $300."
