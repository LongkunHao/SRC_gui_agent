import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [l for l in state["labels"] if l["name"] == "blocked"]
    if not match:
        return False, "Label 'blocked' not found."
    label = match[0]
    if label["color"] != "#e74c3c":
        return False, f"Color is '{label['color']}', expected '#e74c3c'."
    if label["description"] != "Work is blocked by external dependencies":
        return False, f"Description is '{label['description']}', expected 'Work is blocked by external dependencies'."
    return True, "Label 'blocked' created with correct color and description."
