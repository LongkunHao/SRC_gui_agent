import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Label 'stale' must exist with color #95a5a6
    stale = next((l for l in state["labels"] if l["name"] == "stale"), None)
    if stale is None:
        return False, "Label 'stale' not found."
    if stale.get("color") != "#95a5a6":
        return False, f"Label 'stale' color is '{stale.get('color')}', expected '#95a5a6'."

    stale_id = stale["id"]

    # Issues in Backlog (milestone 6) with no assignees and weight <= 3:
    # #68, #105, #116, #122
    for issue_id in [68, 105, 116, 122]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if stale_id not in issue.get("labelIds", []):
            return False, (
                f"Issue #{issue_id} does not have 'stale' label (id {stale_id}). "
                f"Labels: {issue.get('labelIds')}."
            )

    return True, "Label 'stale' created and applied to issues #68, #105, #116, #122."
