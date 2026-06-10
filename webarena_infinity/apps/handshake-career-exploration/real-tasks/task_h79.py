"""
Task: Like every student post in the feed written by someone who doesn't attend
Stanford University.

Student posts:
- post_02: Jessica Park, Stanford -> SKIP
- post_04: Marcus Johnson, Michigan -> LIKE
- post_06: Aisha Mohammed, Howard -> LIKE
- post_08: Kevin O'Brien, MIT -> LIKE
- post_10: Emma Rodriguez, Stanford -> SKIP
- post_12: Jordan Taylor, Northwestern -> LIKE
- post_14: David Lee, UC Berkeley -> LIKE
- post_16: Nathan Brooks, Rice -> LIKE
- post_18: Sophia Williams, Harvard -> LIKE
- post_20: Rachel Kim, Yale -> LIKE

Verify: 8 posts liked (post_04, 06, 08, 12, 14, 16, 18, 20).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    posts = state.get("feedPosts", [])
    errors = []

    # Non-Stanford student posts with seed like counts
    target_posts = {
        "post_04": ("Marcus Johnson", 143),
        "post_06": ("Aisha Mohammed", 231),
        "post_08": ("Kevin O'Brien", 534),
        "post_12": ("Jordan Taylor", 412),
        "post_14": ("David Lee", 276),
        "post_16": ("Nathan Brooks", 325),
        "post_18": ("Sophia Williams", 267),
        "post_20": ("Rachel Kim", 145),
    }

    for post_id, (author, seed_likes) in target_posts.items():
        post = next((p for p in posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"{post_id} ({author}) not found.")
        elif post.get("likes", 0) <= seed_likes:
            errors.append(
                f"{post_id} ({author}) not liked. "
                f"likes={post.get('likes')}, expected > {seed_likes}."
            )

    if errors:
        return False, (
            f"Not all non-Stanford student posts liked. Issues: "
            + " | ".join(errors)
        )

    return True, (
        "All 8 non-Stanford student posts liked: post_04, 06, 08, 12, 14, 16, 18, 20."
    )
