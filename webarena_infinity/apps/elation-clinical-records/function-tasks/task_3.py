import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Marcus Johnson by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Johnson":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Johnson' not found."

    tags = patient.get("tags", [])
    if "Smoker" not in tags:
        return True, "Tag 'Smoker' correctly does not exist in Marcus Johnson's tags."
    else:
        return False, f"Tag 'Smoker' still exists in Marcus Johnson's tags. Current tags: {tags}"
