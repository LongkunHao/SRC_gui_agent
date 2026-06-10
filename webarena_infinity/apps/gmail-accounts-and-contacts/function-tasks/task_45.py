import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    current_user = state.get("currentUser", {})
    recovery_phone = current_user.get("recoveryPhone")
    if recovery_phone == "+1 (415) 555-9999":
        return True, "currentUser.recoveryPhone is '+1 (415) 555-9999'."
    return False, f"currentUser.recoveryPhone is '{recovery_phone}', expected '+1 (415) 555-9999'."
