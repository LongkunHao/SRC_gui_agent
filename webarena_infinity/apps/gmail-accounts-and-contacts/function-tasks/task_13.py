import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Dr. Patricia" and contact.get("lastName") == "Nguyen":
            expected = "1200 California St, San Francisco, CA 94109"
            if contact.get("address") == expected:
                return True, "Contact Dr. Patricia Nguyen has the expected address."
            else:
                return False, f"Contact Dr. Patricia Nguyen found but address is '{contact.get('address')}', expected '{expected}'."
    return False, "No contact found with firstName 'Dr. Patricia', lastName 'Nguyen'."
