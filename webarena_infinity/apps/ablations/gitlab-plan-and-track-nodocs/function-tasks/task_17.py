import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["title"] == "Security audit findings Q1"), None)
    if not issue:
        return False, "Issue 'Security audit findings Q1' not found."

    if issue["confidential"] is not True:
        return False, f"Issue confidential is {issue['confidential']}, expected True."

    # security = label id 5
    if 5 not in issue["labelIds"]:
        return False, "Label 'security' (id 5) not found on the issue."

    return True, "Confidential issue 'Security audit findings Q1' created with 'security' label."
