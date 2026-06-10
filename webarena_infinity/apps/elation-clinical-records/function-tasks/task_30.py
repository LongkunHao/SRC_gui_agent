import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patient = next((p for p in state["patients"] if p["lastName"] == "Henderson"), None)
    if not patient:
        return False, "Patient Robert Henderson not found."

    for note in state.get("visitNotes", []):
        if note.get("patientId") == patient["id"] and note.get("templateUsed") == "tmpl_006":
            return True, "Found visit note for patient Henderson with templateUsed tmpl_006 (Diabetes Management)."

    return False, "No visit note found for patient Robert Henderson with templateUsed tmpl_006 (Diabetes Management)."
