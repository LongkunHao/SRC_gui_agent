import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    collaborators = state.get("collaborators", [])
    collab = next(
        (c for c in collaborators if c.get("name") == "James O'Brien" or c.get("id") == "user_004"),
        None
    )
    if collab is not None:
        return False, "Collaborator 'James O'Brien' (user_004) still exists but should have been removed."

    if len(collaborators) != 6:
        return False, f"Expected 6 collaborators after removing James O'Brien, but found {len(collaborators)}."

    return True, "Collaborator James O'Brien (user_004) has been removed and total collaborators is 6 as expected."
