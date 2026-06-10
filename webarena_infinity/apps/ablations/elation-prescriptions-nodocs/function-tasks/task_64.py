import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    if state.get("currentPatientId") != "pat_005":
        return False, f"Expected current patient pat_005 (Jessica Morales), got '{state.get('currentPatientId')}'."

    return True, "Current patient switched to Jessica Morales (pat_005)."
