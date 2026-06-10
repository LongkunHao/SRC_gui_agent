import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Tom" and contact.get("lastName") == "Bradley":
            return False, "Contact Tom Bradley still exists but should have been deleted."
    return True, "No contact with firstName 'Tom', lastName 'Bradley' exists."
