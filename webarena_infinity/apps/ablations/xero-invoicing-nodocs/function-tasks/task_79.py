import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    settings = state.get("settings", {})
    if settings.get("companyAddress") != "50 Symonds Street, Grafton, Auckland 1010, New Zealand":
        return False, f"Expected company address '50 Symonds Street, Grafton, Auckland 1010, New Zealand', got '{settings.get('companyAddress')}'"
    if settings.get("companyPhone") != "+64 9 373 7999":
        return False, f"Expected company phone '+64 9 373 7999', got '{settings.get('companyPhone')}'"
    return True, "Company address and phone updated correctly."
