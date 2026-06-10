import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_006":
        return False, f"Expected current patient pat_006 (Robert Fitzgerald), got '{state.get('currentPatientId')}'."

    prescriptions = state.get("prescriptions", [])
    rx = next((p for p in prescriptions if p.get("id") == "rx_028"), None)

    if rx is None:
        return False, "Prescription rx_028 not found in state."

    if rx.get("status") != "active":
        return False, f"rx_028 status should be 'active', got '{rx.get('status')}'."

    if rx.get("refillsRemaining") != 5:
        return False, f"rx_028 refillsRemaining should be 5, got {rx.get('refillsRemaining')}."

    if rx.get("refillsTotal") != 5:
        return False, f"rx_028 refillsTotal should be 5, got {rx.get('refillsTotal')}."

    history = rx.get("history", [])
    renewed = any(h.get("action") == "renewed" for h in history)
    if not renewed:
        return False, "rx_028 history does not contain a 'renewed' entry."

    return True, "Patient switched to Robert Fitzgerald and rx_028 (Carvedilol) renewed with 5 refills."
