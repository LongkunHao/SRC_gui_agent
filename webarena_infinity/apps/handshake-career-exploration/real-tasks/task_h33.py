"""
Task: Navigate to your saved posts in the feed and find the student who created a PM interview
study group. Leave a comment on their post thanking them for organizing it.
Verify: post_14 (David Lee - PM interview study group) has a comment by Maya Chen.
post_14 is in seed savedPostIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()

    feed_posts = state.get("feedPosts", [])
    post_14 = next((p for p in feed_posts if p.get("id") == "post_14"), None)
    if post_14 is None:
        return False, "Post post_14 (David Lee - PM interview study group) not found in feedPosts."

    comments = post_14.get("comments", [])
    for comment in comments:
        author = comment.get("authorName", "")
        if "maya" in author.lower():
            return True, (
                f"Found comment from Maya Chen on post_14 (David Lee - PM interview study group): "
                f"'{comment.get('text', '')[:100]}'"
            )

    return False, (
        f"No comment from Maya Chen found on post_14 (David Lee - PM interview study group). "
        f"Current comments: {[{'authorName': c.get('authorName'), 'text': c.get('text', '')[:80]} for c in comments]}"
    )
