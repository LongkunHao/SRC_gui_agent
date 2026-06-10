import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    contacts = state.get("contacts", [])
    sarah_chen = None
    for contact in contacts:
        if contact.get("firstName") == "Sarah" and contact.get("lastName") == "Chen":
            sarah_chen = contact
            break

    if sarah_chen is None:
        return False, "Contact 'Sarah Chen' not found."

    contact_labels = sarah_chen.get("labels", [])
    if "clabel_3" in contact_labels:
        return False, f"Contact 'Sarah Chen' still has 'clabel_3' (Work) in labels. Current labels: {contact_labels}."

    return True, "Contact 'Sarah Chen' does not have 'clabel_3' (Work) in their labels."
