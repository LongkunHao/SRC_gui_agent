# Task: Leave both non-admin workspaces (Side Project Labs and Open Source Collective).
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    workspaces = state.get("workspaces", [])

    if len(workspaces) != 1:
        names = [w.get("name", "unknown") for w in workspaces]
        return False, f"Expected 1 workspace, found {len(workspaces)}: {names}"
    if workspaces[0].get("name") != "Acme Corp":
        return False, f"Remaining workspace is '{workspaces[0].get('name')}', expected 'Acme Corp'"
    return True, "Non-admin workspaces removed, only 'Acme Corp' remains."
