import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    debit_card = state.get("paypalDebitCard", {})
    direct_deposit = debit_card.get("directDeposit", {})
    enabled = direct_deposit.get("enabled")

    if enabled is not False:
        return False, f"paypalDebitCard.directDeposit.enabled should be false, but got {enabled}."

    return True, "Direct deposit was successfully disabled."
