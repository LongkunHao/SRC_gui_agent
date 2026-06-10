import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected current patient pat_002 (David Kowalski), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_019"), None)

    if rx is None:
        return False, "Prescription rx_019 not found in state."

    if rx.get("status") != "cancelled":
        return False, f"rx_019 status should be 'cancelled', got '{rx.get('status')}'."

    return True, "Patient switched to David Kowalski and rx_019 (Metformin ER) is cancelled."
