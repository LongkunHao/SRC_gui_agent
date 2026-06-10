import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected current patient pat_002 (David Kowalski), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_017"), None)

    if rx is None:
        return False, "Prescription rx_017 not found in state."

    if rx.get("status") != "active":
        return False, f"rx_017 status should be 'active', got '{rx.get('status')}'."

    if rx.get("refillsRemaining") != 3:
        return False, f"rx_017 refillsRemaining should be 3, got {rx.get('refillsRemaining')}."

    if rx.get("refillsTotal") != 3:
        return False, f"rx_017 refillsTotal should be 3, got {rx.get('refillsTotal')}."

    history = rx.get("history", [])
    renewed = any(h.get("action") == "renewed" for h in history)
    if not renewed:
        return False, "rx_017 history does not contain a 'renewed' entry."

    return True, "Patient switched to David Kowalski and rx_017 (Atorvastatin) renewed with 3 refills."
