import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    collaborators = state.get("collaborators", [])
    collab = next(
        (c for c in collaborators if c.get("name") == "Tom Nguyen" or c.get("id") == "user_006"),
        None
    )
    if not collab:
        return False, "Collaborator 'Tom Nguyen' (user_006) not found."

    role = collab.get("role")
    if role != "Editor":
        return False, f"Expected Tom Nguyen's role to be 'Editor', but found '{role}'."

    return True, "Collaborator Tom Nguyen (user_006) has role 'Editor' as expected."
