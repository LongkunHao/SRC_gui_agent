import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    ni_label = next((l for l in state["labels"] if l["name"] == "needs-investigation"), None)
    if ni_label is None:
        return False, "Label 'needs-investigation' not found."
    ni_id = ni_label["id"]

    # Open issues with 'is_blocked_by' in relatedIssues: #2, #7, #8, #47, #61, #62
    for issue_id in [2, 7, 8, 47, 61, 62]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if ni_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} does not have needs-investigation label. "
                f"Labels: {issue.get('labelIds')}."
            )

    return True, "All blocked issues (#2, #7, #8, #47, #61, #62) have needs-investigation label."
