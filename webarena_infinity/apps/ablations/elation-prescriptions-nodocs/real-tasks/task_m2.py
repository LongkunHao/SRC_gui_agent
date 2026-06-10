import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_004":
        return False, f"Expected currentPatientId 'pat_004' (William Thornton), got '{state.get('currentPatientId')}'."

    rx_023 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_023"), None)
    if rx_023 is None:
        return False, "Prescription rx_023 (Insulin Glargine) not found."

    if rx_023.get("refillsRemaining") != 3:
        return False, f"Expected rx_023 refillsRemaining 3, got {rx_023.get('refillsRemaining')}."

    if rx_023.get("refillsTotal") != 3:
        return False, f"Expected rx_023 refillsTotal 3, got {rx_023.get('refillsTotal')}."

    if rx_023.get("status") != "active":
        return False, f"Expected rx_023 status 'active', got '{rx_023.get('status')}'."

    return True, "Switched to William Thornton and renewed Insulin Glargine (rx_023) with 3 refills."
