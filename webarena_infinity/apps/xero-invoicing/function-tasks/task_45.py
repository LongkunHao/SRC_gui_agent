import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    if settings.get("invoiceNextNumber") != 100:
        return False, f"Invoice next number is {settings.get('invoiceNextNumber')}, expected 100."

    return True, "Invoice next number changed to 100."
