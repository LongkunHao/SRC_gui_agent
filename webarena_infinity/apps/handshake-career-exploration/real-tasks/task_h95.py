"""
Task: Remove closed job from saved list. Save active jobs from that same employer instead.

Discovery: job_03 (JPMorgan, closed) is in saved list. JPMorgan active jobs: job_27.

Verify:
(1) job_03 NOT in savedJobIds
(2) job_27 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    # Check 1: job_03 (JPMorgan, closed) NOT in savedJobIds
    if "job_03" in saved_job_ids:
        errors.append(
            f"job_03 (JPMorgan Investment Banking Summer Analyst, closed) is still in "
            f"savedJobIds. It should have been removed. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Check 2: job_27 (JPMorgan, active) in savedJobIds
    if "job_27" not in saved_job_ids:
        errors.append(
            f"job_27 (JPMorgan Quantitative Research Analyst, active) not in savedJobIds. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Closed job removed (job_03) and active JPMorgan job saved (job_27). "
        f"Current savedJobIds: {saved_job_ids}"
    )
