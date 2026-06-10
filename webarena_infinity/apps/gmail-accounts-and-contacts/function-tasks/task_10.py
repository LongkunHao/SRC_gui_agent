import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "David" and contact.get("lastName") == "Kim":
            if contact.get("isStarred") is True:
                return True, "Contact David Kim has isStarred True."
            else:
                return False, f"Contact David Kim found but isStarred is {contact.get('isStarred')}, expected True."
    return False, "No contact found with firstName 'David', lastName 'Kim'."
