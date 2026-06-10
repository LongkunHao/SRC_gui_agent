import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_002":
        return False, f"Expected currentPatientId 'pat_002' (David Kowalski), got '{state.get('currentPatientId')}'."

    rr_005 = next((rr for rr in state.get("refillRequests", []) if rr["id"] == "rr_005"), None)
    if rr_005 is None:
        return False, "Refill request rr_005 not found."

    if rr_005.get("status") != "approved":
        return False, f"Expected rr_005 status 'approved', got '{rr_005.get('status')}'."

    rx_016 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_016"), None)
    if rx_016 is None:
        return False, "Prescription rx_016 (Metoprolol) not found."

    if rx_016.get("refillsRemaining") != 2:
        return False, f"Expected rx_016 refillsRemaining 2 (decremented from 3), got {rx_016.get('refillsRemaining')}."

    return True, "Switched to David Kowalski, approved Metoprolol refill (rr_005), and refillsRemaining decremented to 2."
