"""
Task: Like all feed posts from publicly-traded employers.

Employer posts and their company type:
- post_01: Google (emp_01, Public) -> LIKE
- post_03: Meta (emp_07, Public) -> LIKE
- post_05: Anthropic (emp_15, Private) -> skip
- post_07: Amazon (emp_09, Public) -> LIKE
- post_09: McKinsey (emp_04, Private) -> skip
- post_11: Apple (emp_05, Public) -> LIKE
- post_13: Stripe (emp_10, Private) -> skip
- post_15: JPMorgan (emp_02, Public) -> LIKE
- post_17: TFA (emp_18, Nonprofit) -> skip
- post_19: Microsoft (emp_03, Public) -> LIKE

Verify: post_01, post_03, post_07, post_11, post_15, post_19 likes all increased.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    posts = state.get("feedPosts", [])
    errors = []

    # Posts from public employers with their seed like counts
    public_posts = {
        "post_01": ("Google", 342),
        "post_03": ("Meta", 256),
        "post_07": ("Amazon", 178),
        "post_11": ("Apple", 289),
        "post_15": ("JPMorgan Chase", 134),
        "post_19": ("Microsoft", 312),
    }

    for post_id, (name, seed_likes) in public_posts.items():
        post = next((p for p in posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"{post_id} ({name}) not found.")
        elif post.get("likes", 0) <= seed_likes:
            errors.append(
                f"{post_id} ({name}) not liked. "
                f"likes={post.get('likes')}, expected > {seed_likes}."
            )

    if errors:
        return False, (
            f"Not all publicly-traded employer posts liked. Issues: "
            + " | ".join(errors)
        )

    return True, (
        "All publicly-traded employer posts liked: "
        "post_01 (Google), post_03 (Meta), post_07 (Amazon), "
        "post_11 (Apple), post_15 (JPMorgan), post_19 (Microsoft)."
    )
