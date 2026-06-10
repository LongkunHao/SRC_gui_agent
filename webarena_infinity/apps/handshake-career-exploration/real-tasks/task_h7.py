"""
Task: Save all Google and Microsoft internships.
Verify: All Google internships (job_01, job_02, job_22) and Microsoft internships
(job_04, job_23) are in savedJobIds. All five are active internship-type jobs.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    required_jobs = {
        "job_01": "Google - Software Engineering Intern, Summer 2026",
        "job_02": "Google - Associate Product Manager Intern",
        "job_22": "Google - UX Design Intern",
        "job_04": "Microsoft - Software Engineer Intern",
        "job_23": "Microsoft - Program Manager Intern",
    }

    missing = []
    for job_id, job_desc in required_jobs.items():
        if job_id not in saved_job_ids:
            missing.append(f"{job_desc} ({job_id})")

    if missing:
        return False, (
            f"Not all Google and Microsoft internships are saved. "
            f"Missing: {', '.join(missing)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        f"All Google and Microsoft internships are saved: "
        f"job_01, job_02, job_22, job_04, job_23. "
        f"Current savedJobIds: {saved_job_ids}"
    )
