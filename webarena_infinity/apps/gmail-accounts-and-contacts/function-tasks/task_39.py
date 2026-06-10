import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    account_settings = state.get("accountSettings", {})
    contacts_display_order = account_settings.get("contactsDisplayOrder")
    if contacts_display_order == "lastFirst":
        return True, "contactsDisplayOrder is set to 'lastFirst'."
    return False, f"contactsDisplayOrder is '{contacts_display_order}', expected 'lastFirst'."
