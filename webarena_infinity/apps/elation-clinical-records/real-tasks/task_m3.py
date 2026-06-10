import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Sharma":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Sharma'."

    patient_id = patient.get("id")
    notes = state.get("visitNotes", [])
    target_note = None
    for note in notes:
        if note.get("patientId") == patient_id and note.get("format") == "simple":
            target_note = note
            break

    if target_note is None:
        patient_notes = [(n.get("id"), n.get("format")) for n in notes if n.get("patientId") == patient_id]
        return False, f"Could not find a visit note with format='simple' for patient Sharma (patientId={patient_id}). Current notes: {patient_notes}"

    return True, "Successfully verified that a new visit note with Simple Note format was created for Priya Sharma."
