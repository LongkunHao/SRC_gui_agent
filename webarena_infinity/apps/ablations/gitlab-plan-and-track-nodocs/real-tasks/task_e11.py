import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    label = next((l for l in state["labels"] if l["name"] == "breaking-change"), None)
    if label is not None:
        return False, "Label 'breaking-change' still exists."

    return True, "Label 'breaking-change' has been deleted."
