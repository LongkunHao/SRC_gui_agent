import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Priya" and contact.get("lastName") == "Sharma":
            expected = "priya.personal@outlook.com"
            if contact.get("secondaryEmail") == expected:
                return True, "Contact Priya Sharma has secondaryEmail 'priya.personal@outlook.com'."
            else:
                return False, f"Contact Priya Sharma found but secondaryEmail is '{contact.get('secondaryEmail')}', expected '{expected}'."
    return False, "No contact found with firstName 'Priya', lastName 'Sharma'."
