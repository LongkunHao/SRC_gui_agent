import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_003":
        return False, f"Expected current patient pat_003 (Aisha Rahman), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_021"), None)

    if rx is None:
        return False, "Prescription rx_021 not found in state."

    if rx.get("status") != "cancelled":
        return False, f"rx_021 status should be 'cancelled', got '{rx.get('status')}'."

    return True, "Patient switched to Aisha Rahman and rx_021 (Escitalopram) is cancelled."
