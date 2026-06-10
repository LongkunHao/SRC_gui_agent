import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for key in state["apiKeys"]:
        if key.get("label") == "Mobile App Testing":
            return False, "API key 'Mobile App Testing' still exists."
    return True, "API key 'Mobile App Testing' successfully revoked."
