"""
Task: Find employer whose alumni testimonial mentions Azure. Save their active jobs,
like their Imagine Cup post, add IT & Infrastructure to job functions.

Discovery: Microsoft (emp_03) testimonial by Alex Rivera mentions "Azure".
Active jobs: job_04, job_23. Imagine Cup post: post_19 (312 likes seed).

Verify:
(1) job_04 in savedJobIds
(2) job_23 in savedJobIds
(3) post_19.likes > 312
(4) "IT & Infrastructure" in careerInterests.jobFunctions
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: job_04 in savedJobIds
    saved_jobs = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_04" not in saved_jobs:
        errors.append("job_04 not found in savedJobIds")

    # Check 2: job_23 in savedJobIds
    if "job_23" not in saved_jobs:
        errors.append("job_23 not found in savedJobIds")

    # Check 3: post_19.likes > 312
    feed_posts = state.get("feedPosts", [])
    post_19 = None
    for post in feed_posts:
        if post.get("id") == "post_19":
            post_19 = post
            break
    if post_19 is None:
        errors.append("post_19 not found in feedPosts")
    else:
        likes = post_19.get("likes", 0)
        if likes <= 312:
            errors.append(f"post_19.likes is {likes}, expected > 312")

    # Check 4: "IT & Infrastructure" in careerInterests.jobFunctions
    career_interests = state.get("currentUser", {}).get("careerInterests", {})
    job_functions = career_interests.get("jobFunctions", [])
    if "IT & Infrastructure" not in job_functions:
        errors.append(f"'IT & Infrastructure' not found in careerInterests.jobFunctions: {job_functions}")

    if errors:
        return False, " | ".join(errors)

    return True, "All checks passed: job_04 and job_23 saved, post_19 liked, IT & Infrastructure added to job functions."
