import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    login_settings = state.get("accountSettings", {}).get("loginSettings", {})
    auto_sign_in = login_settings.get("autoSignIn")
    if auto_sign_in is False:
        return True, "autoSignIn is False."
    return False, f"autoSignIn is {auto_sign_in}, expected False."
