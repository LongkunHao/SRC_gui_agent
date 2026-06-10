import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Emily Thompson (pat_2) does NOT have the 'New Patient' tag."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("firstName") == "Emily" and p.get("lastName") == "Thompson":
            patient = p
            break

    if patient is None:
        return False, "Patient Emily Thompson not found in state"

    tags = patient.get("tags", [])
    if "New Patient" in tags:
        return False, f"Patient Emily Thompson still has 'New Patient' tag. Current tags: {tags}"

    return True, "Emily Thompson no longer has the 'New Patient' tag"
