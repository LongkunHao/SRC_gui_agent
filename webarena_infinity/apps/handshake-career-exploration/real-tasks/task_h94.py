"""
Task: Like every student feed post written by someone who also answered a Q&A question.

Discovery: Students who both posted AND answered Q&A:
- Kevin O'Brien: post_08 (534 likes), answered qa_06
- Marcus Johnson: post_04 (143 likes), answered qa_09
- Jordan Taylor: post_12 (412 likes), answered qa_05
- Emma Rodriguez: post_10 (89 likes), answered qa_04
- Aisha Mohammed: post_06 (231 likes), answered qa_11
- Nathan Brooks: post_16 (325 likes), answered qa_12
- David Lee: post_14 (276 likes), answered qa_07

Verify:
(1) post_08.likes > 534
(2) post_04.likes > 143
(3) post_12.likes > 412
(4) post_10.likes > 89
(5) post_06.likes > 231
(6) post_16.likes > 325
(7) post_14.likes > 276
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    feed_posts = state.get("feedPosts", [])

    target_posts = {
        "post_08": ("Kevin O'Brien", 534),
        "post_04": ("Marcus Johnson", 143),
        "post_12": ("Jordan Taylor", 412),
        "post_10": ("Emma Rodriguez", 89),
        "post_06": ("Aisha Mohammed", 231),
        "post_16": ("Nathan Brooks", 325),
        "post_14": ("David Lee", 276),
    }

    for post_id, (author, seed_likes) in target_posts.items():
        post = next((p for p in feed_posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"{post_id} ({author}) not found in feedPosts.")
            continue

        current_likes = post.get("likes", 0)
        if current_likes <= seed_likes:
            errors.append(
                f"{post_id} ({author}) likes={current_likes}, expected > {seed_likes} (seed={seed_likes})."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All 7 student posts by Q&A answerers liked: "
        "post_08 (Kevin O'Brien), post_04 (Marcus Johnson), post_12 (Jordan Taylor), "
        "post_10 (Emma Rodriguez), post_06 (Aisha Mohammed), post_16 (Nathan Brooks), "
        "post_14 (David Lee)."
    )
