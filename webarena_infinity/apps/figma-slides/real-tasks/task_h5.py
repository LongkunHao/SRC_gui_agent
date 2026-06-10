import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"
    state = resp.json()

    errors = []

    comments = state.get("comments", [])

    # Previously resolved comments (comment_003 from Priya, comment_006 from David) should be deleted
    for c in comments:
        author = c.get("author", c.get("userName", c.get("user", {}).get("name", "")))
        if isinstance(author, dict):
            author = author.get("name", "")
        text = c.get("text", c.get("content", ""))
        comment_id = c.get("id", "")

        # Check for Priya Sharma's resolved comment
        if "Priya" in str(author) and "Sharma" in str(author):
            errors.append(f"Comment from Priya Sharma should have been deleted (was resolved)")
        if comment_id == "comment_003":
            errors.append(f"comment_003 (previously resolved) should have been deleted")

        # Check for David's resolved comment
        if "David" in str(author) and ("Park" in str(author) or True):
            # Check if this was the resolved one on slide_001
            slide_id = c.get("slideId", "")
            if slide_id == "slide_001" or comment_id == "comment_006":
                errors.append(f"Comment from David on title slide should have been deleted (was resolved)")
        if comment_id == "comment_006":
            errors.append(f"comment_006 (previously resolved) should have been deleted")

    # All remaining comments should be resolved
    for c in comments:
        comment_id = c.get("id", "unknown")
        if c.get("resolved") is not True:
            errors.append(f"Comment {comment_id} has resolved={c.get('resolved')}, expected True")

    if errors:
        return False, "; ".join(errors)
    return True, "Resolved comments deleted, all remaining comments are now resolved"
