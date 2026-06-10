import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    account_settings = state.get("accountSettings", {})
    auto_save_contacts = account_settings.get("autoSaveContacts")
    if auto_save_contacts is False:
        return True, "autoSaveContacts is False."
    return False, f"autoSaveContacts is {auto_save_contacts}, expected False."
