import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    comments = state.get("comments", [])

    # Check no comment from Viewer collaborators
    # In seed data, Viewers are: James O'Brien (user_004), Tom Nguyen (user_006)
    viewer_names = ["James O'Brien", "Tom Nguyen"]

    for c in comments:
        author = c.get("author", c.get("userName", ""))
        if isinstance(author, dict):
            author = author.get("name", "")
        user_id = c.get("userId", c.get("authorId", ""))

        for vname in viewer_names:
            if vname in str(author):
                errors.append(f"Comment from Viewer '{vname}' should have been deleted")
        if user_id in ("user_004", "user_006"):
            errors.append(f"Comment from Viewer user ({user_id}) should have been deleted")

    # All remaining comments should be resolved
    for c in comments:
        comment_id = c.get("id", "unknown")
        if c.get("resolved") is not True:
            errors.append(f"Comment {comment_id} has resolved={c.get('resolved')}, expected True")

    if errors:
        return False, "; ".join(errors)
    return True, "Comments from Viewer collaborators deleted, all remaining comments resolved"
