"""
Task: You follow two employers that each have exactly one active job listing.
Save the job from the one headquartered in San Francisco, and unfollow
the other one.

Discovery: Followed employers with exactly 1 active job:
  Stripe (emp_10, San Francisco) → job_09 (Backend Engineer Intern)
  Tesla (emp_12, Austin) → job_13 (Mechanical Engineering Intern)

Verify:
(1) job_09 in savedJobIds
(2) emp_12 NOT in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})

    # Check 1: job_09 saved
    saved = user.get("savedJobIds", [])
    if "job_09" not in saved:
        errors.append(f"job_09 not in savedJobIds. Current: {saved}")

    # Check 2: emp_12 unfollowed
    followed = user.get("followedEmployerIds", [])
    if "emp_12" in followed:
        errors.append("emp_12 (Tesla) still in followedEmployerIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Stripe job saved (SF). Tesla unfollowed (Austin)."
    )
