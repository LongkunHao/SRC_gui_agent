import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    contacts = state.get("contacts", [])
    kevin_zhao = None
    for contact in contacts:
        if contact.get("firstName") == "Kevin" and contact.get("lastName") == "Zhao":
            kevin_zhao = contact
            break

    if kevin_zhao is None:
        return False, "Contact 'Kevin Zhao' not found."

    contact_labels = kevin_zhao.get("labels", [])
    if "clabel_4" not in contact_labels:
        return False, f"Contact 'Kevin Zhao' does not have 'clabel_4' (VIP Clients) in labels. Current labels: {contact_labels}."

    return True, "Contact 'Kevin Zhao' has 'clabel_4' (VIP Clients) in their labels."
