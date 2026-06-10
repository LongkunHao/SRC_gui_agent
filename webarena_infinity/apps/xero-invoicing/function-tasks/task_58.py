import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    if settings.get("quotePrefix") != "QUOT-":
        return False, f"Quote prefix is '{settings.get('quotePrefix')}', expected 'QUOT-'."

    return True, "Quote prefix changed to 'QUOT-'."
