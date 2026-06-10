import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    if settings.get("defaultTaxMode") != "inclusive":
        return False, f"Default tax mode is '{settings.get('defaultTaxMode')}', expected 'inclusive'."

    return True, "Default tax mode changed to inclusive."
