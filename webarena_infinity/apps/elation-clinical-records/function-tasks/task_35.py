import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    visit_notes = state.get("visitNotes", [])
    for note in visit_notes:
        if note.get("id") == "note_012":
            billing_items = note.get("billingItems", [])
            for item in billing_items:
                if item.get("cptCode") == "99213":
                    return True, "Found billing item with cptCode '99213' in note_012."
            return False, "No billing item with cptCode '99213' found in note_012."

    return False, "Visit note with id 'note_012' not found."
