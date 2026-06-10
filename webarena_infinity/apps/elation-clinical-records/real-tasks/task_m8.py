import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Kowalski":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Kowalski'."

    patient_id = patient.get("id")
    vaccinations = state.get("vaccinations", [])
    target_vax = None
    for vax in vaccinations:
        if (vax.get("patientId") == patient_id
                and "influenza" in vax.get("vaccineName", "").lower()
                and vax.get("recordType") == "Declined"):
            target_vax = vax
            break

    if target_vax is None:
        patient_vaxes = [(vax.get("vaccineName"), vax.get("recordType")) for vax in vaccinations if vax.get("patientId") == patient_id]
        return False, f"Could not find a declined influenza vaccination for patient Kowalski (patientId={patient_id}). Current vaccinations: {patient_vaxes}"

    return True, "Successfully verified that a declined influenza vaccine was recorded for David Kowalski."
