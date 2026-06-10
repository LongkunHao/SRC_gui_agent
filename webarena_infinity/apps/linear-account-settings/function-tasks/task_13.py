import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    val = state["preferences"]["defaultHomeView"]
    if val == "My Issues":
        return True, "Default home view successfully changed to 'My Issues'."
    return False, f"Expected defaultHomeView 'My Issues', got '{val}'."
