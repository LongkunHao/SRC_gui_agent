import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for passkey in state["passkeys"]:
        if passkey.get("name") == "Windows Hello":
            return True, "Passkey 'Windows Hello' successfully added."
    return False, "No passkey with name 'Windows Hello' found."
