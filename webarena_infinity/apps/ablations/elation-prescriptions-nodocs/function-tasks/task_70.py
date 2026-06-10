import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected current patient pat_002 (David Kowalski), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_016"), None)

    if rx is None:
        return False, "Prescription rx_016 not found in state."

    if rx.get("dosage") != "100mg":
        return False, f"rx_016 dosage should be '100mg', got '{rx.get('dosage')}'."

    history = rx.get("history", [])
    modified = any(h.get("action") == "modified" for h in history)
    if not modified:
        return False, "rx_016 history does not contain a 'modified' entry."

    return True, "Patient switched to David Kowalski and rx_016 (Metoprolol ER) dosage changed to 100mg."
