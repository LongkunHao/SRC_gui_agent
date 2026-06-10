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

    # Check for a NEW vitals record with oxygenSaturation=98, BP 110/68
    # Seed data has vit_012 with different values
    vitals = state.get("vitals", [])
    for v in vitals:
        if v.get("patientId") != patient_id:
            continue
        if v.get("id") == "vit_012":
            continue  # Skip existing seed record
        if (
            v.get("oxygenSaturation") == 98
            and v.get("bloodPressureSystolic") == 110
            and v.get("bloodPressureDiastolic") == 68
        ):
            return True, "Found new vitals record for Sofia Rodriguez-Martinez with oxygenSaturation=98, BP 110/68."

    return False, "No new vitals record found for Sofia Rodriguez-Martinez with oxygenSaturation=98, bloodPressureSystolic=110, bloodPressureDiastolic=68."
