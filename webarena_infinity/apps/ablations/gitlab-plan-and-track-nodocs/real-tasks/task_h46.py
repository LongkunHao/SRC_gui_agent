import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # The only incident-type issue is #41 (weight 13, assignees [5, 6]).
    # Its related issue is #33 (related_to).
    incident = next((i for i in state["issues"] if i.get("type") == "incident"), None)
    if incident is None:
        return False, "No incident-type issue found."

    related = incident.get("relatedIssues", [])
    if not related:
        return False, "Incident issue has no related issues."

    related_id = related[0]["issueId"]  # 33
    related_issue = next((i for i in state["issues"] if i["id"] == related_id), None)
    if related_issue is None:
        return False, f"Related issue #{related_id} not found."

    if related_issue.get("weight") != incident.get("weight"):
        return False, (
            f"Related issue #{related_id} weight is {related_issue.get('weight')}, "
            f"expected {incident.get('weight')} (matching incident)."
        )

    for aid in incident.get("assigneeIds", []):
        if aid not in related_issue.get("assigneeIds", []):
            return False, (
                f"Assignee {aid} from incident not in related issue #{related_id} "
                f"assigneeIds: {related_issue.get('assigneeIds')}."
            )

    return True, f"Related issue #{related_id} matches incident weight and assignees."
