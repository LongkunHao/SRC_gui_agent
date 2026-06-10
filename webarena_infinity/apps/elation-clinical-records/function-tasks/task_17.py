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

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        reason = v.get("reason", "")
        if (
            v.get("vaccineName") == "Influenza (IIV4) Standard"
            and v.get("recordType") == "Declined"
            and "not to vaccinate" in reason
            and v.get("status") == "declined"
        ):
            return True, "Found declined vaccination for David Kowalski with vaccineName='Influenza (IIV4) Standard', recordType='Declined', reason containing 'not to vaccinate', status='declined'."

    return False, "No vaccination found for David Kowalski with vaccineName='Influenza (IIV4) Standard', recordType='Declined', reason containing 'not to vaccinate', and status='declined'."
