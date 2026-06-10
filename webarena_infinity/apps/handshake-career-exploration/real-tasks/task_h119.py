"""
Task: Bookmark the feed posts from all employers that have at least two
active job listings on Handshake.

Discovery: Employers with >= 2 active jobs:
  Google (3): post_01
  Microsoft (2): post_19
  Apple (2): post_11
  Meta (2): post_03
  Amazon (2): post_07
  Anthropic (2): post_05

Verify:
(1) post_01, post_03, post_05, post_07, post_11, post_19 all bookmarked
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    posts = {p["id"]: p for p in state.get("feedPosts", [])}

    target_posts = ["post_01", "post_03", "post_05", "post_07", "post_11", "post_19"]
    for pid in target_posts:
        post = posts.get(pid)
        if post is None:
            errors.append(f"{pid} not found.")
        elif not post.get("bookmarked"):
            errors.append(f"{pid} not bookmarked.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All employer posts from companies with >= 2 active jobs bookmarked: "
        "post_01, post_03, post_05, post_07, post_11, post_19."
    )
