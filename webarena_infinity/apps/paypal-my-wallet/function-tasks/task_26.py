import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard", {})
    cash_back_enabled = debit_card.get("cashBackEnabled")

    if cash_back_enabled is not False:
        return False, f"paypalDebitCard.cashBackEnabled should be false, but got {cash_back_enabled}."

    return True, "Cash back was successfully disabled."
