import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "Enterprise SSO Integration" in e.get("title", "")), None)
    if epic is None:
        return False, "Epic 'Enterprise SSO Integration' not found."

    # Open issues with both security (5) and backend (7) labels: #1, #2, #3, #45
    # (#58 and #59 also match but are already children)
    expected_new = [1, 2, 3, 45]
    for issue_id in expected_new:
        if issue_id not in epic.get("childIssueIds", []):
            return False, (
                f"Issue #{issue_id} not in epic childIssueIds: {epic.get('childIssueIds')}."
            )

    return True, f"Issues {expected_new} added as children of Enterprise SSO Integration epic."
