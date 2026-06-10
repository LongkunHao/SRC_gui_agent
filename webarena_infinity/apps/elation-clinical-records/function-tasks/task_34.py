import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    visit_notes = state.get("visitNotes", [])
    for note in visit_notes:
        if note.get("id") == "note_012":
            blocks = note.get("blocks", [])
            for block in blocks:
                if block.get("type") == "hpi":
                    return False, "Found an HPI block in note_012, but it should have been removed."
            return True, "No HPI block found in note_012 as expected."

    return False, "Visit note with id 'note_012' not found."
