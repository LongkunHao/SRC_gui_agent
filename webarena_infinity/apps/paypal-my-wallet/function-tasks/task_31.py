import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    credit = state.get("paypalCredit")
    if not credit:
        return False, "paypalCredit not found in state."

    autopay_enabled = credit.get("autopayEnabled")
    if autopay_enabled is False:
        return True, "Autopay successfully disabled."
    return False, f"Expected autopayEnabled to be False, but got {autopay_enabled}."
