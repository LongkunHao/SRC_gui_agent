"""
Task: Unsave any closed jobs from your saved list.
Verify: No closed jobs remain in savedJobIds. In seed data, job_03 (JPMorgan IB) is
closed and in savedJobIds. After the task, job_03 should NOT be in savedJobIds.
Also dynamically verify that no job in savedJobIds has status=='closed'.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    jobs = state.get("jobs", [])

    # Specific check: job_03 is the known closed job in seed savedJobIds
    if "job_03" in saved_job_ids:
        return False, (
            f"job_03 (JPMorgan Investment Banking Summer Analyst, closed) is still "
            f"in savedJobIds. It should have been removed. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Dynamic check: verify no saved job has status 'closed'
    closed_saved = []
    for job_id in saved_job_ids:
        job = next((j for j in jobs if j.get("id") == job_id), None)
        if job and job.get("status") == "closed":
            closed_saved.append(f"{job.get('title', 'Unknown')} ({job_id})")

    if closed_saved:
        return False, (
            f"Closed jobs still in savedJobIds: {', '.join(closed_saved)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    return True, (
        f"No closed jobs in savedJobIds. "
        f"Current savedJobIds: {saved_job_ids}"
    )
