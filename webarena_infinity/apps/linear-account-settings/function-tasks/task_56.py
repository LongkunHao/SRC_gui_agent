import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for key in state["apiKeys"]:
        if key.get("label") == "Data Export Script":
            return False, "API key 'Data Export Script' still exists."
    return True, "API key 'Data Export Script' successfully revoked."
