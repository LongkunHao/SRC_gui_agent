import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Thomas Bergstrom by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Bergstrom":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Bergstrom' not found."

    patient_id = patient.get("id")

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        if (
            v.get("vaccineName") == "COVID-19 Moderna"
            and v.get("recall") == "3 weeks"
        ):
            return True, "Found vaccination for Thomas Bergstrom with vaccineName='COVID-19 Moderna' and recall='3 weeks'."

    return False, "No vaccination found for Thomas Bergstrom with vaccineName='COVID-19 Moderna' and recall='3 weeks'."
