"""
Task: Follow all employers with 10,000 or more employees that you aren't already
following, and save each of their active internship positions.

10,000+ employers not followed in seed:
- emp_02 (JPMorgan) -> no active internships (job_03 closed)
- emp_06 (Goldman Sachs) -> no active internships (job_10 closed)
- emp_08 (Deloitte) -> job_11 (Internship, active)
- emp_09 (Amazon) -> job_08 (Internship, active), job_24 (already saved)
- emp_16 (Nike) -> job_18 (Internship, active, already saved)
- emp_19 (Salesforce) -> job_30 (Internship, active)

Verify:
(1) emp_02, emp_06, emp_08, emp_09, emp_16, emp_19 in followedEmployerIds.
(2) job_08, job_11, job_30 in savedJobIds (job_18, job_24 already saved).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: All 10K+ employers followed
    followed = current_user.get("followedEmployerIds", [])
    must_follow = {
        "emp_02": "JPMorgan Chase",
        "emp_06": "Goldman Sachs",
        "emp_08": "Deloitte",
        "emp_09": "Amazon",
        "emp_16": "Nike",
        "emp_19": "Salesforce",
    }
    missing_follows = []
    for emp_id, name in must_follow.items():
        if emp_id not in followed:
            missing_follows.append(f"{name} ({emp_id})")
    if missing_follows:
        errors.append(
            f"10,000+ employee employers not followed: {', '.join(missing_follows)}. "
            f"Current followedEmployerIds: {followed}"
        )

    # Check 2: Active internships saved
    saved = current_user.get("savedJobIds", [])
    required_jobs = {
        "job_08": "Amazon SDE Intern",
        "job_11": "Deloitte Technology Consulting Intern",
        "job_18": "Nike PM Intern",
        "job_24": "Amazon PM Intern",
        "job_30": "Salesforce Marketing Analyst Intern",
    }
    missing_jobs = []
    for job_id, title in required_jobs.items():
        if job_id not in saved:
            missing_jobs.append(f"{title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Internships from 10K+ employers not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All 10,000+ employee employers now followed "
        "(emp_02, emp_06, emp_08, emp_09, emp_16, emp_19) and their active "
        "internships saved (job_08, job_11, job_18, job_24, job_30)."
    )
