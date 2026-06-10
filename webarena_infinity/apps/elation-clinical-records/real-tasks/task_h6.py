import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find O'Brien (pat_005)
    patients = state.get("patients", [])
    obrien = None
    for p in patients:
        if p.get("lastName") == "O'Brien" or p.get("lastName") == "O\u2019Brien":
            obrien = p
            break
    if not obrien:
        return False, "Patient with lastName \"O'Brien\" not found."

    patient_id = obrien.get("id", "pat_005")

    # Find vitals for O'Brien
    vitals = state.get("vitals", [])
    obrien_vitals = [v for v in vitals if v.get("patientId") == patient_id]

    if not obrien_vitals:
        return False, "No vitals found for O'Brien."

    expected = {
        "bloodPressureSystolic": 138,
        "bloodPressureDiastolic": 86,
        "heartRate": 68,
        "respiratoryRate": 18,
        "oxygenSaturation": 93,
        "temperature": 97.6,
        "weight": 190,
        "painLevel": 4,
    }

    for vital in obrien_vitals:
        errors = []
        for key, expected_val in expected.items():
            actual = vital.get(key)
            if actual is None:
                errors.append(f"{key}: missing")
                continue
            try:
                actual_num = float(actual)
            except (ValueError, TypeError):
                errors.append(f"{key}: expected {expected_val}, got '{actual}'")
                continue
            if abs(actual_num - expected_val) > 0.01:
                errors.append(f"{key}: expected {expected_val}, got {actual_num}")

        if not errors:
            return True, "O'Brien's vitals recorded correctly: BP 138/86, HR 68, RR 18, SpO2 93, Temp 97.6, Weight 190, Pain 4."

    # Show details from closest match
    best_vital = obrien_vitals[-1]  # most recent
    mismatches = []
    for key, expected_val in expected.items():
        actual = best_vital.get(key)
        try:
            actual_num = float(actual) if actual is not None else None
        except (ValueError, TypeError):
            actual_num = None
        if actual_num is None or abs(actual_num - expected_val) > 0.01:
            mismatches.append(f"{key}: expected {expected_val}, got {actual}")
    return False, f"No vital entry for O'Brien matches all criteria. Closest mismatch(es): {'; '.join(mismatches)}"
