import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient James Fitzgerald by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Fitzgerald":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Fitzgerald' not found."

    tags = patient.get("tags", [])
    if "New-Patient" in tags:
        return True, "Tag 'New-Patient' found in James Fitzgerald's tags."
    else:
        return False, f"Tag 'New-Patient' not found in James Fitzgerald's tags. Current tags: {tags}"
