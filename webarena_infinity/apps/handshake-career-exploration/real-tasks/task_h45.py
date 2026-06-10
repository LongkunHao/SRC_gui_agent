"""
Task: The most helpful answer on the salary negotiation Q&A was written by a student
who also posted in the feed. Like and bookmark that student's post.

Discovery: qa_05 is about salary negotiation. ans_07 (Jordan Taylor, 89 helpful) is
the most helpful. Jordan Taylor wrote post_12 (startup vs Big Tech, 412 likes).

Verify:
(1) post_12.likes > 412 (seed).
(2) post_12.bookmarked == True.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    feed_posts = state.get("feedPosts", [])
    post_12 = next((p for p in feed_posts if p.get("id") == "post_12"), None)
    if post_12 is None:
        return False, "Post post_12 (Jordan Taylor) not found in feedPosts."

    # Check 1: Post liked
    likes = post_12.get("likes", 0)
    if likes <= 412:
        errors.append(
            f"post_12 (Jordan Taylor) likes={likes}, expected > 412 (seed=412)."
        )

    # Check 2: Post bookmarked
    if post_12.get("bookmarked") != True:
        errors.append(
            f"post_12 (Jordan Taylor) not bookmarked. bookmarked={post_12.get('bookmarked')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Jordan Taylor's post (post_12) liked (likes={likes}) and bookmarked. "
        "Correctly identified from salary negotiation Q&A most helpful answer."
    )
