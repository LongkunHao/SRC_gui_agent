"""
Task: Bookmark the Amazon AWS re:Invent post.
Verify: post_07 has bookmarked == True AND post_07 id is in currentUser.savedPostIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    feed_posts = state.get("feedPosts", [])
    current_user = state.get("currentUser", {})
    saved_post_ids = current_user.get("savedPostIds", [])

    post = next((p for p in feed_posts if p.get("id") == "post_07"), None)
    if post is None:
        return False, "Post post_07 (Amazon AWS re:Invent) not found in feedPosts."

    if post.get("bookmarked") != True:
        return False, (
            f"Post post_07 (Amazon AWS re:Invent) is not bookmarked. "
            f"bookmarked={post.get('bookmarked')}"
        )

    if "post_07" not in saved_post_ids:
        return False, (
            f"Post post_07 is bookmarked but not in currentUser.savedPostIds. "
            f"savedPostIds={saved_post_ids}"
        )

    return True, "Amazon AWS re:Invent post (post_07) is bookmarked and in savedPostIds."
