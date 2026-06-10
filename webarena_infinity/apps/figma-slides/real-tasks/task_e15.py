import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    collaborators = state.get("collaborators", [])
    target = None
    for collab in collaborators:
        if collab.get("name") == "James O'Brien":
            target = collab
            break

    if target is None:
        return False, "Could not find collaborator 'James O'Brien'"

    role = target.get("role")
    if role != "Editor":
        return False, f"James O'Brien's role is '{role}', expected 'Editor'"

    return True, "James O'Brien's role changed to Editor"
