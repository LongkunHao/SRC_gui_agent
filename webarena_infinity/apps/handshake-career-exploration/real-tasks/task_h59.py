"""
Task: Like all student posts in the feed that have more than 300 likes.

Student posts with > 300 likes (seed values):
- post_08 (Kevin O'Brien): 534 likes
- post_12 (Jordan Taylor): 412 likes
- post_16 (Nathan Brooks): 325 likes

Verify: post_08.likes > 534, post_12.likes > 412, post_16.likes > 325.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    feed_posts = state.get("feedPosts", [])
    errors = []

    posts_to_check = {
        "post_08": ("Kevin O'Brien", 534),
        "post_12": ("Jordan Taylor", 412),
        "post_16": ("Nathan Brooks", 325),
    }

    for post_id, (author, seed_likes) in posts_to_check.items():
        post = next((p for p in feed_posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"Post {post_id} ({author}) not found.")
            continue
        likes = post.get("likes", 0)
        if likes <= seed_likes:
            errors.append(
                f"{post_id} ({author}) likes={likes}, expected > {seed_likes} "
                f"(seed={seed_likes}). Post was not liked."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All student posts with >300 likes were liked: "
        "post_08 (Kevin O'Brien), post_12 (Jordan Taylor), post_16 (Nathan Brooks)."
    )
