import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    prescriptions = state.get("prescriptions", [])
    rx_013 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_013":
            rx_013 = rx
            break

    if rx_013 is None:
        return False, "Prescription rx_013 (Sertraline) not found in state."

    status = rx_013.get("status", "")
    if status != "discontinued":
        return False, f"Expected rx_013 status to be 'discontinued', but got '{status}'."

    return True, "Sertraline (rx_013) has been successfully discontinued."
