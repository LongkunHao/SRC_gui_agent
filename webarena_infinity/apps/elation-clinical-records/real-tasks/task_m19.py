import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Bergstrom":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Bergstrom'."

    patient_id = patient.get("id")
    notes = state.get("visitNotes", [])
    target_note = None
    for note in notes:
        if note.get("patientId") == patient_id and note.get("category") == "cat_002":
            target_note = note
            break

    if target_note is None:
        patient_notes = [(n.get("id"), n.get("category")) for n in notes if n.get("patientId") == patient_id]
        return False, f"Could not find a visit note with category='cat_002' (Telehealth) for patient Bergstrom (patientId={patient_id}). Current notes: {patient_notes}"

    return True, "Successfully verified that a visit note with Telehealth category was created for Thomas Bergstrom."
