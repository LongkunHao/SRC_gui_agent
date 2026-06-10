import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    comments = state.get("comments", [])
    comment = next((c for c in comments if c.get("id") == "comment_001"), None)
    if not comment:
        return False, "Comment with id 'comment_001' not found."

    resolved = comment.get("resolved")
    if resolved is not True:
        return False, f"Expected comment_001 resolved to be True, but found {resolved}."

    return True, "Comment comment_001 has resolved == True as expected."
