import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    board = next((b for b in state["boards"] if b["name"] == "Development Board"), None)
    if not board:
        return False, "Development Board not found."

    # Done list has labelId 18 (status::done)
    done_list = next((l for l in board["lists"] if l.get("labelId") == 18), None)
    if done_list:
        return False, "Done list (labelId 18) still exists on Development Board."

    return True, "Done list removed from Development Board."
