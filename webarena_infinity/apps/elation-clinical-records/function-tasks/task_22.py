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

    # Check for a NEW vitals record with BP 120/74, HR 70, RR 16
    # Seed data has vit_007 with BP 118/72, so we look for the new one specifically
    vitals = state.get("vitals", [])
    for v in vitals:
        if v.get("patientId") != patient_id:
            continue
        if v.get("id") == "vit_007":
            continue  # Skip existing seed record
        if (
            v.get("bloodPressureSystolic") == 120
            and v.get("bloodPressureDiastolic") == 74
            and v.get("heartRate") == 70
            and v.get("respiratoryRate") == 16
        ):
            return True, "Found new vitals record for Emily Nakamura with BP 120/74, HR 70, RR 16."

    return False, "No new vitals record found for Emily Nakamura with bloodPressureSystolic=120, bloodPressureDiastolic=74, heartRate=70, respiratoryRate=16."
