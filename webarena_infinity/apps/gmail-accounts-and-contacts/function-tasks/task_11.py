import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    contacts = state.get("contacts", [])
    for contact in contacts:
        if contact.get("firstName") == "Emily" and contact.get("lastName") == "Rodriguez":
            expected_notes = "Key investor contact for Series C round."
            if contact.get("notes") == expected_notes:
                return True, "Contact Emily Rodriguez has the expected notes."
            else:
                return False, f"Contact Emily Rodriguez found but notes is '{contact.get('notes')}', expected '{expected_notes}'."
    return False, "No contact found with firstName 'Emily', lastName 'Rodriguez'."
