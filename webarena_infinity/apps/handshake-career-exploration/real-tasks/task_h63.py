"""
Task: Find the employer on Handshake with the fewest followers. Follow them and
save all their active jobs.

Discovery: emp_20 (Startup Grind Labs) has 420 followers (fewest).
Active jobs: job_21 (Full-Stack Engineer).

Verify:
(1) emp_20 in followedEmployerIds.
(2) job_21 in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: Startup Grind Labs followed
    followed = current_user.get("followedEmployerIds", [])
    if "emp_20" not in followed:
        errors.append(
            f"Startup Grind Labs (emp_20, fewest followers at 420) not followed. "
            f"Current followedEmployerIds: {followed}"
        )

    # Check 2: Their active job saved
    saved = current_user.get("savedJobIds", [])
    if "job_21" not in saved:
        errors.append(
            f"job_21 (Startup Grind Labs Full-Stack Engineer) not saved. "
            f"Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Startup Grind Labs (emp_20, fewest followers) followed and "
        "their active job (job_21) saved."
    )
