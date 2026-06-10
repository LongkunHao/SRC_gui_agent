"""
Task: Like all feed posts from employers in the Consulting or Finance industries, follow those
employers, and save all their active job listings.
Verify:
(1) post_09 (McKinsey, Consulting, seed likes=167) likes > 167.
(2) post_15 (JPMorgan, Finance, seed likes=134) likes > 134.
(3) emp_02 (JPMorgan) and emp_04 (McKinsey) in followedEmployerIds.
(4) Active jobs from emp_04: job_05. Active jobs from emp_02: job_27 (job_03 is closed).
    job_05 and job_27 in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1 & 2: Posts liked
    feed_posts = state.get("feedPosts", [])

    post_09 = next((p for p in feed_posts if p.get("id") == "post_09"), None)
    if post_09 is None:
        errors.append("Post post_09 (McKinsey) not found in feedPosts.")
    else:
        likes = post_09.get("likes", 0)
        if likes <= 167:
            errors.append(
                f"post_09 (McKinsey) likes={likes}, expected > 167 (seed=167)."
            )

    post_15 = next((p for p in feed_posts if p.get("id") == "post_15"), None)
    if post_15 is None:
        errors.append("Post post_15 (JPMorgan) not found in feedPosts.")
    else:
        likes = post_15.get("likes", 0)
        if likes <= 134:
            errors.append(
                f"post_15 (JPMorgan) likes={likes}, expected > 134 (seed=134)."
            )

    # Check 3: Employers followed
    followed = state.get("currentUser", {}).get("followedEmployerIds", [])
    if "emp_02" not in followed:
        errors.append(
            f"emp_02 (JPMorgan Chase) not in followedEmployerIds. Currently following: {followed}"
        )
    if "emp_04" not in followed:
        errors.append(
            f"emp_04 (McKinsey & Company) not in followedEmployerIds. Currently following: {followed}"
        )

    # Check 4: Active jobs saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    active_jobs = {
        "job_05": "Business Analyst Intern (McKinsey)",
        "job_27": "Quantitative Research Analyst (JPMorgan)",
    }
    missing_jobs = []
    for job_id, job_title in active_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Active jobs not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Consulting/Finance employer posts liked (post_09, post_15), "
        "employers followed (emp_02, emp_04), "
        "and active jobs saved (job_05, job_27)."
    )
