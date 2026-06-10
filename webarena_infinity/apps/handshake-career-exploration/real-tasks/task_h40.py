"""
Task: Read all unread messages from Technology industry employers, then bookmark those same
employers' posts in the feed.
Verify:
(1) Unread messages from Tech employers: msg_01 (Google), msg_03 (Meta), msg_06 (Stripe),
    msg_08 (Apple). All must have isRead==True.
(2) Feed posts from those 4 employers: post_01 (Google), post_03 (Meta), post_13 (Stripe),
    post_11 (Apple). All must have bookmarked==True.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Messages read
    messages = state.get("messages", [])
    unread_msgs = {
        "msg_01": "Google - top match for SWE Intern",
        "msg_03": "Meta - ML Engineer Intern",
        "msg_06": "Stripe - Backend Engineer Intern",
        "msg_08": "Apple - Pathways invitation",
    }
    still_unread = []
    for msg_id, msg_desc in unread_msgs.items():
        msg = next((m for m in messages if m.get("id") == msg_id), None)
        if msg is None:
            errors.append(f"Message {msg_id} ({msg_desc}) not found in messages list.")
            continue
        if msg.get("isRead") != True:
            still_unread.append(f"{msg_desc} ({msg_id})")
    if still_unread:
        errors.append(
            f"Messages still unread: {', '.join(still_unread)}"
        )

    # Check 2: Posts bookmarked
    feed_posts = state.get("feedPosts", [])
    required_bookmarks = {
        "post_01": "Google",
        "post_03": "Meta",
        "post_13": "Stripe",
        "post_11": "Apple",
    }
    not_bookmarked = []
    for post_id, employer_name in required_bookmarks.items():
        post = next((p for p in feed_posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"Post {post_id} ({employer_name}) not found in feedPosts.")
            continue
        if post.get("bookmarked") != True:
            not_bookmarked.append(f"{employer_name} ({post_id})")
    if not_bookmarked:
        errors.append(
            f"Posts not bookmarked: {', '.join(not_bookmarked)}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All unread tech employer messages read (msg_01, msg_03, msg_06, msg_08) "
        "and their posts bookmarked (post_01, post_03, post_11, post_13)."
    )
