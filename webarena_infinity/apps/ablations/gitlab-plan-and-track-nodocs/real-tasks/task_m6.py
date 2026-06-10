import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    label = next((l for l in state["labels"] if l["name"] == "regression"), None)
    if label is None:
        return False, "Label with name 'regression' not found."

    if label.get("color", "").lower() != "#c0392b":
        return False, f"Label color is '{label.get('color')}', expected '#c0392b'."

    issue = next((i for i in state["issues"] if i["id"] == 35), None)
    if issue is None:
        return False, "Issue #35 not found."

    if label["id"] not in issue.get("labelIds", []):
        return False, f"Label 'regression' (id {label['id']}) not in issue #35 labelIds: {issue.get('labelIds', [])}."

    return True, "Label 'regression' created with correct color and applied to issue #35."
