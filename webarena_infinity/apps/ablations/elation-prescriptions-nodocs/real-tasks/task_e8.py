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

    refills_remaining = rx_013.get("refillsRemaining")
    if refills_remaining != 5:
        return False, f"Expected rx_013 refillsRemaining to be 5, but got {refills_remaining}."

    refills_total = rx_013.get("refillsTotal")
    if refills_total != 5:
        return False, f"Expected rx_013 refillsTotal to be 5, but got {refills_total}."

    status = rx_013.get("status", "")
    if status != "active":
        return False, f"Expected rx_013 status to be 'active', but got '{status}'."

    return True, "Sertraline (rx_013) renewed with 5 refills and active status."
