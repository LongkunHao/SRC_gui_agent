import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    prescriptions = state.get("prescriptions", [])
    rx_002 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_002":
            rx_002 = rx
            break

    if rx_002 is None:
        return False, "Prescription rx_002 (Amlodipine) not found in state."

    quantity = rx_002.get("quantity")
    if quantity != 90:
        return False, f"Expected rx_002 quantity to be 90, but got {quantity}."

    return True, "Amlodipine (rx_002) quantity increased to 90."
