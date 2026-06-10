"""
Task: Two students posted about interview preparation in the feed — one shared a FAANG
study plan and another shared takeaways from a PM interview book. Comment on the FAANG
study plan post asking about their timeline, and bookmark the PM book post.

Disambiguation:
- post_08 (Kevin O'Brien): FAANG interview prep study plan → comment
- post_18 (Sophia Williams): Takeaways from 'Cracking the PM Interview' → bookmark
- post_14 (David Lee): PM study group — NOT a book post, should not be targeted

Verify:
(1) post_08 has a new comment (comments length > seed 3).
(2) post_18.bookmarked == True.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    feed_posts = state.get("feedPosts", [])

    # Check 1: Comment added to FAANG study plan post
    post_08 = next((p for p in feed_posts if p.get("id") == "post_08"), None)
    if post_08 is None:
        errors.append("Post post_08 (Kevin O'Brien FAANG prep) not found.")
    else:
        comments = post_08.get("comments", [])
        if len(comments) <= 3:
            errors.append(
                f"post_08 has {len(comments)} comments, expected > 3 (seed=3). "
                f"No new comment was added."
            )

    # Check 2: PM book post bookmarked
    post_18 = next((p for p in feed_posts if p.get("id") == "post_18"), None)
    if post_18 is None:
        errors.append("Post post_18 (Sophia Williams PM book) not found.")
    elif post_18.get("bookmarked") != True:
        errors.append(
            f"post_18 (Sophia Williams PM book) not bookmarked. "
            f"bookmarked={post_18.get('bookmarked')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "FAANG study plan post (post_08) commented on and "
        "PM interview book post (post_18) bookmarked."
    )
