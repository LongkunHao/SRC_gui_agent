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

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        if (
            v.get("vaccineName") == "Hepatitis B (Engerix-B)"
            and v.get("recordType") == "Historical"
        ):
            return True, "Found vaccination for James Fitzgerald with vaccineName='Hepatitis B (Engerix-B)' and recordType='Historical'."

    return False, "No vaccination found for James Fitzgerald with vaccineName='Hepatitis B (Engerix-B)' and recordType='Historical'."
