import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    board = next((b for b in state["boards"] if b["name"] == "Development Board"), None)
    if board is None:
        return False, "Board 'Development Board' not found."

    old_label_ids = {15, 16, 17, 18}
    for lst in board.get("lists", []):
        if lst.get("labelId") in old_label_ids:
            return False, f"Board still has a list with old status labelId {lst['labelId']}."

    list_label_ids = {lst.get("labelId") for lst in board.get("lists", [])}

    if 1 not in list_label_ids:
        return False, f"No list with labelId 1 (bug) found on the board."

    if 2 not in list_label_ids:
        return False, f"No list with labelId 2 (feature) found on the board."

    if 4 not in list_label_ids:
        return False, f"No list with labelId 4 (performance) found on the board."

    return True, "Development Board label lists replaced: old status lists removed, bug/feature/performance lists added."
