import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_006":
        return False, f"Expected current patient pat_006 (Robert Fitzgerald), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_029"), None)

    if rx is None:
        return False, "Prescription rx_029 not found in state."

    if rx.get("status") != "on-hold":
        return False, f"rx_029 status should be 'on-hold', got '{rx.get('status')}'."

    return True, "Patient switched to Robert Fitzgerald and rx_029 (Spironolactone) is on hold."
