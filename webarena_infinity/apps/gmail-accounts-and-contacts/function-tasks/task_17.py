import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    labels = state.get("contactLabels", [])
    label_names = [label.get("name") for label in labels]
    if "Book Club" in label_names:
        return False, "Label 'Book Club' still exists but should have been deleted."
    contacts = state.get("contacts", [])
    for contact in contacts:
        contact_labels = contact.get("labels", [])
        if "clabel_8" in contact_labels:
            name = f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip()
            return False, f"Contact '{name}' still has 'clabel_8' in their labels array, but Book Club (clabel_8) was deleted."
    return True, "Label 'Book Club' does not exist and no contact has 'clabel_8' in their labels."
