import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    login_settings = state.get("accountSettings", {}).get("loginSettings", {})
    two_factor_method = login_settings.get("twoFactorMethod")
    if two_factor_method == "security_key":
        return True, "twoFactorMethod is 'security_key'."
    return False, f"twoFactorMethod is '{two_factor_method}', expected 'security_key'."
