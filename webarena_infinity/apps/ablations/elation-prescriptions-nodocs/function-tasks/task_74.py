import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_005":
        return False, f"Expected current patient pat_005 (Jessica Morales), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_026"), None)

    if rx is None:
        return False, "Prescription rx_026 not found in state."

    if rx.get("status") != "discontinued":
        return False, f"rx_026 status should be 'discontinued', got '{rx.get('status')}'."

    reason = rx.get("discontinuedReason", "")
    if "no longer needed" not in reason.lower() and "mood stable" not in reason.lower():
        return False, f"rx_026 discontinuedReason should mention 'no longer needed' or 'mood stable', got '{reason}'."

    return True, "Patient switched to Jessica Morales and rx_026 (Fluoxetine) is discontinued."
