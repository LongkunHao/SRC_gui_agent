import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "API v3 Migration" in e["title"]), None)
    if epic is None:
        return False, "Epic with 'API v3 Migration' in title not found."

    child_ids = epic.get("childIssueIds", [])

    if 48 in child_ids:
        return False, f"Issue #48 should not be in childIssueIds but is still present: {child_ids}."

    if 121 not in child_ids:
        return False, f"Issue #121 not in childIssueIds: {child_ids}."

    return True, "Epic 'API v3 Migration' has #48 removed and #121 added to child issues."
