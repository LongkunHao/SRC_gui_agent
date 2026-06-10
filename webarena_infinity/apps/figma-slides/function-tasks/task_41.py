import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    comments = state.get("comments", [])
    comment = next((c for c in comments if c.get("id") == "comment_002"), None)
    if not comment:
        return False, "Comment with id 'comment_002' not found."

    replies = comment.get("replies", [])
    if len(replies) < 1:
        return False, f"Expected comment_002 to have at least 1 reply, but found {len(replies)}."

    last_reply = replies[-1]
    expected_text = "Great idea, I will add one after the roadmap section."
    actual_text = last_reply.get("text")
    if actual_text != expected_text:
        return False, f"Expected last reply text to be '{expected_text}', but found '{actual_text}'."

    return True, "Comment comment_002 has at least 1 reply and the last reply text matches as expected."
