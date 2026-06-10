import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    board = next((b for b in state["boards"] if b["name"] == "Development Board"), None)
    if not board:
        return False, "Development Board not found."

    # bug label = id 1
    bug_list = next((l for l in board["lists"] if l.get("labelId") == 1), None)
    if not bug_list:
        return False, "Board list for 'bug' label not found on Development Board."

    return True, "Board list for 'bug' label added to Development Board."
