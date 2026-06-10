import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Brian Murphy (pat_15) passport invitation was sent."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Brian" and p.get("lastName") == "Murphy":
            patient = p
            break

    if patient is None:
        return False, "Patient Brian Murphy not found in patients"

    if patient.get("passportStatus") != "invited":
        return False, f"Brian Murphy passportStatus is '{patient.get('passportStatus')}', expected 'invited'"

    if patient.get("invitedAt") is None:
        return False, "Brian Murphy invitedAt is None, expected a timestamp"

    return True, "Brian Murphy (pat_15) passport invitation sent successfully"
