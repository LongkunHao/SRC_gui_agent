import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    current_user = state.get("currentUser", {})
    recovery_email = current_user.get("recoveryEmail")
    if recovery_email == "alex.new.recovery@proton.me":
        return True, "currentUser.recoveryEmail is 'alex.new.recovery@proton.me'."
    return False, f"currentUser.recoveryEmail is '{recovery_email}', expected 'alex.new.recovery@proton.me'."
