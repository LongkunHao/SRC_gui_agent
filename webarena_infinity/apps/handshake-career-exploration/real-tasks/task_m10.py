import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    current_user = state.get("currentUser", {})
    user_id = current_user.get("id", "")
    user_name = current_user.get("fullName", "")

    feed_posts = state.get("feedPosts", [])

    for post in feed_posts:
        author_id = post.get("authorId", "")
        author_name = post.get("authorName", "")

        is_current_user = (author_id == user_id) or (author_name == user_name)
        if not is_current_user:
            continue

        content = post.get("content", "").lower()
        if "system design" in content:
            return True, f"Found feed post by {author_name} mentioning 'system design'."

    return False, "No feed post by the current user found containing 'system design'."
