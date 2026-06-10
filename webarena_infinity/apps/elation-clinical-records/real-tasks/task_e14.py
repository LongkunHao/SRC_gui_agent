import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "O'Brien":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName=\"O'Brien\"."

    tags = patient.get("tags", [])
    if "*High-Risk" not in tags:
        return False, f"Patient William O'Brien does not have the '*High-Risk' tag. Current tags: {tags}"

    return True, "Successfully verified that '*High-Risk' priority tag has been added to William O'Brien."
