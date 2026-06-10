"""
Task: The student who answered the question about return offers also wrote a post
about their first week at a company. Like their post and save that company's
active jobs.

Discovery: qa_09 (return offers) -> ans_12 by Marcus Johnson -> post_04 (first
week at Stripe) -> emp_10 (Stripe) -> active jobs: job_09.

Verify:
(1) post_04.likes > 143 (seed value).
(2) job_09 in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Marcus Johnson's post liked
    posts = state.get("feedPosts", [])
    post_04 = next((p for p in posts if p.get("id") == "post_04"), None)
    if post_04 is None:
        errors.append("Post post_04 (Marcus Johnson, Stripe) not found.")
    elif post_04.get("likes", 0) <= 143:
        errors.append(
            f"post_04 (Marcus Johnson) not liked. "
            f"likes={post_04.get('likes')}, expected > 143 (seed value)."
        )

    # Check 2: Stripe's active job saved
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_09" not in saved:
        errors.append(
            f"job_09 (Stripe Backend Engineer Intern) not saved. "
            f"Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Marcus Johnson identified from return offers Q&A (qa_09). "
        "His post (post_04) liked and Stripe job (job_09) saved."
    )
