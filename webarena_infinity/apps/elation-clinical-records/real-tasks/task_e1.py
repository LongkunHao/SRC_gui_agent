import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Johnson":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Johnson'."

    tags = patient.get("tags", [])
    if "Smoker" in tags:
        return False, f"Patient Marcus Johnson still has the 'Smoker' tag. Current tags: {tags}"

    return True, "Successfully verified that 'Smoker' tag has been removed from Marcus Johnson's chart."
