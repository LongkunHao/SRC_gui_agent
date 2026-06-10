import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rx_001 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_001"), None)
    if rx_001 is None:
        return False, "Prescription rx_001 (Atorvastatin) not found."

    dosage = rx_001.get("dosage", "")
    if "40" not in dosage:
        return False, f"Expected rx_001 dosage to contain '40', got '{dosage}'."

    if rx_001.get("quantity") != 90:
        return False, f"Expected rx_001 quantity 90, got {rx_001.get('quantity')}."

    return True, "Margaret's Atorvastatin (rx_001) updated to 40mg with quantity 90."
