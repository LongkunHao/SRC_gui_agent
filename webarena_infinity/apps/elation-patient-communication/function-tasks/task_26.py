import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Stephanie Rivera (pat_28) passport is disabled."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Stephanie" and p.get("lastName") == "Rivera":
            patient = p
            break

    if patient is None:
        return False, "Patient Stephanie Rivera not found in patients"

    if patient.get("passportAccountDisabled") is not True:
        return False, f"Stephanie Rivera passportAccountDisabled is {patient.get('passportAccountDisabled')}, expected True"

    if patient.get("passportStatus") != "not_invited":
        return False, f"Stephanie Rivera passportStatus is '{patient.get('passportStatus')}', expected 'not_invited'"

    return True, "Stephanie Rivera (pat_28) passport disabled successfully"
