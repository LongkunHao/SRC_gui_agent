import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for ws in state.get("workspaces", []):
        if ws.get("name") == "Open Source Collective":
            return False, "Workspace 'Open Source Collective' still exists."
    return True, "Successfully left 'Open Source Collective' workspace."
