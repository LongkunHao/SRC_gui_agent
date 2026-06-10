import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    label = next((l for l in state["labels"] if l["name"] == "blocked"), None)
    if label is None:
        return False, "Label 'blocked' not found."

    if label.get("color", "").lower() != "#e74c3c":
        return False, f"Label 'blocked' color is '{label.get('color')}', expected '#e74c3c'."

    label_id = label["id"]

    for issue_id in [7, 8, 47]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if label_id not in issue.get("labelIds", []):
            return False, f"Label 'blocked' (id {label_id}) not in issue #{issue_id} labelIds: {issue.get('labelIds')}."

    return True, "Label 'blocked' created with color #e74c3c and applied to issues #7, #8, #47."
