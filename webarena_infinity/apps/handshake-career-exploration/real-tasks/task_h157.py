"""
Task: Update your bio to mention your interest in AI safety and alignment
research. Then find the employer whose about section describes building
'reliable, interpretable, and steerable AI systems'. Bookmark their feed
post and leave a comment on it expressing your interest.

Discovery: 'reliable, interpretable, and steerable AI systems' → Anthropic.
Anthropic feed post: post_05 (AI safety internships).

Verify:
(1) bio includes 'safety' and 'alignment' (case-insensitive)
(2) post_05 bookmarked + in savedPostIds
(3) post_05 has new comment from current user
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    posts = state.get("feedPosts", [])

    # Check 1: bio mentions safety + alignment
    bio = user.get("bio", "").lower()
    if "safety" not in bio:
        errors.append("Bio does not mention 'safety'.")
    if "alignment" not in bio:
        errors.append("Bio does not mention 'alignment'.")

    # Check 2: post_05 bookmarked
    post_05 = next((p for p in posts if p.get("id") == "post_05"), None)
    if post_05 is None:
        errors.append("post_05 not found.")
    else:
        if not post_05.get("bookmarked"):
            errors.append("post_05 not bookmarked.")

        # Check 3: new comment on post_05
        seed_comment_ids = {"cmt_04"}
        new_comments = [
            c for c in post_05.get("comments", [])
            if c.get("id") not in seed_comment_ids
        ]
        if not new_comments:
            errors.append("No new comment on post_05.")

    if "post_05" not in user.get("savedPostIds", []):
        errors.append("post_05 not in savedPostIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Bio updated with AI safety and alignment. "
        "Anthropic post bookmarked and commented on."
    )
