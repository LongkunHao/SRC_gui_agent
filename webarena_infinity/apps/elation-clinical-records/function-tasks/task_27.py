import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient James Fitzgerald by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Fitzgerald":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Fitzgerald' not found."

    patient_id = patient.get("id")

    # Check for a new visit note with reason='New Patient Visit' and status='draft'
    visit_notes = state.get("visitNotes", [])
    for vn in visit_notes:
        if vn.get("patientId") != patient_id:
            continue
        if (
            vn.get("reason") == "New Patient Visit"
            and vn.get("status") == "draft"
        ):
            return True, "Found visit note for James Fitzgerald with reason='New Patient Visit' and status='draft'."

    return False, "No visit note found for James Fitzgerald with reason='New Patient Visit' and status='draft'."
