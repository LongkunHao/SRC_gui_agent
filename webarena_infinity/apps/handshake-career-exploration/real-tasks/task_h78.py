"""
Task: One of the past events was a design speaker series. Find which employer
hosted it, save all their active jobs you haven't saved, and like their feed post.

Discovery: evt_12 (Apple Design Speaker Series, past) -> emp_05 (Apple).
Apple active jobs: job_06 (HW Eng Intern), job_25 (ML/AI Intern). Neither saved.
Apple feed post: post_11.

Verify:
(1) job_06 and job_25 in savedJobIds.
(2) post_11.likes > 289 (seed value).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Apple's active jobs saved
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    required_jobs = {
        "job_06": "Apple Hardware Engineering Intern",
        "job_25": "Apple ML/AI Intern",
    }
    for job_id, title in required_jobs.items():
        if job_id not in saved:
            errors.append(
                f"{job_id} ({title}) not saved. Current savedJobIds: {saved}"
            )

    # Check 2: Apple's feed post liked
    posts = state.get("feedPosts", [])
    post_11 = next((p for p in posts if p.get("id") == "post_11"), None)
    if post_11 is None:
        errors.append("Post post_11 (Apple) not found.")
    elif post_11.get("likes", 0) <= 289:
        errors.append(
            f"post_11 (Apple) not liked. likes={post_11.get('likes')}, expected > 289."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Apple identified from past Design Speaker Series (evt_12). "
        "Active jobs saved (job_06, job_25) and post (post_11) liked."
    )
