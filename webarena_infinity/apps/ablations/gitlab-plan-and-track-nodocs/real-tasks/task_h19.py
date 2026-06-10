import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    epic = next((e for e in state["epics"] if "Enterprise SSO" in e.get("title", "")), None)
    if epic is None:
        return False, "Epic containing 'Enterprise SSO' not found."

    if epic.get("confidential") is not False:
        return False, f"Epic 'Enterprise SSO' confidential is {epic.get('confidential')}, expected False."

    for issue_id in [57, 58, 59]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if issue.get("confidential") is not False:
            return False, f"Issue #{issue_id} confidential is {issue.get('confidential')}, expected False."

    return True, "Enterprise SSO epic and children (#57, #58, #59) are no longer confidential."
