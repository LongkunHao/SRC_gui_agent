import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    prescriptions = state.get("prescriptions", [])
    rx_007 = None
    for rx in prescriptions:
        if rx.get("id") == "rx_007":
            rx_007 = rx
            break

    if rx_007 is None:
        return False, "Prescription rx_007 (Gabapentin) not found in state."

    status = rx_007.get("status", "")
    if status != "on-hold":
        return False, f"Expected rx_007 status to be 'on-hold', but got '{status}'."

    return True, "Gabapentin (rx_007) has been successfully put on hold."
