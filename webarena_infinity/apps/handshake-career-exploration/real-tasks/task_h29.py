"""
Task: Save all active jobs labeled 'STEM' that are from employers you don't
currently follow.

Seed followed: emp_01, emp_03, emp_05, emp_07, emp_10, emp_12, emp_15.

STEM-labeled active jobs from non-followed employers:
- job_08 (emp_09)
- job_15 (emp_13)
- job_16 (emp_14)
- job_19 (emp_17)
- job_28 (emp_06)

Verify: all 5 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    required_jobs = {
        "job_08": "STEM job from emp_09",
        "job_15": "STEM job from emp_13",
        "job_16": "STEM job from emp_14",
        "job_19": "STEM job from emp_17",
        "job_28": "STEM job from emp_06",
    }

    missing = []
    for job_id, job_desc in required_jobs.items():
        if job_id not in saved_job_ids:
            missing.append(f"{job_desc} ({job_id})")

    if missing:
        return False, (
            f"Not all active STEM jobs from non-followed employers are saved. "
            f"Missing: {', '.join(missing)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        f"All active STEM jobs from non-followed employers saved: "
        f"job_08, job_15, job_16, job_19, job_28. "
        f"Current savedJobIds: {saved_job_ids}"
    )
