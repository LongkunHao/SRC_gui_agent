import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Emily Nakamura by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Nakamura":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Nakamura' not found."

    tags = patient.get("tags", [])
    if "*High-Risk" in tags:
        return True, "Tag '*High-Risk' found in Emily Nakamura's tags."
    else:
        return False, f"Tag '*High-Risk' not found in Emily Nakamura's tags. Current tags: {tags}"
