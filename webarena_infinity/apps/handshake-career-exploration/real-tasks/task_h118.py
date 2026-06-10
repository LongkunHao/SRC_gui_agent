"""
Task: Read all your unread messages, then leave a comment on the feed post
from the employer who sent you the most recent unread message.

Discovery: Unread messages: msg_01 (Google, March 6), msg_03 (Meta, March 4),
msg_06 (Stripe, Feb 28), msg_08 (Apple, Feb 22).
Most recent: msg_01 (Google, March 6). Google post: post_01.

Verify:
(1) msg_01, msg_03, msg_06, msg_08 all isRead=True
(2) post_01 has new comment from Maya Chen
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check all unread messages are now read
    messages = state.get("messages", [])
    for mid in ["msg_01", "msg_03", "msg_06", "msg_08"]:
        msg = next((m for m in messages if m.get("id") == mid), None)
        if msg is None:
            errors.append(f"{mid} not found.")
        elif not msg.get("isRead"):
            errors.append(f"{mid} not read.")

    # Check comment on Google's post
    posts = state.get("feedPosts", [])
    post_01 = next((p for p in posts if p.get("id") == "post_01"), None)
    if post_01 is None:
        errors.append("post_01 not found.")
    else:
        maya_comment = any(
            "maya" in c.get("authorName", "").lower()
            for c in post_01.get("comments", [])
        )
        if not maya_comment:
            errors.append("No comment from Maya Chen on post_01 (Google).")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All unread messages read. Comment left on Google's post "
        "(most recent unread sender)."
    )
