import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    for e in state["emails"]:
        if e["subject"] == "Budget Approval Needed - Marketing Campaign" and e["from"]["name"] == "Priya Sharma":
            if e["isRead"] is False:
                return True, "The budget email from Priya Sharma is marked as unread."
            return False, f"The budget email from Priya Sharma is not unread (isRead={e['isRead']})."

    return False, "Could not find the budget email from Priya Sharma."
