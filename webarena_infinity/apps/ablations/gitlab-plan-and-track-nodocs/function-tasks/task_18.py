import requests

def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."

    state = resp.json()
    comments = [c for c in state["comments"] if c["issueId"] == 14]
    match = [c for c in comments if "This is ready for review" in c["body"]]

    if not match:
        return False, "Comment 'This is ready for review.' not found on issue #14."

    return True, "Comment added to issue #14."
