import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    ux_label = next((l for l in state["labels"] if l["name"] == "UX"), None)
    ni_label = next((l for l in state["labels"] if l["name"] == "needs-investigation"), None)
    if not ux_label or not ni_label:
        return False, "UX or needs-investigation label not found."
    ux_id = ux_label["id"]
    ni_id = ni_label["id"]

    # Open Accessibility Compliance children with frontend+UX: #22, #23, #55
    for issue_id in [22, 23, 55]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if ux_id in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} still has UX label."
        if ni_id not in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} does not have needs-investigation label."

    return True, "Issues #22, #23, #55 swapped UX for needs-investigation."
