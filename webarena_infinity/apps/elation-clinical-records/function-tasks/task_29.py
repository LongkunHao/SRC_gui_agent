import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patient = next((p for p in state["patients"] if p["lastName"] == "Bergstrom"), None)
    if not patient:
        return False, "Patient Thomas Bergstrom not found."

    for note in state.get("visitNotes", []):
        if note.get("patientId") == patient["id"] and note.get("category") == "cat_002":
            return True, "Found visit note for patient Bergstrom with category cat_002 (Telehealth)."

    return False, "No visit note found for patient Thomas Bergstrom with category cat_002 (Telehealth)."
