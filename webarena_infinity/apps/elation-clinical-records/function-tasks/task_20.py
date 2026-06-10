import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Aaliyah Washington by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Washington":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Washington' not found."

    patient_id = patient.get("id")

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        if (
            v.get("vaccineName") == "DTaP (Daptacel)"
            and v.get("program") == "VFC Eligible"
            and v.get("fundedBy") == "VFC"
        ):
            return True, "Found vaccination for Aaliyah Washington with vaccineName='DTaP (Daptacel)', program='VFC Eligible', fundedBy='VFC'."

    return False, "No vaccination found for Aaliyah Washington with vaccineName='DTaP (Daptacel)', program='VFC Eligible', fundedBy='VFC'."
