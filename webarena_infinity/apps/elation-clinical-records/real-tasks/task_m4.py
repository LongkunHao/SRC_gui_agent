import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Henderson":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Henderson'."

    patient_id = patient.get("id")
    vitals = state.get("vitals", [])
    target_vital = None
    for v in vitals:
        if (v.get("patientId") == patient_id
                and v.get("bloodPressureSystolic") == 126
                and v.get("bloodPressureDiastolic") == 78
                and v.get("heartRate") == 72):
            target_vital = v
            break

    if target_vital is None:
        patient_vitals = [
            {"id": v.get("id"), "bp": f"{v.get('bloodPressureSystolic')}/{v.get('bloodPressureDiastolic')}", "hr": v.get("heartRate")}
            for v in vitals if v.get("patientId") == patient_id
        ]
        return False, f"Could not find vitals with BP 126/78 and HR 72 for patient Henderson (patientId={patient_id}). Current vitals: {patient_vitals}"

    return True, "Successfully verified that vitals (BP 126/78, HR 72) were added for Robert Henderson."
