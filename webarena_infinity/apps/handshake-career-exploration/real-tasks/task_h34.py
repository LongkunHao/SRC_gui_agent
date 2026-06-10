"""
Task: Review your saved jobs and unsave any whose employer is not in the Technology or
Artificial Intelligence industry.
Verify: Seed savedJobIds: job_03 (JPMorgan/Finance), job_07 (Meta/Technology),
job_12 (Anthropic/Artificial Intelligence), job_18 (Nike/Retail), job_24 (Amazon/Technology).
Should unsave: job_03 (Finance), job_18 (Retail).
Should keep: job_07, job_12, job_24.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    errors = []

    # These should have been unsaved (not Technology or AI industry)
    should_be_unsaved = {
        "job_03": "JPMorgan Chase (Finance)",
        "job_18": "Nike (Retail)",
    }
    for job_id, desc in should_be_unsaved.items():
        if job_id in saved_job_ids:
            errors.append(
                f"{job_id} ({desc}) should have been unsaved but is still in savedJobIds."
            )

    # These should remain saved (Technology or Artificial Intelligence industry)
    should_remain = {
        "job_07": "Meta (Technology)",
        "job_12": "Anthropic (Artificial Intelligence)",
        "job_24": "Amazon (Technology)",
    }
    for job_id, desc in should_remain.items():
        if job_id not in saved_job_ids:
            errors.append(
                f"{job_id} ({desc}) should still be saved but is missing from savedJobIds."
            )

    if errors:
        return False, " | ".join(errors) + f" Current savedJobIds: {saved_job_ids}"

    return True, (
        "Non-tech/AI jobs unsaved (job_03, job_18) and tech/AI jobs retained "
        f"(job_07, job_12, job_24). Current savedJobIds: {saved_job_ids}"
    )
