import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for key in state["apiKeys"]:
        if key.get("label") == "GitHub Actions":
            return True, "API key 'GitHub Actions' successfully created."
    return False, "No API key with label 'GitHub Actions' found."
