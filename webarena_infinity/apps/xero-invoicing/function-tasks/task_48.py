import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    if settings.get("showTaxColumn") is not False:
        return False, f"showTaxColumn is {settings.get('showTaxColumn')}, expected False."

    return True, "Show Tax Column disabled in invoice settings."
