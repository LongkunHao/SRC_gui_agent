import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    login_settings = state.get("accountSettings", {}).get("loginSettings", {})
    remember_password = login_settings.get("rememberPassword")
    if remember_password is False:
        return True, "rememberPassword is False."
    return False, f"rememberPassword is {remember_password}, expected False."
