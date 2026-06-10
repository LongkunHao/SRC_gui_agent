"""
Task: Follow all private companies you aren't already following and save
their active full-time positions.

Discovery: Private employers: emp_04 (McKinsey), emp_08 (Deloitte),
emp_10 (Stripe, followed), emp_11 (Bain), emp_14 (Epic), emp_15 (Anthropic, followed),
emp_20 (Startup Grind Labs).
Not followed: emp_04, emp_08, emp_11, emp_14, emp_20.
Active FT from ANY private: job_16 (Epic), job_21 (SGL).

Verify:
(1) emp_04, emp_08, emp_11, emp_14, emp_20 in followedEmployerIds
(2) job_16, job_21 in savedJobIds
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
    for eid in ["emp_04", "emp_08", "emp_11", "emp_14", "emp_20"]:
        if eid not in followed:
            errors.append(f"{eid} not followed.")

    saved = user.get("savedJobIds", [])
    for jid in ["job_16", "job_21"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All unfollowed private companies now followed. "
        "Active FT positions (job_16, job_21) saved."
    )
