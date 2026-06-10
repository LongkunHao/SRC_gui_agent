import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Ben" and contact.get("lastName") == "Walker":
            website = contact.get("website", "")
            if website == "https://benwalker.com":
                return True, "Contact 'Ben Walker' has website 'https://benwalker.com'."
            return False, f"Contact 'Ben Walker' found but website is '{website}', expected 'https://benwalker.com'."
    return False, "Contact with firstName 'Ben' and lastName 'Walker' not found."
