"""
Task: Read your message from Stripe, then find and like the feed post written by
the same person featured in Stripe's alumni testimonial.

Discovery: msg_06 from Stripe (unread). Stripe testimonial: Marcus Johnson.
Marcus Johnson's post: post_04.

Verify:
(1) msg_06.isRead == True.
(2) post_04.likes > 143 (seed value).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Stripe message read
    messages = state.get("messages", [])
    msg_06 = next((m for m in messages if m.get("id") == "msg_06"), None)
    if msg_06 is None:
        errors.append("Message msg_06 (Stripe) not found.")
    elif msg_06.get("isRead") != True:
        errors.append(
            f"msg_06 (Stripe) not read. isRead={msg_06.get('isRead')}"
        )

    # Check 2: Marcus Johnson's post liked
    posts = state.get("feedPosts", [])
    post_04 = next((p for p in posts if p.get("id") == "post_04"), None)
    if post_04 is None:
        errors.append("Post post_04 (Marcus Johnson) not found.")
    elif post_04.get("likes", 0) <= 143:
        errors.append(
            f"post_04 (Marcus Johnson) not liked. "
            f"likes={post_04.get('likes')}, expected > 143."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Stripe message (msg_06) read. Marcus Johnson (Stripe testimonial "
        "author) identified and his post (post_04) liked."
    )
