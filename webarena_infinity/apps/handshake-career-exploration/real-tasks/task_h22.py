"""
Task: Like the feed post written by the student who answered the question about
transitioning from liberal arts to a tech career.

qa_12 answered by Nathan Brooks (ans_14). Nathan Brooks has post_16 (seed likes=325).

Verify: post_16.likes > 325
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    feed_posts = state.get("feedPosts", [])

    post_16 = next((p for p in feed_posts if p.get("id") == "post_16"), None)
    if post_16 is None:
        return False, "Post post_16 (Nathan Brooks) not found in feedPosts."

    likes = post_16.get("likes", 0)
    if likes <= 325:
        return False, (
            f"Post post_16 (Nathan Brooks) has likes={likes}, expected > 325 "
            f"(seed value is 325). The post was not liked."
        )

    return True, (
        f"Post post_16 (Nathan Brooks) has been liked. "
        f"likes={likes} (seed was 325)."
    )
