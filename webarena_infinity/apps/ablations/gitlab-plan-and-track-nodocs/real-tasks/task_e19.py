import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    board = next((b for b in state["boards"] if b["name"] == "Development Board"), None)
    if board is None:
        return False, "Board 'Development Board' not found."

    review_list = next((l for l in board["lists"] if l.get("labelId") == 17), None)
    if review_list is not None:
        return False, "Development Board still has a Review list (labelId 17)."

    return True, "Development Board no longer has a Review list (labelId 17)."
