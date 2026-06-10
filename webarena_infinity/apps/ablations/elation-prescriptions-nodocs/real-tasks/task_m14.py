import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    rx_007 = next((rx for rx in state["prescriptions"] if rx["id"] == "rx_007"), None)
    if rx_007 is None:
        return False, "Prescription rx_007 (Gabapentin) not found."

    expected_sig = "Take 1 capsule by mouth twice daily with food"
    if rx_007.get("sig") != expected_sig:
        return False, f"Expected rx_007 sig '{expected_sig}', got '{rx_007.get('sig')}'."

    return True, "Margaret's Gabapentin (rx_007) directions updated to 'Take 1 capsule by mouth twice daily with food'."
