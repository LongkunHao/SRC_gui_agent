import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [l for l in state["labels"] if l["name"] == "documentation"]
    if match:
        return False, "Label 'documentation' still exists."
    # Check no issues reference label id 3
    for issue in state["issues"]:
        if 3 in issue.get("labelIds", []):
            return False, f"Issue #{issue['id']} still references label id 3."
    return True, "Label 'documentation' deleted and removed from all issues."
