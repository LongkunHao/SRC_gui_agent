import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient David Kowalski by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Kowalski":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Kowalski' not found."

    patient_id = patient.get("id")

    # Check for a vitals record with painLevel==6
    # No existing seed vitals for Kowalski, so any match is valid
    vitals = state.get("vitals", [])
    for v in vitals:
        if v.get("patientId") != patient_id:
            continue
        if v.get("painLevel") == 6:
            return True, "Found vitals record for David Kowalski with painLevel=6."

    return False, "No vitals record found for David Kowalski with painLevel=6."
