import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rx_003 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_003"), None)
    if rx_003 is None:
        return False, "Prescription rx_003 (Metformin) not found."

    if rx_003.get("frequency") != "Once daily":
        return False, f"Expected rx_003 frequency 'Once daily', got '{rx_003.get('frequency')}'."

    return True, "Margaret's Metformin (rx_003) frequency changed to once daily."
