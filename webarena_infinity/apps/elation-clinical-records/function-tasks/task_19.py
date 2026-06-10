import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Marcus Johnson by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Johnson":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Johnson' not found."

    patient_id = patient.get("id")

    # Check for vaccination with matching criteria
    vaccinations = state.get("vaccinations", [])
    for v in vaccinations:
        if v.get("patientId") != patient_id:
            continue
        if (
            v.get("vaccineName") == "Ketorolac (Toradol)"
            and v.get("isInjectable") is True
            and v.get("notSendToRegistry") is True
            and v.get("method") == "Intramuscular"
            and v.get("site") == "Left Gluteal"
        ):
            return True, "Found vaccination for Marcus Johnson with vaccineName='Ketorolac (Toradol)', isInjectable=True, notSendToRegistry=True, method='Intramuscular', site='Left Gluteal'."

    return False, "No vaccination found for Marcus Johnson with vaccineName='Ketorolac (Toradol)', isInjectable=True, notSendToRegistry=True, method='Intramuscular', site='Left Gluteal'."
