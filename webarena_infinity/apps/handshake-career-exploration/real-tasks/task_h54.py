"""
Task: Like every employer post in the feed where the employer has at least one active
job with the 'AI/ML' label.

Jobs with AI/ML label: job_07 (Meta), job_12 (Anthropic), job_25 (Apple), job_29 (Anthropic).
Employers: Meta (emp_07), Anthropic (emp_15), Apple (emp_05).
Their feed posts: post_03 (Meta, 256), post_05 (Anthropic, 198), post_11 (Apple, 289).

Verify: post_03.likes > 256, post_05.likes > 198, post_11.likes > 289.
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
        "post_03": ("Meta", 256),
        "post_05": ("Anthropic", 198),
        "post_11": ("Apple", 289),
    }

    for post_id, (employer_name, seed_likes) in posts_to_check.items():
        post = next((p for p in feed_posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"Post {post_id} ({employer_name}) not found.")
            continue
        likes = post.get("likes", 0)
        if likes <= seed_likes:
            errors.append(
                f"{post_id} ({employer_name}) likes={likes}, "
                f"expected > {seed_likes} (seed={seed_likes})."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All employer posts with AI/ML labeled jobs liked: "
        "post_03 (Meta), post_05 (Anthropic), post_11 (Apple)."
    )
