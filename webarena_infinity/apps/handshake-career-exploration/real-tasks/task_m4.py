import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    feed_posts = state.get("feedPosts", [])

    for post in feed_posts:
        if post.get("id") == "post_02":
            comments = post.get("comments", [])
            for comment in comments:
                comment_text = comment.get("text", "").lower()
                if "congrats" in comment_text:
                    return True, f"Found comment containing 'Congrats' on post_02: '{comment.get('text', '')}'"
            return False, f"No comment containing 'Congrats' found on post_02. Comments: {comments}"

    return False, "Post post_02 not found in feedPosts."
