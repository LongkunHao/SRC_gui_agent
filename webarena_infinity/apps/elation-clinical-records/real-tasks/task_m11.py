import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Zhao":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Zhao'."

    patient_id = patient.get("id")
    notes = state.get("visitNotes", [])

    # Zhao already has note_010 with category=cat_003 and templateUsed=tmpl_001
    # We need to find a NEW note (different ID) with those same values
    target_note = None
    for note in notes:
        if (note.get("patientId") == patient_id
                and note.get("category") == "cat_003"
                and note.get("templateUsed") == "tmpl_001"
                and note.get("id") != "note_010"):
            target_note = note
            break

    if target_note is None:
        patient_notes = [(n.get("id"), n.get("category"), n.get("templateUsed")) for n in notes if n.get("patientId") == patient_id]
        return False, f"Could not find a new visit note for Zhao with category='cat_003' (Annual Exam) and templateUsed='tmpl_001' (E* Annual Wellness Visit). Current notes: {patient_notes}"

    return True, "Successfully verified that a new visit note was created for Helen Zhao with Annual Exam category and E* Annual Wellness Visit template."
