import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Priya Sharma by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Sharma":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Sharma' not found."

    patient_id = patient.get("id")

    # Check for a visit note with format='simple'
    visit_notes = state.get("visitNotes", [])
    for vn in visit_notes:
        if vn.get("patientId") != patient_id:
            continue
        if vn.get("format") == "simple":
            return True, "Found visit note for Priya Sharma with format='simple'."

    return False, "No visit note found for Priya Sharma with format='simple'."
