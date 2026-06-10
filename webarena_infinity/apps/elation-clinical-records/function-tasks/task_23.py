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

    # Check for a NEW vitals record with temperature 37.2 and unit C
    # Seed data has vit_008 and vit_009 for Johnson - look for new one
    vitals = state.get("vitals", [])
    for v in vitals:
        if v.get("patientId") != patient_id:
            continue
        if v.get("id") in ("vit_008", "vit_009"):
            continue  # Skip existing seed records
        if (
            v.get("temperature") == 37.2
            and v.get("temperatureUnit") == "C"
        ):
            return True, "Found new vitals record for Marcus Johnson with temperature=37.2 and temperatureUnit='C'."

    return False, "No new vitals record found for Marcus Johnson with temperature=37.2 and temperatureUnit='C'."
