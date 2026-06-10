import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Jake" and contact.get("lastName") == "Morrison":
            if contact.get("phone") == "+1 (415) 999-8888":
                return True, "Contact Jake Morrison has phone '+1 (415) 999-8888'."
            else:
                return False, f"Contact Jake Morrison found but phone is '{contact.get('phone')}', expected '+1 (415) 999-8888'."
    return False, "No contact found with firstName 'Jake', lastName 'Morrison'."
