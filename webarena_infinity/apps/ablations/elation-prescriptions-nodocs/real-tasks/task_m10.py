import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rx_014 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_014"), None)
    if rx_014 is None:
        return False, "Prescription rx_014 (Apixaban/Eliquis) not found."

    if rx_014.get("refillsRemaining") != 5:
        return False, f"Expected rx_014 refillsRemaining 5, got {rx_014.get('refillsRemaining')}."

    if rx_014.get("refillsTotal") != 5:
        return False, f"Expected rx_014 refillsTotal 5, got {rx_014.get('refillsTotal')}."

    if rx_014.get("status") != "active":
        return False, f"Expected rx_014 status 'active', got '{rx_014.get('status')}'."

    return True, "Margaret's Eliquis (rx_014) renewed with 5 refills."
