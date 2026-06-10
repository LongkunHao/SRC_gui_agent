import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_006":
        return False, f"Expected currentPatientId 'pat_006' (Robert Fitzgerald), got '{state.get('currentPatientId')}'."

    rx_028 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_028"), None)
    if rx_028 is None:
        return False, "Prescription rx_028 (Carvedilol) not found."

    dosage = rx_028.get("dosage", "")
    if "25" not in dosage:
        return False, f"Expected rx_028 dosage to contain '25', got '{dosage}'."

    return True, "Switched to Robert Fitzgerald and raised Carvedilol (rx_028) dose to 25mg."
