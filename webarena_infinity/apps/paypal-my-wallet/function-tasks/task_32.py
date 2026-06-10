import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    credit = state.get("paypalCredit")
    if not credit:
        return False, "paypalCredit not found in state."

    autopay_amount = credit.get("autopayAmount")
    if autopay_amount == "full":
        return True, "Autopay successfully set to full balance."
    return False, f"Expected autopayAmount to be 'full', but got '{autopay_amount}'."
