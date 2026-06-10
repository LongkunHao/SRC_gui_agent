import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_004":
        return False, f"Expected current patient pat_004 (William Thornton), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_023"), None)

    if rx is None:
        return False, "Prescription rx_023 not found in state."

    if rx.get("dosage") != "30 units":
        return False, f"rx_023 dosage should be '30 units', got '{rx.get('dosage')}'."

    history = rx.get("history", [])
    modified = any(h.get("action") == "modified" for h in history[-3:])
    if not modified:
        return False, "rx_023 recent history does not contain a 'modified' entry."

    return True, "Patient switched to William Thornton and rx_023 (Insulin Glargine) dosage changed to 30 units."
