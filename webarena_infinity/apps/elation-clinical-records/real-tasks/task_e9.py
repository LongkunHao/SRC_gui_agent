import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    patients = state.get("patients", [])
    patient = None
    for p in patients:
        if p.get("lastName") == "Nakamura":
            patient = p
            break

    if patient is None:
        return False, "Could not find patient with lastName='Nakamura'."

    tags = patient.get("tags", [])
    if "Prenatal" in tags:
        return False, f"Patient Emily Nakamura still has the 'Prenatal' tag. Current tags: {tags}"

    return True, "Successfully verified that 'Prenatal' tag has been removed from Emily Nakamura."
