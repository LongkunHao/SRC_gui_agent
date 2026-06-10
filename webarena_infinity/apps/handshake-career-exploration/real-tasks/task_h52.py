"""
Task: Your saved jobs include a closed position. Remove it, then follow the employers
of your remaining saved jobs that you aren't already following.

Seed savedJobIds: job_03 (JPMorgan, closed), job_07 (Meta), job_12 (Anthropic),
    job_18 (Nike), job_24 (Amazon).
Seed followedEmployerIds: emp_01, emp_03, emp_05, emp_07, emp_10, emp_12, emp_15.

After removing job_03:
- job_07 → Meta (emp_07, already followed)
- job_12 → Anthropic (emp_15, already followed)
- job_18 → Nike (emp_16, NOT followed) → follow
- job_24 → Amazon (emp_09, NOT followed) → follow

Verify:
(1) job_03 NOT in savedJobIds.
(2) emp_16 (Nike) and emp_09 (Amazon) in followedEmployerIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    errors = []

    # Check 1: Closed job removed
    saved_job_ids = current_user.get("savedJobIds", [])
    if "job_03" in saved_job_ids:
        errors.append(
            f"job_03 (JPMorgan IB, closed) should be unsaved but is still in savedJobIds."
        )

    # Check 2: Employers of remaining saved jobs are followed
    followed = current_user.get("followedEmployerIds", [])
    must_follow = {
        "emp_16": "Nike",
        "emp_09": "Amazon",
    }
    missing_follows = []
    for emp_id, name in must_follow.items():
        if emp_id not in followed:
            missing_follows.append(f"{name} ({emp_id})")
    if missing_follows:
        errors.append(
            f"Employers of remaining saved jobs not followed: "
            f"{', '.join(missing_follows)}. Current followedEmployerIds: {followed}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Closed job (job_03) removed from saved list. "
        "Employers of remaining saved jobs now followed (emp_09 Amazon, emp_16 Nike)."
    )
