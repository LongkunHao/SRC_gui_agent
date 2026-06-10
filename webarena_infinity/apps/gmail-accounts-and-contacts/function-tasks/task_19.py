import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    labels = state.get("contactLabels", [])
    for label in labels:
        if label.get("name") == "Travel Contacts":
            return False, "Label 'Travel Contacts' still exists."

    contacts = state.get("contacts", [])
    for contact in contacts:
        contact_labels = contact.get("labels", [])
        if "clabel_11" in contact_labels:
            name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip()
            return False, f"Contact '{name}' still has 'clabel_11' (Travel Contacts) in their labels."

    return True, "Label 'Travel Contacts' does not exist and no contact has 'clabel_11' in their labels."
