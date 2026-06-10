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
    vitals = state.get("vitals", [])
    target_vital = None
    for v in vitals:
        if (v.get("patientId") == patient_id
                and v.get("bloodPressureSystolic") == 110
                and v.get("bloodPressureDiastolic") == 68
                and v.get("oxygenSaturation") == 98):
            target_vital = v
            break

    if target_vital is None:
        patient_vitals = [
            {"id": v.get("id"), "bp": f"{v.get('bloodPressureSystolic')}/{v.get('bloodPressureDiastolic')}", "spo2": v.get("oxygenSaturation")}
            for v in vitals if v.get("patientId") == patient_id
        ]
        return False, f"Could not find vitals with BP 110/68 and SpO2 98 for patient Rodriguez-Martinez (patientId={patient_id}). Current vitals: {patient_vitals}"

    return True, "Successfully verified that vitals (BP 110/68, SpO2 98) were added for Sofia Rodriguez-Martinez."
