import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Marek Kowalski (id 2) authored epics 2 (7 children) and 9 (3 children).
    # Epic 2 has the most child issues.
    epic = next((e for e in state["epics"] if e["id"] == 2), None)
    if epic is None:
        return False, "Epic 'API v3 Migration' (id 2) not found."

    # Issue #6 is the only closed child — should be removed
    if 6 in epic.get("childIssueIds", []):
        return False, f"Closed issue #6 still in epic childIssueIds: {epic['childIssueIds']}."

    if epic.get("dueDate") != "2026-06-30":
        return False, f"Epic dueDate is '{epic.get('dueDate')}', expected '2026-06-30'."

    return True, "Epic 2 has no closed children and dueDate is 2026-06-30."
