import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    expected_content = (
        "Patient returns for 6-week follow-up. Reports improvement in back pain "
        "with physical therapy. Anxiety well-managed on current medication."
    )

    visit_notes = state.get("visitNotes", [])
    for note in visit_notes:
        if note.get("id") == "note_012":
            blocks = note.get("blocks", [])
            for block in blocks:
                if block.get("type") == "hpi" and block.get("content") == expected_content:
                    return True, "Found HPI block in note_012 with the expected content."
            return False, "No HPI block with the expected content found in note_012."

    return False, "Visit note with id 'note_012' not found."
