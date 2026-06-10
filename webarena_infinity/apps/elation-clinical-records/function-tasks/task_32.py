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
                if block.get("type") == "pe" and "Alert, oriented" in block.get("content", ""):
                    return True, "Found PE block in note_012 containing 'Alert, oriented'."
            return False, "No block with type 'pe' containing 'Alert, oriented' found in note_012."

    return False, "Visit note with id 'note_012' not found."
