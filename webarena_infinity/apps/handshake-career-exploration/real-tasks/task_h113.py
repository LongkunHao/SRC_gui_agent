"""
Task: Find the employer with the second-highest follower count on Handshake.
Like their feed post and save all their active internships.

Discovery: Follower counts: Apple (52300), Amazon (47600, 2nd).
Amazon post: post_07. Active internships: job_08 (SDE Intern), job_24 (PM Intern).

Verify:
(1) post_07 likes > 178 (seed)
(2) job_08 in savedJobIds
(3) job_24 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    posts = state.get("feedPosts", [])
    post_07 = next((p for p in posts if p.get("id") == "post_07"), None)
    if post_07 is None:
        errors.append("post_07 not found.")
    elif post_07.get("likes", 0) <= 178:
        errors.append(
            f"post_07 likes not incremented. Expected > 178, got {post_07.get('likes')}"
        )

    saved = state.get("currentUser", {}).get("savedJobIds", [])
    for jid in ["job_08", "job_24"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Amazon identified as 2nd-highest followers. "
        "Post liked and internships (job_08, job_24) saved."
    )
