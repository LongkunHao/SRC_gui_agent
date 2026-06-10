"""
Task: Save all active internships posted by private companies, and follow any
private companies you aren't already following.

Private employers: emp_04 (McKinsey), emp_08 (Deloitte), emp_10 (Stripe),
emp_11 (Bain), emp_14 (Epic), emp_15 (Anthropic), emp_20 (Startup Grind Labs).

Active internships from private companies:
- job_05 (emp_04), job_09 (emp_10), job_11 (emp_08),
- job_12 (emp_15), job_29 (emp_15)

Seed followed: emp_01, emp_03, emp_05, emp_07, emp_10, emp_12, emp_15
(emp_10 and emp_15 already followed)
Must follow: emp_04, emp_08, emp_11, emp_14, emp_20

Verify:
- All 5 jobs in savedJobIds
- All 5 unfollowed private employers in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: All active internships from private companies are saved
    saved_job_ids = current_user.get("savedJobIds", [])
    required_jobs = {
        "job_05": "McKinsey Management Consulting Intern",
        "job_09": "Stripe Backend Engineer Intern",
        "job_11": "Deloitte Consulting Intern",
        "job_12": "Anthropic Research Engineer Intern",
        "job_29": "Anthropic Policy Research Intern",
    }

    missing_jobs = []
    for job_id, job_title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")

    if missing_jobs:
        errors.append(
            f"Not all active internships from private companies are saved. "
            f"Missing: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Check 2: All previously-unfollowed private companies are now followed
    followed = current_user.get("followedEmployerIds", [])
    must_follow = {
        "emp_04": "McKinsey & Company",
        "emp_08": "Deloitte",
        "emp_11": "Bain & Company",
        "emp_14": "Epic Systems",
        "emp_20": "Startup Grind Labs",
    }

    missing_follows = []
    for emp_id, emp_name in must_follow.items():
        if emp_id not in followed:
            missing_follows.append(f"{emp_name} ({emp_id})")

    if missing_follows:
        errors.append(
            f"Not all private companies are followed. "
            f"Missing: {', '.join(missing_follows)}. "
            f"Current followedEmployerIds: {followed}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"All active internships from private companies saved "
        f"(job_05, job_09, job_11, job_12, job_29) and all previously-unfollowed "
        f"private companies now followed (emp_04, emp_08, emp_11, emp_14, emp_20)."
    )
