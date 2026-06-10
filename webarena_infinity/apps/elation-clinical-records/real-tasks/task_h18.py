import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find Wu (pat_012)
    patients = state.get("patients", [])
    wu = None
    for p in patients:
        if p.get("lastName") == "Wu":
            wu = p
            break
    if not wu:
        return False, "Patient with lastName 'Wu' not found."

    patient_id = wu.get("id", "pat_012")

    # Find vitals for Wu
    vitals = state.get("vitals", [])
    wu_vitals = [v for v in vitals if v.get("patientId") == patient_id]

    if not wu_vitals:
        return False, "No vitals found for Mei-Ling Wu."

    expected = {
        "bloodPressureSystolic": 108,
        "bloodPressureDiastolic": 68,
        "heartRate": 76,
        "temperature": 98.6,
        "weight": 115,
        "height": 63,
        "painLevel": 0,
    }

    for vital in wu_vitals:
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
            return True, "Wu's vitals recorded correctly: BP 108/68, HR 76, Temp 98.6, Weight 115, Height 63, Pain 0."

    # Show diagnostics from the closest match
    best_vital = wu_vitals[-1]
    mismatches = []
    for key, expected_val in expected.items():
        actual = best_vital.get(key)
        try:
            actual_num = float(actual) if actual is not None else None
        except (ValueError, TypeError):
            actual_num = None
        if actual_num is None or abs(actual_num - expected_val) > 0.01:
            mismatches.append(f"{key}: expected {expected_val}, got {actual}")
    return False, f"No vital entry for Wu matches all criteria. Closest mismatch(es): {'; '.join(mismatches)}"
