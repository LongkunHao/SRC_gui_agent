import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify James Rodriguez (pat_1) passport sharing level changed to 4."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "James" and p.get("lastName") == "Rodriguez":
            patient = p
            break

    if patient is None:
        return False, "Patient James Rodriguez not found in patients"

    if patient.get("passportSharingLevel") != 4:
        return False, f"James Rodriguez passportSharingLevel is {patient.get('passportSharingLevel')}, expected 4"

    return True, "James Rodriguez (pat_1) passport sharing level changed to 4 successfully"
