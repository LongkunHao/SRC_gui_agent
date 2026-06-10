"""
Task: Save all active jobs from employers that have messaged you but that you
don't currently follow.

Message senders not followed in seed:
- emp_04 (McKinsey) -> job_05 (active)
- emp_09 (Amazon) -> job_08 (active), job_24 (active, already saved)
- emp_02 (JPMorgan) -> job_27 (active), job_03 (closed)
- emp_19 (Salesforce) -> job_17 (active), job_30 (active)
- emp_11 (Bain) -> job_14 (closed)

Verify: job_05, job_08, job_17, job_24, job_27, job_30 all in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    required_jobs = {
        "job_05": "McKinsey Business Analyst Intern",
        "job_08": "Amazon SDE Intern",
        "job_17": "Salesforce Software Engineer New Grad",
        "job_24": "Amazon PM Intern",
        "job_27": "JPMorgan Quantitative Research Analyst",
        "job_30": "Salesforce Marketing Analyst Intern",
    }

    missing = []
    for job_id, title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing.append(f"{title} ({job_id})")

    if missing:
        return False, (
            f"Not all active jobs from non-followed message senders are saved. "
            f"Missing: {missing}. Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        "All active jobs from non-followed message senders saved: "
        "job_05, job_08, job_17, job_24, job_27, job_30."
    )
