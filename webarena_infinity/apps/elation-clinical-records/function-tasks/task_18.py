import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Sofia Rodriguez-Martinez by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Rodriguez-Martinez":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Rodriguez-Martinez' not found."

    patient_id = patient.get("id")

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        if (
            v.get("vaccineName") == "Tdap (Adacel)"
            and v.get("lotNumber") == "TDP-5590"
            and v.get("expirationDate") == "2027-06-30"
        ):
            return True, "Found vaccination for Sofia Rodriguez-Martinez with vaccineName='Tdap (Adacel)', lotNumber='TDP-5590', expirationDate='2027-06-30'."

    return False, "No vaccination found for Sofia Rodriguez-Martinez with vaccineName='Tdap (Adacel)', lotNumber='TDP-5590', expirationDate='2027-06-30'."
