"""
Task: Go to your saved posts and leave a comment on each one thanking the author
for their insight.

Seed savedPostIds: post_02, post_08, post_14.
All three are student posts:
- post_02: Jessica Park (Meta return offer)
- post_08: Kevin O'Brien (FAANG prep)
- post_14: David Lee (PM study group)

Verify: New comment from Maya Chen on each of post_02, post_08, post_14.
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
        "post_02": ("Jessica Park", ["cmt_01", "cmt_02"]),
        "post_08": ("Kevin O'Brien", ["cmt_07", "cmt_08", "cmt_09"]),
        "post_14": ("David Lee", ["cmt_13", "cmt_14", "cmt_15"]),
    }

    for post_id, (author, seed_comment_ids) in target_posts.items():
        post = next((p for p in posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"{post_id} ({author}) not found.")
            continue

        comments = post.get("comments", [])
        new_maya_comments = [
            c for c in comments
            if c.get("authorName") == "Maya Chen"
            and c.get("id") not in seed_comment_ids
        ]

        if not new_maya_comments:
            errors.append(
                f"No new comment from Maya Chen on {post_id} ({author}'s post)."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Comments left on all saved posts: post_02 (Jessica Park), "
        "post_08 (Kevin O'Brien), post_14 (David Lee)."
    )
