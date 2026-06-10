import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Megan Burke (pat_42) has the 'Insurance Pending' tag."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("id") == "pat_42":
            patient = p
            break

    if patient is None:
        return False, "Patient pat_42 (Megan Burke) not found in state"

    tags = patient.get("tags", [])
    if "Insurance Pending" not in tags:
        return False, f"Patient Megan Burke (pat_42) tags are {tags}, expected 'Insurance Pending' to be present"

    return True, "Megan Burke (pat_42) has the 'Insurance Pending' tag"
