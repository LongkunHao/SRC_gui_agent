import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    for passkey in state["passkeys"]:
        if passkey.get("name") == "iPhone Face ID":
            return False, "Passkey 'iPhone Face ID' still exists."
    return True, "Passkey 'iPhone Face ID' successfully removed."
