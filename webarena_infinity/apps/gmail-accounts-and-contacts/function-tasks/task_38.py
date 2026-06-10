import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    account_settings = state.get("accountSettings", {})
    contacts_sort_by = account_settings.get("contactsSortBy")
    if contacts_sort_by == "lastName":
        return True, "contactsSortBy is set to 'lastName'."
    return False, f"contactsSortBy is '{contacts_sort_by}', expected 'lastName'."
