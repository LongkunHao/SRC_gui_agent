import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Notification System Revamp epic author is Priya Sharma (id 5)
    epic = next((e for e in state["epics"] if "Notification System Revamp" in e.get("title", "")), None)
    if epic is None:
        return False, "Epic 'Notification System Revamp' not found."

    author_id = epic["authorId"]  # 5

    todo_label = next((l for l in state["labels"] if l["name"] == "status::to-do"), None)
    if todo_label is None:
        return False, "Label 'status::to-do' not found."
    todo_id = todo_label["id"]

    for issue_id in [63, 64, 65]:
        issue = next((i for i in state["issues"] if i["id"] == issue_id), None)
        if issue is None:
            return False, f"Issue #{issue_id} not found."
        if author_id not in issue.get("assigneeIds", []):
            return False, f"Issue #{issue_id} does not have author (id {author_id}) as assignee."
        if todo_id not in issue.get("labelIds", []):
            return False, f"Issue #{issue_id} does not have status::to-do label."

    return True, "All Notification System Revamp children have author assigned and status::to-do."
