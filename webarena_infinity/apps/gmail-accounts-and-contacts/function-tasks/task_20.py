import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    contacts = state.get("contacts", [])
    david_kim = None
    for contact in contacts:
        if contact.get("firstName") == "David" and contact.get("lastName") == "Kim":
            david_kim = contact
            break

    if david_kim is None:
        return False, "Contact 'David Kim' not found."

    contact_labels = david_kim.get("labels", [])
    if "clabel_2" not in contact_labels:
        return False, f"Contact 'David Kim' does not have 'clabel_2' (Friends) in labels. Current labels: {contact_labels}."

    return True, "Contact 'David Kim' has 'clabel_2' (Friends) in their labels."
