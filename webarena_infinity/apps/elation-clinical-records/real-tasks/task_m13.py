import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Johnson":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Johnson'."

    patient_id = patient.get("id")
    vitals = state.get("vitals", [])
    target_vital = None
    for v in vitals:
        if v.get("patientId") == patient_id:
            temp = v.get("temperature")
            temp_unit = v.get("temperatureUnit", "")
            if temp is not None and abs(float(temp) - 37.2) < 0.01 and temp_unit in ("C", "Celsius"):
                target_vital = v
                break

    if target_vital is None:
        patient_vitals = [
            {"id": v.get("id"), "temp": v.get("temperature"), "unit": v.get("temperatureUnit")}
            for v in vitals if v.get("patientId") == patient_id
        ]
        return False, f"Could not find vitals with temperature 37.2 Celsius for patient Johnson (patientId={patient_id}). Current vitals: {patient_vitals}"

    return True, "Successfully verified that vitals with temperature 37.2 Celsius were added for Marcus Johnson."
