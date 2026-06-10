import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Sarah" and contact.get("lastName") == "Chen":
            if contact.get("jobTitle") == "Chief Product Officer":
                return True, "Contact Sarah Chen has jobTitle 'Chief Product Officer'."
            else:
                return False, f"Contact Sarah Chen found but jobTitle is '{contact.get('jobTitle')}', expected 'Chief Product Officer'."
    return False, "No contact found with firstName 'Sarah', lastName 'Chen'."
