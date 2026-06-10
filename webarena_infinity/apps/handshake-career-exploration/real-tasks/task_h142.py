"""
Task: The student who posted about their first week at Stripe also appears
in Stripe's alumni testimonials. Like that student's feed post. Then find the
employer that sent you an unread message mentioning 'Pathways' and bookmark
their most recent feed post.

Discovery: Marcus Johnson → post_04 (Stripe first week) + Stripe testimonial.
Pathways message → msg_08 from Apple → post_11 (Apple Pathways program).

Verify:
(1) post_04 likes > 143
(2) post_11 bookmarked
(3) post_11 in savedPostIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    posts = state.get("feedPosts", [])

    # Check 1: post_04 liked
    post_04 = next((p for p in posts if p.get("id") == "post_04"), None)
    if post_04 is None:
        errors.append("post_04 not found.")
    elif post_04.get("likes", 0) <= 143:
        errors.append(
            f"post_04 likes not incremented. "
            f"Expected > 143, got {post_04.get('likes')}"
        )

    # Check 2-3: post_11 bookmarked
    post_11 = next((p for p in posts if p.get("id") == "post_11"), None)
    if post_11 is None:
        errors.append("post_11 not found.")
    elif not post_11.get("bookmarked"):
        errors.append("post_11 not bookmarked.")

    saved_posts = user.get("savedPostIds", [])
    if "post_11" not in saved_posts:
        errors.append("post_11 not in savedPostIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Marcus Johnson's post liked. "
        "Apple Pathways post bookmarked."
    )
