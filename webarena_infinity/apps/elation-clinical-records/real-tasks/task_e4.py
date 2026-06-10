import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    notes = state.get("visitNotes", [])
    target_note = None
    for note in notes:
        if note.get("id") == "note_012":
            target_note = note
            break

    if target_note is None:
        return False, "Could not find visit note with id='note_012'."

    status = target_note.get("status", "")
    if status != "signed":
        return False, f"Note note_012 status is '{status}', expected 'signed'."

    signed_at = target_note.get("signedAt", "")
    if not signed_at:
        return False, "Note note_012 has status 'signed' but signedAt is empty."

    return True, "Successfully verified that David Kowalski's draft visit note (note_012) is signed."
