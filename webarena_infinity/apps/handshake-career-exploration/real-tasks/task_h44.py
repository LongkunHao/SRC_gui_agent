"""
Task: Save all active full-time positions and unsave any internships currently in
your saved list.

Active full-time jobs: job_16 (Epic), job_17 (Salesforce), job_20 (TFA),
    job_21 (Startup Grind), job_27 (JPMorgan), job_28 (Goldman Sachs).
Seed saved (all internships): job_03, job_07, job_12, job_18, job_24.

Verify:
(1) All 6 FT jobs are in savedJobIds.
(2) All 5 seed internships are NOT in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    errors = []

    # Check 1: All active full-time jobs are saved
    ft_jobs = {
        "job_16": "Epic Technical Solutions Engineer",
        "job_17": "Salesforce SWE New Grad",
        "job_20": "Teach For America Corps Member",
        "job_21": "Startup Grind Labs Full-Stack Engineer",
        "job_27": "JPMorgan Quantitative Research Analyst",
        "job_28": "Goldman Sachs Engineering Analyst",
    }
    missing_ft = []
    for job_id, title in ft_jobs.items():
        if job_id not in saved_job_ids:
            missing_ft.append(f"{title} ({job_id})")
    if missing_ft:
        errors.append(f"Full-time jobs not saved: {', '.join(missing_ft)}")

    # Check 2: All seed internships are unsaved
    intern_jobs = {
        "job_03": "JPMorgan IB Summer Analyst",
        "job_07": "Meta ML Engineer Intern",
        "job_12": "Anthropic Research Engineer Intern",
        "job_18": "Nike PM Intern",
        "job_24": "Amazon PM Intern",
    }
    still_saved = []
    for job_id, title in intern_jobs.items():
        if job_id in saved_job_ids:
            still_saved.append(f"{title} ({job_id})")
    if still_saved:
        errors.append(f"Internships still saved: {', '.join(still_saved)}")

    if errors:
        return False, " | ".join(errors) + f" Current savedJobIds: {saved_job_ids}"

    return True, (
        "All active full-time jobs saved (job_16, job_17, job_20, job_21, job_27, job_28) "
        "and all seed internships unsaved (job_03, job_07, job_12, job_18, job_24)."
    )
