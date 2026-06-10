import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Tony" and contact.get("lastName") == "Russo":
            return False, "Contact Tony Russo still exists but should have been deleted."
    return True, "No contact with firstName 'Tony', lastName 'Russo' exists."
