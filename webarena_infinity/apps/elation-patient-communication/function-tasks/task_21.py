import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Anthony Petrov (pat_9) passport invitation was sent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Anthony" and p.get("lastName") == "Petrov":
            patient = p
            break

    if patient is None:
        return False, "Patient Anthony Petrov not found in patients"

    if patient.get("passportStatus") != "invited":
        return False, f"Anthony Petrov passportStatus is '{patient.get('passportStatus')}', expected 'invited'"

    if patient.get("invitedAt") is None:
        return False, "Anthony Petrov invitedAt is None, expected a timestamp"

    return True, "Anthony Petrov (pat_9) passport invitation sent successfully"
