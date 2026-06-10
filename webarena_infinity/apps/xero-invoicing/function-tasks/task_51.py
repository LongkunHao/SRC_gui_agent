import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    settings = state.get("invoiceSettings", {})

    if settings.get("creditNotePrefix") != "CR-":
        return False, f"Credit note prefix is '{settings.get('creditNotePrefix')}', expected 'CR-'."

    return True, "Credit note prefix changed to 'CR-'."
