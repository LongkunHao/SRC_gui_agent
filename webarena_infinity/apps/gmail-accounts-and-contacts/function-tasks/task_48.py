import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    login_settings = state.get("accountSettings", {}).get("loginSettings", {})
    two_factor_enabled = login_settings.get("twoFactorEnabled")
    if two_factor_enabled is False:
        return True, "twoFactorEnabled is False."
    return False, f"twoFactorEnabled is {two_factor_enabled}, expected False."
