import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Nakamura":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Nakamura'."

    patient_id = patient.get("id")
    vaccinations = state.get("vaccinations", [])
    target_vax = None
    for vax in vaccinations:
        if vax.get("patientId") == patient_id and "influenza" in vax.get("vaccineName", "").lower():
            target_vax = vax
            break

    if target_vax is None:
        patient_vaxes = [vax.get("vaccineName") for vax in vaccinations if vax.get("patientId") == patient_id]
        return False, f"Could not find an influenza vaccination for patient Nakamura (patientId={patient_id}). Current vaccinations: {patient_vaxes}"

    method = target_vax.get("method", "")
    if method != "Intramuscular":
        return False, f"Influenza vaccination method is '{method}', expected 'Intramuscular'."

    site = target_vax.get("site", "")
    if site != "Left Deltoid":
        return False, f"Influenza vaccination site is '{site}', expected 'Left Deltoid'."

    return True, "Successfully verified that influenza vaccine was recorded for Emily Nakamura, IM in left deltoid."
