"""
Task: Find the employer affiliated with 'Twitch'. Save all their active jobs
you haven't saved and like their AWS re:Invent post.

Discovery: Twitch → Amazon (emp_09). Active jobs: job_08, job_24.
Feed post: post_07 (AWS re:Invent).

Verify:
(1) job_08 in savedJobIds
(2) job_24 in savedJobIds
(3) post_07 likes incremented (> seed value 178)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    saved = state.get("currentUser", {}).get("savedJobIds", [])
    for jid in ["job_08", "job_24"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds. Current: {saved}")

    posts = state.get("feedPosts", [])
    post_07 = next((p for p in posts if p.get("id") == "post_07"), None)
    if post_07 is None:
        errors.append("post_07 not found.")
    elif post_07.get("likes", 0) <= 178:
        errors.append(f"post_07 likes not incremented. likes={post_07.get('likes')}")

    if errors:
        return False, " | ".join(errors)
    return True, "Amazon identified via Twitch affiliation. Jobs saved and post liked."
