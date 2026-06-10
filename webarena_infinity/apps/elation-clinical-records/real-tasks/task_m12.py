import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Rodriguez-Martinez":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Rodriguez-Martinez'."

    patient_id = patient.get("id")
    vaccinations = state.get("vaccinations", [])
    target_vax = None
    for vax in vaccinations:
        if (vax.get("patientId") == patient_id
                and "tdap" in vax.get("vaccineName", "").lower()):
            target_vax = vax
            break

    if target_vax is None:
        patient_vaxes = [vax.get("vaccineName") for vax in vaccinations if vax.get("patientId") == patient_id]
        return False, f"Could not find a Tdap vaccination for patient Rodriguez-Martinez (patientId={patient_id}). Current vaccinations: {patient_vaxes}"

    lot_number = target_vax.get("lotNumber", "")
    if lot_number != "TDP-5590":
        return False, f"Tdap vaccination lotNumber is '{lot_number}', expected 'TDP-5590'."

    return True, "Successfully verified that Tdap vaccine with lot number TDP-5590 was recorded for Sofia Rodriguez-Martinez."
