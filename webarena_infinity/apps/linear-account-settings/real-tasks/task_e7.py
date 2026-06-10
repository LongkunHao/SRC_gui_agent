# Task: Set the default home view to My Issues.
import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()
    view = state.get("preferences", {}).get("defaultHomeView")
    if view == "My Issues":
        return True, "Default home view is 'My Issues'."
    return False, f"Expected defaultHomeView 'My Issues', got '{view}'."
