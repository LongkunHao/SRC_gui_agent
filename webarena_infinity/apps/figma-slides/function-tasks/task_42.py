import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    comments = state.get("comments", [])
    comment = next((c for c in comments if c.get("id") == "comment_006"), None)
    if comment is not None:
        return False, "Comment with id 'comment_006' still exists but should have been deleted."

    if len(comments) != 5:
        return False, f"Expected 5 comments after deleting comment_006, but found {len(comments)}."

    return True, "Comment comment_006 has been deleted and total comments is 5 as expected."
