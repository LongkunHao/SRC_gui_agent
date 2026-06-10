import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    visit_notes = state.get("visitNotes", [])
    for note in visit_notes:
        if note.get("id") == "note_012":
            if note.get("status") != "signed":
                return False, f"Visit note note_012 has status '{note.get('status')}', expected 'signed'."
            if not note.get("signedAt"):
                return False, "Visit note note_012 has status 'signed' but signedAt is empty."
            return True, f"Visit note note_012 is signed with signedAt='{note.get('signedAt')}'."

    return False, "Visit note with id 'note_012' not found."
