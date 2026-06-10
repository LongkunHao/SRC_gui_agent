import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Helen Zhao by lastName
    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Zhao":
            patient = p
            break
    if not patient:
        return False, "Patient with lastName 'Zhao' not found."

    patient_id = patient.get("id")

    # Check for a NEW vitals record with weight=58, weightUnit='kg', height=157, heightUnit='cm'
    # Seed data has vit_013 with different values
    vitals = state.get("vitals", [])
    for v in vitals:
        if v.get("patientId") != patient_id:
            continue
        if v.get("id") == "vit_013":
            continue  # Skip existing seed record
        if (
            v.get("weight") == 58
            and v.get("weightUnit") == "kg"
            and v.get("height") == 157
            and v.get("heightUnit") == "cm"
        ):
            return True, "Found new vitals record for Helen Zhao with weight=58 kg, height=157 cm."

    return False, "No new vitals record found for Helen Zhao with weight=58, weightUnit='kg', height=157, heightUnit='cm'."
