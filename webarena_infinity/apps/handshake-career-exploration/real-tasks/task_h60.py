"""
Task: Follow all Technology industry employers you aren't already following, then save
their active internship positions.

Technology employers not followed in seed:
- emp_09 (Amazon) → internships: job_08, job_24 (job_24 already saved)
- emp_17 (Palantir) → internships: job_19
- emp_19 (Salesforce) → internships: job_30
- emp_20 (Startup Grind Labs) → no internships (job_21 is Full-time)

Verify:
(1) emp_09, emp_17, emp_19, emp_20 in followedEmployerIds.
(2) job_08, job_19, job_24, job_30 in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: All unfollowed Technology employers are now followed
    followed = current_user.get("followedEmployerIds", [])
    must_follow = {
        "emp_09": "Amazon",
        "emp_17": "Palantir Technologies",
        "emp_19": "Salesforce",
        "emp_20": "Startup Grind Labs",
    }
    missing_follows = []
    for emp_id, name in must_follow.items():
        if emp_id not in followed:
            missing_follows.append(f"{name} ({emp_id})")
    if missing_follows:
        errors.append(
            f"Technology employers not followed: {', '.join(missing_follows)}. "
            f"Current followedEmployerIds: {followed}"
        )

    # Check 2: Active internships from newly followed employers are saved
    saved_job_ids = current_user.get("savedJobIds", [])
    required_jobs = {
        "job_08": "Amazon SDE Intern",
        "job_19": "Palantir FDE Intern",
        "job_24": "Amazon PM Intern",
        "job_30": "Salesforce Marketing Analyst Intern",
    }
    missing_jobs = []
    for job_id, title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Internships not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All unfollowed Technology employers now followed "
        "(emp_09, emp_17, emp_19, emp_20) and their active internships saved "
        "(job_08, job_19, job_24, job_30)."
    )
