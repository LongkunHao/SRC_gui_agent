import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    collaborators = state.get("collaborators", [])

    # Check Aiko Tanaka's role is Viewer
    aiko = None
    for c in collaborators:
        if c.get("name") == "Aiko Tanaka":
            aiko = c
            break

    if aiko is None:
        return False, "Could not find collaborator named 'Aiko Tanaka'"

    if aiko.get("role") != "Viewer":
        return False, f"Aiko Tanaka's role is '{aiko.get('role')}', expected 'Viewer'"

    # Check Elena Kowalski is removed
    for c in collaborators:
        if c.get("name") == "Elena Kowalski":
            return False, "Elena Kowalski is still present in collaborators but should be removed"

    return True, "Aiko Tanaka's role changed to Viewer and Elena Kowalski removed"
