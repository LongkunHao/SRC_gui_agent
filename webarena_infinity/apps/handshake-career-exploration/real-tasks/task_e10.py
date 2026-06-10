"""
Task: Save the Palantir Forward Deployed Engineer Intern job.
Verify: job_19 is in currentUser.savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    saved_jobs = current_user.get("savedJobIds", [])

    if "job_19" not in saved_jobs:
        return False, (
            f"Palantir FDE Intern (job_19) is not in currentUser.savedJobIds. "
            f"Currently saved jobs: {saved_jobs}"
        )

    return True, "Palantir Forward Deployed Engineer Intern (job_19) is saved."
