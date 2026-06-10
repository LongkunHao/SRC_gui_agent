import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rx_030 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_030"), None)
    if rx_030 is None:
        return False, "Prescription rx_030 (Semaglutide/Ozempic) not found."

    if rx_030.get("status") != "on-hold":
        return False, f"Expected rx_030 status 'on-hold', got '{rx_030.get('status')}'."

    return True, "Margaret's Ozempic (rx_030) put on hold — prior auth needs renewal."
