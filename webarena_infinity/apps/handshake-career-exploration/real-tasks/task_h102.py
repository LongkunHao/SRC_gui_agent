"""
Task: In the feed, bookmark every student post with fewer than 200 likes,
and like every student post with 200 or more likes.

Student posts (seed likes):
  < 200: post_02 (187), post_04 (143), post_10 (89), post_20 (145)
  >= 200: post_06 (231), post_08 (534), post_12 (412), post_14 (276),
          post_16 (325), post_18 (267)

Verify:
(1) post_02, post_04, post_10, post_20 bookmarked
(2) post_06, post_08, post_12, post_14, post_16, post_18 likes incremented
"""

import requests

SEED_LIKES = {
    "post_06": 231, "post_08": 534, "post_12": 412,
    "post_14": 276, "post_16": 325, "post_18": 267,
}


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    posts = {p["id"]: p for p in state.get("feedPosts", [])}

    # Check bookmarks on < 200 likes posts
    for pid in ["post_02", "post_04", "post_10", "post_20"]:
        post = posts.get(pid)
        if post is None:
            errors.append(f"{pid} not found.")
        elif not post.get("bookmarked"):
            errors.append(f"{pid} not bookmarked.")

    # Check likes on >= 200 likes posts
    for pid, seed in SEED_LIKES.items():
        post = posts.get(pid)
        if post is None:
            errors.append(f"{pid} not found.")
        elif post.get("likes", 0) <= seed:
            errors.append(
                f"{pid} likes not incremented (seed={seed}, current={post.get('likes')})"
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All student posts correctly handled: "
        "< 200 likes bookmarked, >= 200 likes liked."
    )
