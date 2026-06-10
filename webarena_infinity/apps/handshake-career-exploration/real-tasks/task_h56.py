"""
Task: Save all active jobs located in Seattle or New York.

Seattle active jobs: job_08 (Amazon SDE Intern), job_24 (Amazon PM Intern, already saved).
New York active jobs: job_15 (Spotify DS Intern), job_27 (JPMorgan Quant FT),
    job_28 (Goldman Sachs Engineering FT).
(Closed NYC jobs job_03 and job_10 are excluded.)

Verify: job_08, job_15, job_24, job_27, job_28 all in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    required_jobs = {
        "job_08": "Amazon SDE Intern (Seattle)",
        "job_15": "Spotify Data Science Intern (New York)",
        "job_24": "Amazon PM Intern (Seattle)",
        "job_27": "JPMorgan Quantitative Research (New York)",
        "job_28": "Goldman Sachs Engineering Analyst (New York)",
    }

    missing_jobs = []
    for job_id, title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{title} ({job_id})")

    if missing_jobs:
        return False, (
            f"Not all active Seattle/NYC jobs saved. "
            f"Missing: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        "All active Seattle and New York jobs saved: "
        "job_08, job_15, job_24, job_27, job_28."
    )
