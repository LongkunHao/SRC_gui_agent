import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    val = state["preferences"]["defaultHomeView"]
    if val == "Favorited Projects":
        return True, "Default home view successfully changed to 'Favorited Projects'."
    return False, f"Expected defaultHomeView 'Favorited Projects', got '{val}'."
