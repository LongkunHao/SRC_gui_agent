import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify David Park (pat_7) has the 'VIP' tag."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("id") == "pat_7":
            patient = p
            break

    if patient is None:
        return False, "Patient pat_7 (David Park) not found in state"

    tags = patient.get("tags", [])
    if "VIP" not in tags:
        return False, f"Patient David Park (pat_7) tags are {tags}, expected 'VIP' to be present"

    return True, "David Park (pat_7) has the 'VIP' tag"
