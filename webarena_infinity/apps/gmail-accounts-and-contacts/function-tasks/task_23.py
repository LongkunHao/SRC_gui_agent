import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    contacts = state.get("contacts", [])
    chris_evans = None
    for contact in contacts:
        if contact.get("firstName") == "Chris" and contact.get("lastName") == "Evans":
            chris_evans = contact
            break

    if chris_evans is None:
        return False, "Contact 'Chris Evans' not found."

    contact_labels = chris_evans.get("labels", [])
    if "clabel_5" in contact_labels:
        return False, f"Contact 'Chris Evans' still has 'clabel_5' (Gym Buddies) in labels. Current labels: {contact_labels}."

    return True, "Contact 'Chris Evans' does not have 'clabel_5' (Gym Buddies) in their labels."
