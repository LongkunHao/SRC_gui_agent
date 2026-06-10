"""
Task: Review your saved jobs and unsave any whose employer is headquartered
outside California.

Seed savedJobIds: job_03, job_07, job_12, job_18, job_24.
- job_03 -> emp_02 JPMorgan (New York, NY) -> UNSAVE
- job_07 -> emp_07 Meta (Menlo Park, CA) -> KEEP
- job_12 -> emp_15 Anthropic (San Francisco, CA) -> KEEP
- job_18 -> emp_16 Nike (Beaverton, OR) -> UNSAVE
- job_24 -> emp_09 Amazon (Seattle, WA) -> UNSAVE

Verify: savedJobIds contains job_07 and job_12 only. Does NOT contain
job_03, job_18, job_24.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    errors = []

    # Should be removed (employer HQ outside California)
    should_remove = {
        "job_03": "JPMorgan (New York, NY)",
        "job_18": "Nike (Beaverton, OR)",
        "job_24": "Amazon (Seattle, WA)",
    }
    for job_id, desc in should_remove.items():
        if job_id in saved_job_ids:
            errors.append(f"{job_id} ({desc}) should be unsaved but is still in savedJobIds.")

    # Should be kept (employer HQ in California)
    should_keep = {
        "job_07": "Meta (Menlo Park, CA)",
        "job_12": "Anthropic (San Francisco, CA)",
    }
    for job_id, desc in should_keep.items():
        if job_id not in saved_job_ids:
            errors.append(f"{job_id} ({desc}) should remain saved but was removed.")

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Non-California employer jobs unsaved (job_03, job_18, job_24). "
        "California employer jobs retained (job_07, job_12)."
    )
