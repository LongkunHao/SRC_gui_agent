"""
Task: Some of your saved jobs are from employers you haven't followed yet.
Find and follow each of those employers.

Discovery: Saved jobs → check employer follow status.
Saved: job_03 (emp_02 JPMorgan, NOT followed), job_07 (emp_07 Meta, followed),
       job_12 (emp_15 Anthropic, followed), job_18 (emp_16 Nike, NOT followed),
       job_24 (emp_09 Amazon, NOT followed).

Verify:
(1) emp_02 in followedEmployerIds
(2) emp_16 in followedEmployerIds
(3) emp_09 in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    followed = user.get("followedEmployerIds", [])

    for emp_id, name in [("emp_02", "JPMorgan Chase"), ("emp_16", "Nike"), ("emp_09", "Amazon")]:
        if emp_id not in followed:
            errors.append(f"{emp_id} ({name}) not in followedEmployerIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All employers of saved jobs are now followed: "
        "JPMorgan Chase, Nike, Amazon."
    )
