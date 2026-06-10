"""
Task: Save all active full-time positions from Finance industry employers
and follow those employers if you aren't already.

Discovery: Finance employers: JPMorgan (emp_02), Goldman Sachs (emp_06).
Active FT: job_27 (JPMorgan), job_28 (Goldman).

Verify:
(1) job_27 in savedJobIds
(2) job_28 in savedJobIds
(3) emp_02 in followedEmployerIds
(4) emp_06 in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})

    saved = user.get("savedJobIds", [])
    for jid in ["job_27", "job_28"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds.")

    followed = user.get("followedEmployerIds", [])
    for eid in ["emp_02", "emp_06"]:
        if eid not in followed:
            errors.append(f"{eid} not in followedEmployerIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Finance employers (JPMorgan, Goldman) followed. "
        "Active FT jobs (job_27, job_28) saved."
    )
