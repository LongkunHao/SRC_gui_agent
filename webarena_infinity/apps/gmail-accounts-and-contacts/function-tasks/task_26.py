import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    target_email = "tina.marshall@designhub.com"

    other_contacts = state.get("otherContacts", [])
    for oc in other_contacts:
        if oc.get("email") == target_email:
            return False, f"Other contact with email '{target_email}' still exists in otherContacts."

    contacts = state.get("contacts", [])
    found_in_main = False
    for contact in contacts:
        if contact.get("email") == target_email:
            found_in_main = True
            break

    if not found_in_main:
        return False, f"No main contact with email '{target_email}' found in contacts."

    return True, f"No other contact with email '{target_email}' in otherContacts and main contact exists in contacts."
