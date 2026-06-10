import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    prescriptions = state.get("prescriptions", [])
    rx_012 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_012":
            rx_012 = rx
            break

    if rx_012 is None:
        return False, "Prescription rx_012 (Hydrochlorothiazide) not found in state."

    status = rx_012.get("status", "")
    if status != "active":
        return False, f"Expected rx_012 status to be 'active', but got '{status}'."

    return True, "Hydrochlorothiazide (rx_012) has been successfully resumed to active status."
