import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    if settings.get("invoicePrefix") != "TAX-":
        return False, f"Invoice prefix is '{settings.get('invoicePrefix')}', expected 'TAX-'."

    return True, "Invoice prefix changed to 'TAX-'."
