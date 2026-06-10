import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Robert Washington (pat_3) does NOT have the 'Chronic Care' tag."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Robert" and p.get("lastName") == "Washington":
            patient = p
            break

    if patient is None:
        return False, "Patient Robert Washington not found in state"

    tags = patient.get("tags", [])
    if "Chronic Care" in tags:
        return False, f"Patient Robert Washington still has 'Chronic Care' tag. Current tags: {tags}"

    return True, "Robert Washington no longer has the 'Chronic Care' tag"
