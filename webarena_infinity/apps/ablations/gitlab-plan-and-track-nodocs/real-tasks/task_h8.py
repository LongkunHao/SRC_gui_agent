import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    api_epic = next((e for e in state["epics"] if "API v3 Migration" in e.get("title", "")), None)
    if api_epic is None:
        return False, "Epic containing 'API v3 Migration' not found."

    if 47 in api_epic.get("childIssueIds", []):
        return False, f"Issue #47 still in 'API v3 Migration' epic's childIssueIds."

    perf_epic = next((e for e in state["epics"] if e.get("title") == "Performance Optimization Phase 2"), None)
    if perf_epic is None:
        return False, "Epic 'Performance Optimization Phase 2' not found."

    if 47 not in perf_epic.get("childIssueIds", []):
        return False, f"Issue #47 not in 'Performance Optimization Phase 2' epic's childIssueIds: {perf_epic.get('childIssueIds')}."

    issue = next((i for i in state["issues"] if i["id"] == 47), None)
    if issue is None:
        return False, "Issue #47 not found."

    if issue.get("milestoneId") != 4:
        return False, f"Issue #47 milestoneId is {issue.get('milestoneId')}, expected 4."

    if 12 not in issue.get("labelIds", []):
        return False, f"Label priority::high (id 12) not in issue #47 labelIds: {issue.get('labelIds')}."

    if 13 in issue.get("labelIds", []):
        return False, f"Label priority::medium (id 13) still in issue #47 labelIds: {issue.get('labelIds')}."

    return True, "Issue #47 moved to Performance Optimization Phase 2 epic with milestoneId 4 and priority::high."
