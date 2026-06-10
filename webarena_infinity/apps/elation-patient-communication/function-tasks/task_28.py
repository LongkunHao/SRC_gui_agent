import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Helen Matsumoto (pat_10) passport sharing level changed to 1."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Helen" and p.get("lastName") == "Matsumoto":
            patient = p
            break

    if patient is None:
        return False, "Patient Helen Matsumoto not found in patients"

    if patient.get("passportSharingLevel") != 1:
        return False, f"Helen Matsumoto passportSharingLevel is {patient.get('passportSharingLevel')}, expected 1"

    return True, "Helen Matsumoto (pat_10) passport sharing level changed to 1 successfully"
