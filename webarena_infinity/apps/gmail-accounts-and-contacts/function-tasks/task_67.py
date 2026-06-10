import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if (contact.get("firstName") == "Test"
                and contact.get("lastName") == "User"
                and contact.get("email") == "test@example.com"):
            labels = contact.get("labels", [])
            if "clabel_3" in labels:
                return True, "Contact 'Test User' (test@example.com) exists and has label 'clabel_3' (Work)."
            return False, f"Contact 'Test User' found but labels are {labels}, expected 'clabel_3' to be present."
    return False, "Contact with firstName 'Test', lastName 'User', email 'test@example.com' not found."
