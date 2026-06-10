import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if (contact.get("firstName") == "Alice"
                and contact.get("lastName") == "Wonderland"
                and contact.get("email") == "alice@wonderland.com"):
            return True, "Contact Alice Wonderland with email alice@wonderland.com exists."
    return False, "No contact found with firstName 'Alice', lastName 'Wonderland', email 'alice@wonderland.com'."
