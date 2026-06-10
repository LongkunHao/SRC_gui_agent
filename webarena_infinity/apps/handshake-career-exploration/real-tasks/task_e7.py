"""
Task: Like Jordan Taylor's post about choosing a startup over Big Tech.
Verify: post_12 likes > 412.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    feed_posts = state.get("feedPosts", [])

    post = next((p for p in feed_posts if p.get("id") == "post_12"), None)
    if post is None:
        return False, "Post post_12 (Jordan Taylor startup post) not found in feedPosts."

    likes = post.get("likes", 0)
    if likes <= 412:
        return False, (
            f"Post post_12 (Jordan Taylor startup) has {likes} likes, expected > 412. "
            f"The like action may not have been performed."
        )

    return True, (
        f"Jordan Taylor's startup post (post_12) has been liked. likes={likes}."
    )
