"""
Task: Save all active internships paying at least $50/hr from employers
you don't currently follow.

Discovery: Followed employers (seed): emp_01, emp_03, emp_05, emp_07, emp_10, emp_12, emp_15.
Active internships >= $50/hr from unfollowed:
  job_08 ($51/hr, emp_09 Amazon)
  job_19 ($55/hr, emp_17 Palantir)
  job_24 ($53/hr, emp_09 Amazon) — already saved in seed

Verify:
(1) job_08 in savedJobIds
(2) job_19 in savedJobIds
(3) job_24 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    errors = []

    for jid in ["job_08", "job_19", "job_24"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds.")

    if errors:
        return False, " | ".join(errors) + f" Current savedJobIds: {saved}"
    return True, (
        "All active internships >= $50/hr from unfollowed employers saved: "
        "job_08, job_19, job_24."
    )
