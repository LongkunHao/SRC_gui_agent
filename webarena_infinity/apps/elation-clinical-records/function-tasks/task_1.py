import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Find patient Robert Henderson by lastName
    patient = None
    for p in state.get("patients", []):
        if p.get("lastName") == "Henderson":
            patient = p
            break

    if not patient:
        return False, "Patient with lastName 'Henderson' not found."

    tags = patient.get("tags", [])
    if "Flu-Season" in tags:
        return True, "Tag 'Flu-Season' found in Robert Henderson's tags."
    else:
        return False, f"Tag 'Flu-Season' not found in Robert Henderson's tags. Current tags: {tags}"
