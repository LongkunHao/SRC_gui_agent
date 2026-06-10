"""
Task: Save all active Google jobs to your list.
Verify: job_01 (SWE Intern), job_02 (APM Intern), job_22 (UX Design Intern) are all in savedJobIds.
All three are Google (emp_01) jobs with status='active'.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    google_active_jobs = {
        "job_01": "Software Engineering Intern, Summer 2026",
        "job_02": "Associate Product Manager Intern",
        "job_22": "UX Design Intern",
    }

    missing = []
    for job_id, job_title in google_active_jobs.items():
        if job_id not in saved_job_ids:
            missing.append(f"{job_title} ({job_id})")

    if missing:
        return False, (
            f"Not all active Google jobs are saved. Missing: {', '.join(missing)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        f"All active Google jobs are saved: job_01, job_02, job_22. "
        f"Current savedJobIds: {saved_job_ids}"
    )
