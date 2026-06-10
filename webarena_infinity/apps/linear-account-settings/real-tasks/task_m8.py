# Task: Leave the Side Project Labs workspace.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    workspaces = state.get("workspaces", [])
    for ws in workspaces:
        if ws.get("name") == "Side Project Labs":
            return False, "Workspace 'Side Project Labs' still exists."
    return True, "Successfully left the Side Project Labs workspace."
