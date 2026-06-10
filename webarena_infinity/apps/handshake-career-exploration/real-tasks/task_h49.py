"""
Task: Save all active jobs from employers hosting upcoming on-campus events.

Upcoming on-campus (non-virtual) events with employers:
- evt_01: McKinsey (emp_04) → job_05 (active intern)
- evt_04: Google (emp_01) → job_01, job_02, job_22 (all active)
- evt_08: JPMorgan (emp_02) → job_27 (active FT; job_03 is closed)
(evt_03, evt_05, evt_09 are Stanford career center events with no employer.)

Verify: job_01, job_02, job_05, job_22, job_27 all in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    required_jobs = {
        "job_01": "Google SWE Intern",
        "job_02": "Google APM Intern",
        "job_05": "McKinsey Business Analyst Intern",
        "job_22": "Google UX Design Intern",
        "job_27": "JPMorgan Quantitative Research Analyst",
    }

    missing_jobs = []
    for job_id, title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{title} ({job_id})")

    if missing_jobs:
        return False, (
            f"Not all active jobs from on-campus event hosts are saved. "
            f"Missing: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        "All active jobs from on-campus event host employers saved: "
        "McKinsey (job_05), Google (job_01, job_02, job_22), JPMorgan (job_27)."
    )
