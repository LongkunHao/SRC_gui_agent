import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    prescriptions = state.get("prescriptions", [])
    rx_008 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_008":
            rx_008 = rx
            break

    if rx_008 is None:
        return False, "Prescription rx_008 (Fluticasone/Flonase) not found in state."

    status = rx_008.get("status", "")
    if status != "cancelled":
        return False, f"Expected rx_008 status to be 'cancelled', but got '{status}'."

    return True, "Fluticasone/Flonase (rx_008) has been successfully cancelled."
