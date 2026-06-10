import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    comments = state.get("comments", [])
    comment = next((c for c in comments if c.get("id") == "comment_003"), None)
    if not comment:
        return False, "Comment with id 'comment_003' not found."

    resolved = comment.get("resolved")
    if resolved is not False:
        return False, f"Expected comment_003 resolved to be False (unresolved), but found {resolved}."

    return True, "Comment comment_003 has resolved == False (unresolved) as expected."
