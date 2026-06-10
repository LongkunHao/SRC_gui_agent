import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()
    match = [i for i in state["issues"] if i["title"] == "Production database outage alert"]
    if not match:
        return False, "Issue 'Production database outage alert' not found."
    issue = match[0]
    if issue["type"] != "incident":
        return False, f"Issue type is '{issue['type']}', expected 'incident'."
    if issue["status"] != "open":
        return False, f"Issue status is '{issue['status']}', expected 'open'."
    return True, "Issue 'Production database outage alert' created with type 'incident'."
