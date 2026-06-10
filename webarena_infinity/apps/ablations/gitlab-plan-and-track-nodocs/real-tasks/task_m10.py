import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    board = next((b for b in state["boards"] if b["name"] == "Development Board"), None)
    if board is None:
        return False, "Board 'Development Board' not found."

    lists = board.get("lists", [])

    in_progress_list = next((l for l in lists if l.get("labelId") == 16), None)
    if in_progress_list is not None:
        return False, "Board still has a list with labelId 16 (In Progress); it should have been removed."

    performance_list = next((l for l in lists if l.get("labelId") == 4), None)
    if performance_list is None:
        return False, f"Board does not have a list with labelId 4 (performance). Current lists: {lists}."

    return True, "Development Board updated: In Progress list removed and performance list added."
