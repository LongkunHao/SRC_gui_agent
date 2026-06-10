import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Samantha" and contact.get("lastName") == "Lee":
            birthday = contact.get("birthday", "")
            if birthday == "1993-05-20":
                return True, "Contact 'Samantha Lee' has birthday '1993-05-20'."
            return False, f"Contact 'Samantha Lee' found but birthday is '{birthday}', expected '1993-05-20'."
    return False, "Contact with firstName 'Samantha' and lastName 'Lee' not found."
