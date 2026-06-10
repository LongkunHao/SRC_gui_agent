import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    board = next((b for b in state["boards"] if b["name"] == "Development Board"), None)
    if not board:
        return False, "Development Board not found."
    feature_list = next((l for l in board["lists"] if l.get("labelId") == 2), None)
    if not feature_list:
        return False, "Board list for label 'feature' (id 2) not found."
    return True, "Board list for 'feature' label added to Development Board."
