import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    prescriptions = state.get("prescriptions", [])
    rx_005 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_005":
            rx_005 = rx
            break

    if rx_005 is None:
        return False, "Prescription rx_005 (Pantoprazole) not found in state."

    status = rx_005.get("status", "")
    if status != "discontinued":
        return False, f"Expected rx_005 status to be 'discontinued', but got '{status}'."

    return True, "Pantoprazole (rx_005) has been successfully discontinued."
