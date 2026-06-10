"""
Task: Save the Microsoft Software Engineer Intern position.
Verify: job_04 is in currentUser.savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    saved_jobs = current_user.get("savedJobIds", [])

    if "job_04" not in saved_jobs:
        return False, (
            f"Microsoft SWE Intern (job_04) is not in currentUser.savedJobIds. "
            f"Currently saved jobs: {saved_jobs}"
        )

    return True, "Microsoft Software Engineer Intern (job_04) is saved."
