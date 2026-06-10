import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    collaborators = state.get("collaborators", [])
    if not collaborators:
        errors.append("No collaborators found in state")
        return False, "; ".join(errors)

    # Check that no collaborator has online==False
    offline_users = []
    for c in collaborators:
        if c.get("online") is False:
            offline_users.append(c.get("name", c.get("id", "unknown")))

    if offline_users:
        errors.append(f"Found offline collaborators that should have been removed: {', '.join(offline_users)}")

    if errors:
        return False, "; ".join(errors)
    return True, f"All offline collaborators removed successfully. {len(collaborators)} online collaborators remain."
