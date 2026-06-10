import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check 'needs-review' label exists
    nr_label = next((l for l in state["labels"] if l["name"] == "needs-review"), None)
    if nr_label is None:
        return False, "Label 'needs-review' not found."

    if nr_label.get("color") != "#3498db":
        return False, f"Label 'needs-review' color is '{nr_label.get('color')}', expected '#3498db'."

    nr_id = nr_label["id"]

    # Open issues in API v3 Migration epic with status::to-do: #8, #47
    for issue_id in [8, 47]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if nr_id not in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} does not have 'needs-review' label."

    return True, "Label 'needs-review' created and applied to issues #8, #47."
