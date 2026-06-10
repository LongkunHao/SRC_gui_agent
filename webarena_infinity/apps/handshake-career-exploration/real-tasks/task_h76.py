"""
Task: Bookmark the feed posts from all employers hosting upcoming tech talks.

Upcoming tech talks:
- evt_04: Google (emp_01), type='Tech Talk' -> post_01
- evt_06: Anthropic (emp_15), type='Tech Talk' -> post_05

Verify: post_01 and post_05 bookmarked.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    posts = state.get("feedPosts", [])
    errors = []

    target_posts = {
        "post_01": "Google",
        "post_05": "Anthropic",
    }

    for post_id, employer in target_posts.items():
        post = next((p for p in posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"{post_id} ({employer}) not found.")
        elif post.get("bookmarked") != True:
            errors.append(
                f"{post_id} ({employer}) not bookmarked. "
                f"bookmarked={post.get('bookmarked')}"
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Feed posts from tech talk hosts bookmarked: "
        "post_01 (Google) and post_05 (Anthropic)."
    )
