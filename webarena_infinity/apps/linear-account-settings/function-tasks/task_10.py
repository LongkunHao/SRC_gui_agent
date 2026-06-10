import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for ws in state.get("workspaces", []):
        if ws.get("name") == "Side Project Labs":
            return False, "Workspace 'Side Project Labs' still exists."
    return True, "Successfully left 'Side Project Labs' workspace."
