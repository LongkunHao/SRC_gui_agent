"""
Task: Follow all employers headquartered in New York and save all their active internship positions.
Verify: (1) emp_02 (JPMorgan), emp_04 (McKinsey), emp_06 (Goldman Sachs), emp_08 (Deloitte),
emp_13 (Spotify), emp_18 (Teach For America) all in followedEmployerIds.
(2) Active internships from NY employers: job_05 (McKinsey), job_11 (Deloitte), job_15 (Spotify)
all in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: All NY employers followed
    followed = current_user.get("followedEmployerIds", [])
    ny_employers = {
        "emp_02": "JPMorgan Chase",
        "emp_04": "McKinsey & Company",
        "emp_06": "Goldman Sachs",
        "emp_08": "Deloitte",
        "emp_13": "Spotify",
        "emp_18": "Teach For America",
    }
    missing_follows = []
    for emp_id, emp_name in ny_employers.items():
        if emp_id not in followed:
            missing_follows.append(f"{emp_name} ({emp_id})")
    if missing_follows:
        errors.append(
            f"NY employers not followed: {', '.join(missing_follows)}. "
            f"Currently following: {followed}"
        )

    # Check 2: Active internships from NY employers saved
    saved_job_ids = current_user.get("savedJobIds", [])
    ny_active_internships = {
        "job_05": "Business Analyst Intern (McKinsey)",
        "job_11": "Technology Consulting Intern (Deloitte)",
        "job_15": "Data Science Intern (Spotify)",
    }
    missing_jobs = []
    for job_id, job_title in ny_active_internships.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Active NY internships not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All NY employers followed (emp_02, emp_04, emp_06, emp_08, emp_13, emp_18) "
        "and active NY internships saved (job_05, job_11, job_15)."
    )
