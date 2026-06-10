import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Born-before-1950 patient: renew all active rxs with 6."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    errors = []

    # William Thornton (pat_004, born 1944) — all 3 active rxs renewed with 6
    if state.get("currentPatientId") != "pat_004":
        errors.append(f"Expected currentPatientId 'pat_004' (William Thornton), got '{state.get('currentPatientId')}'.")

    for rx_id, name in [("rx_022", "Valsartan"), ("rx_023", "Insulin Glargine"), ("rx_024", "Furosemide")]:
        rx = next((r for r in state["prescriptions"] if r["id"] == rx_id), None)
        if not rx:
            errors.append(f"Prescription {rx_id} ({name}) not found.")
        elif rx.get("refillsRemaining", 0) < 6:
            errors.append(f"Expected {rx_id} ({name}) refillsRemaining >= 6, got {rx.get('refillsRemaining')}.")

    if errors:
        return False, " ".join(errors)
    return True, "Pre-1950 patient found, all active prescriptions renewed for travel."
