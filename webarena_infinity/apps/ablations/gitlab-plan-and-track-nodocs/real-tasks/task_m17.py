import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "CI/CD Pipeline" in e["title"]), None)
    if epic is None:
        return False, "Epic with 'CI/CD Pipeline' in title not found."

    if 74 not in epic.get("childIssueIds", []):
        return False, f"Issue #74 not in epic childIssueIds: {epic.get('childIssueIds', [])}."

    issue = next((i for i in state["issues"] if i["id"] == 74), None)
    if issue is None:
        return False, "Issue #74 not found."

    if issue.get("milestoneId") != 4:
        return False, f"Issue #74 milestoneId is {issue.get('milestoneId')}, expected 4."

    return True, "Issue #74 added to CI/CD Pipeline epic and milestone changed to v2.1."
