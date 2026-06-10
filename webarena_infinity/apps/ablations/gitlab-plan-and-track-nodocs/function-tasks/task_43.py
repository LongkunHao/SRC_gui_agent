import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    epic = next((e for e in state["epics"] if e["title"] == "Mobile Responsive Redesign"), None)
    if not epic:
        return False, "Epic 'Mobile Responsive Redesign' not found."

    if 30 not in epic["childIssueIds"]:
        return False, "Issue #30 not found in epic's child issues."

    return True, "Issue #30 added to epic 'Mobile Responsive Redesign'."
