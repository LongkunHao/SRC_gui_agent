import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected current patient pat_002 (David Kowalski), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_018"), None)

    if rx is None:
        return False, "Prescription rx_018 not found in state."

    if rx.get("status") != "discontinued":
        return False, f"rx_018 status should be 'discontinued', got '{rx.get('status')}'."

    reason = rx.get("discontinuedReason", "")
    if "side effect" not in reason.lower():
        return False, f"rx_018 discontinuedReason should contain 'side effect', got '{reason}'."

    return True, "Patient switched to David Kowalski and rx_018 (Escitalopram) is discontinued with correct reason."
