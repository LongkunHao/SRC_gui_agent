import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    posts = state.get("feedPosts", [])
    post_09 = next((p for p in posts if p.get("id") == "post_09"), None)
    if post_09 is None:
        return False, "Post post_09 not found in state."

    comments = post_09.get("comments", [])
    # Seed data has 0 comments on post_09. Look for a new comment containing "project".
    for comment in comments:
        text = comment.get("text", "").lower()
        if "project" in text:
            return True, f"Found comment on post_09 containing 'project': '{comment.get('text')}'"

    return False, (
        f"No comment containing 'project' found on post_09. "
        f"Current comments: {[c.get('text', '')[:80] for c in comments]}"
    )
