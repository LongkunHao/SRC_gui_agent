import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Zhao":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Zhao'."

    tags = patient.get("tags", [])
    if "Fall-Risk" not in tags:
        return False, f"Patient Helen Zhao does not have the 'Fall-Risk' tag. Current tags: {tags}"

    return True, "Successfully verified that 'Fall-Risk' tag has been added to Helen Zhao's chart."
