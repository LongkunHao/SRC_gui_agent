import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Emily Nakamura by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Nakamura":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Nakamura' not found."

    patient_id = patient.get("id")

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        if (
            v.get("vaccineName") == "Influenza (IIV4) Preservative Free"
            and v.get("manufacturer") == "Sanofi Pasteur"
            and v.get("method") == "Intramuscular"
            and v.get("site") == "Left Deltoid"
        ):
            return True, "Found vaccination for Emily Nakamura with vaccineName='Influenza (IIV4) Preservative Free', manufacturer='Sanofi Pasteur', method='Intramuscular', site='Left Deltoid'."

    return False, "No vaccination found for Emily Nakamura with vaccineName='Influenza (IIV4) Preservative Free', manufacturer='Sanofi Pasteur', method='Intramuscular', site='Left Deltoid'."
