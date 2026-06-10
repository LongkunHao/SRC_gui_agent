# Task: Set username to URL key of most recently joined workspace, then leave it.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    failures = []

    # Most recently joined workspace was Open Source Collective (urlKey='osc')
    username = state.get("currentUser", {}).get("username", "")
    if username != "osc":
        failures.append(f"Expected username 'osc', got '{username}'")

    workspaces = state.get("workspaces", [])
    ws_names = [w.get("name") for w in workspaces]
    if "Open Source Collective" in ws_names:
        failures.append("Open Source Collective workspace should have been left")

    if failures:
        return False, "; ".join(failures)
    return True, "Username set to 'osc' and Open Source Collective workspace left."
