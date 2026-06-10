import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Marcus" and contact.get("lastName") == "Williams":
            if contact.get("company") == "DesignHub International":
                return True, "Contact Marcus Williams has company 'DesignHub International'."
            else:
                return False, f"Contact Marcus Williams found but company is '{contact.get('company')}', expected 'DesignHub International'."
    return False, "No contact found with firstName 'Marcus', lastName 'Williams'."
