"""
Task: In Q&A, find the approved answer with the fewest helpful votes (among those
with at least one vote). That student also posted in the feed. Leave a comment on
their post praising their Q&A advice.

Discovery: Helpful counts across all answers (seed):
ans_06 (Emma Rodriguez): 29 <- fewest with >= 1
ans_12 (Marcus Johnson): 35
ans_05 (Sarah Kim): 38
...
Emma Rodriguez's post: post_10.

Verify: New comment on post_10 by Maya Chen.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()

    posts = state.get("feedPosts", [])
    post_10 = next((p for p in posts if p.get("id") == "post_10"), None)
    if post_10 is None:
        return False, "Post post_10 (Emma Rodriguez) not found."

    # Seed has 1 comment (from Maya Chen about Spotify redesign).
    # Need a NEW comment from Maya Chen.
    comments = post_10.get("comments", [])
    new_comments = [
        c for c in comments
        if c.get("authorName") == "Maya Chen"
        and c.get("id") != "cmt_10"  # exclude seed comment
    ]

    if not new_comments:
        return False, (
            f"No new comment from Maya Chen on post_10 (Emma Rodriguez). "
            f"Expected a comment praising her Q&A advice. "
            f"Current comments: {[c.get('authorName') for c in comments]}"
        )

    return True, (
        "Emma Rodriguez identified as having the fewest helpful votes (ans_06, 29). "
        "New comment left on her post (post_10)."
    )
