"""
Task: Unfollow every employer not in Technology or AI industry.
Save all active internships from remaining followed employers.

Discovery: Currently following: emp_01(Tech), emp_03(Tech), emp_05(Tech),
emp_07(Tech), emp_10(Tech), emp_12(Automotive!), emp_15(AI).
Unfollow: emp_12 (Tesla, Automotive).
Remaining internships not already saved:
- Google: job_01, job_02, job_22
- Microsoft: job_04, job_23
- Apple: job_06, job_25
- Meta: job_26 (job_07 already saved)
- Stripe: job_09
- Anthropic: job_29 (job_12 already saved)

Verify:
(1) emp_12 NOT in followedEmployerIds
(2) All of job_01, job_02, job_04, job_06, job_09, job_22, job_23, job_25, job_26, job_29 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: emp_12 NOT in followedEmployerIds
    followed = state.get("currentUser", {}).get("followedEmployerIds", [])
    if "emp_12" in followed:
        errors.append("emp_12 still in followedEmployerIds (should have been unfollowed)")

    # Check 2: All required jobs in savedJobIds
    saved_jobs = state.get("currentUser", {}).get("savedJobIds", [])
    required_jobs = [
        "job_01", "job_02", "job_04", "job_06", "job_09",
        "job_22", "job_23", "job_25", "job_26", "job_29"
    ]
    missing_jobs = [j for j in required_jobs if j not in saved_jobs]
    if missing_jobs:
        errors.append(f"Missing jobs in savedJobIds: {missing_jobs}")

    if errors:
        return False, " | ".join(errors)

    return True, "All checks passed: emp_12 unfollowed, all 10 required internships saved."
