import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()

    current_patient = state.get("currentPatientId", "")
    if current_patient != "pat_003":
        return False, f"Expected currentPatientId to be 'pat_003' (Aisha Rahman), but got '{current_patient}'."

    return True, "Aisha Rahman's chart is now open (currentPatientId is pat_003)."
