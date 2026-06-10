import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Sharma":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Sharma'."

    tags = patient.get("tags", [])
    if "Pediatric-Parent" in tags:
        return False, f"Patient Priya Sharma still has the 'Pediatric-Parent' tag. Current tags: {tags}"

    return True, "Successfully verified that 'Pediatric-Parent' tag has been removed from Priya Sharma."
