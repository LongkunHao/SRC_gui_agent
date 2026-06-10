import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Karl Fischer (id 9) reported the most open bugs (16).
    # Unassigned open security issues: #57, #58, #59.
    karl_id = 9

    for issue_id in [57, 58, 59]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if karl_id not in issue.get("assigneeIds", []):
            return False, (
                f"Karl Fischer (id {karl_id}) not in issue #{issue_id} "
                f"assigneeIds: {issue.get('assigneeIds')}."
            )

    return True, "Karl Fischer assigned to issues #57, #58, #59."
