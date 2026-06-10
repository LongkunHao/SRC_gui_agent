"""
Task: Find the most-viewed question in the Q&A community and create a post visible
only to your school recommending that topic to fellow students.

Most viewed: qa_05 (1567 views) about salary negotiation.

Verify: new post by Maya Chen (authorId='stu_8f3a2c81' or authorName='Maya Chen')
with audience='school' containing 'salary' or 'negotiat' (case-insensitive).
"""

import requests
import re


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    feed_posts = state.get("feedPosts", [])
    current_user = state.get("currentUser", {})
    user_id = current_user.get("id", "")
    user_name = current_user.get("fullName", "")

    for post in feed_posts:
        author_id = post.get("authorId", "")
        author_name = post.get("authorName", "")

        is_by_user = (
            author_id == user_id
            or author_id == "stu_8f3a2c81"
            or author_name == user_name
            or author_name == "Maya Chen"
        )
        if not is_by_user:
            continue

        audience = post.get("audience", "")
        content = post.get("content", "").lower()

        if audience == "school" and (
            "salary" in content or "negotiat" in content
        ):
            return True, (
                f"Found post by {author_name} with audience='school' about "
                f"salary negotiation. Content: '{post.get('content', '')[:100]}...'"
            )

    # Diagnostic info
    user_posts = [
        {
            "id": p.get("id"),
            "authorName": p.get("authorName"),
            "audience": p.get("audience"),
            "content": p.get("content", "")[:80],
        }
        for p in feed_posts
        if p.get("authorId") == user_id
        or p.get("authorId") == "stu_8f3a2c81"
        or p.get("authorName") == user_name
        or p.get("authorName") == "Maya Chen"
    ]
    return False, (
        f"No post by Maya Chen with audience='school' containing 'salary' or "
        f"'negotiat' found. User posts: {user_posts}"
    )
