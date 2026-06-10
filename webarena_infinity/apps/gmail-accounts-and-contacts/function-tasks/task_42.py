import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    collaboration = state.get("accountSettings", {}).get("collaborationSettings", {})
    show_contact_info = collaboration.get("showContactInfo")
    if show_contact_info is False:
        return True, "showContactInfo is False."
    return False, f"showContactInfo is {show_contact_info}, expected False."
