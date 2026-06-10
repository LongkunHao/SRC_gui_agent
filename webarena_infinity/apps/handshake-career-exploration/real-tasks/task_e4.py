"""
Task: Remove the Meta ML Engineer Intern from saved jobs.
Verify: job_07 is NOT in currentUser.savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    saved_jobs = current_user.get("savedJobIds", [])

    if "job_07" in saved_jobs:
        return False, (
            f"Meta ML Engineer Intern (job_07) is still in currentUser.savedJobIds. "
            f"The job has not been unsaved. Currently saved jobs: {saved_jobs}"
        )

    return True, "Meta ML Engineer Intern (job_07) has been removed from saved jobs."
