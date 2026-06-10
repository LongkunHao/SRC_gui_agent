import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Megan Burke (pat_42) passport invitation was sent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Megan" and p.get("lastName") == "Burke":
            patient = p
            break

    if patient is None:
        return False, "Patient Megan Burke not found in patients"

    if patient.get("passportStatus") != "invited":
        return False, f"Megan Burke passportStatus is '{patient.get('passportStatus')}', expected 'invited'"

    if patient.get("invitedAt") is None:
        return False, "Megan Burke invitedAt is None, expected a timestamp"

    return True, "Megan Burke (pat_42) passport invitation sent successfully"
