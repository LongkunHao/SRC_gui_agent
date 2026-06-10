import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    issue = next((i for i in state["issues"] if i["id"] == 29), None)
    if not issue:
        return False, "Issue #29 not found."

    # v2.1 — Integrations = milestone id 4
    if issue["milestoneId"] != 4:
        return False, f"Issue #29 milestoneId is {issue['milestoneId']}, expected 4 (v2.1 — Integrations)."

    return True, "Issue #29 milestone changed to 'v2.1 — Integrations'."
