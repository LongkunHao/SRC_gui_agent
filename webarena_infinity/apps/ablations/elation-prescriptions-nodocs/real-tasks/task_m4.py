import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_005":
        return False, f"Expected currentPatientId 'pat_005' (Jessica Morales), got '{state.get('currentPatientId')}'."

    rx_025 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_025"), None)
    if rx_025 is None:
        return False, "Prescription rx_025 (Cephalexin) not found."

    if rx_025.get("status") != "on-hold":
        return False, f"Expected rx_025 status 'on-hold', got '{rx_025.get('status')}'."

    return True, "Switched to Jessica Morales and put Cephalexin (rx_025) on hold for GI side effects."
