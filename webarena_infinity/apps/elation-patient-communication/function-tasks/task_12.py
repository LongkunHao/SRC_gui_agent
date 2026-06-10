import requests


def verify(server_url: str) -> tuple[bool, str]:
    """Verify Janet Okonkwo (pat_30) has the 'High Risk' tag."""
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    patients = state.get("patients", [])

    patient = None
    for p in patients:
        if p.get("id") == "pat_30" or (p.get("firstName") == "Janet" and p.get("lastName") == "Okonkwo"):
            patient = p
            break

    if patient is None:
        return False, "Patient Janet Okonkwo (pat_30) not found in state"

    tags = patient.get("tags", [])
    if "High Risk" not in tags:
        return False, f"Patient Janet Okonkwo (pat_30) tags are {tags}, expected 'High Risk' to be present"

    return True, "Janet Okonkwo (pat_30) has the 'High Risk' tag"
