import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "James" and contact.get("lastName") == "O'Brien":
            if contact.get("isStarred") is True:
                return True, "Contact James O'Brien has isStarred True."
            else:
                return False, f"Contact James O'Brien found but isStarred is {contact.get('isStarred')}, expected True."
    return False, "No contact found with firstName 'James', lastName \"O'Brien\"."
