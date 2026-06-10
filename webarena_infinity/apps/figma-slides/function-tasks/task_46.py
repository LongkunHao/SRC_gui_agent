import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    collaborators = state.get("collaborators", [])
    for collab in collaborators:
        if collab.get("id") == "user_008" or collab.get("name") == "David Park":
            role = collab.get("role")
            if role == "Viewer":
                return True, "David Park (user_008) role is correctly set to 'Viewer'."
            else:
                return False, f"David Park (user_008) role is '{role}', expected 'Viewer'."

    return False, "Collaborator David Park (user_008) not found in state."
