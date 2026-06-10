"""
Task: Add Full-time to job type prefs in career interests, save, then save all
active full-time positions from Technology industry employers.

Verify:
(1) "Full-time" in careerInterests.jobTypes
(2) job_17 (Salesforce SWE New Grad, Technology) in savedJobIds
(3) job_21 (Startup Grind Labs Full-Stack, Technology) in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    ci = current_user.get("careerInterests", {})
    errors = []

    # Check 1: Full-time in jobTypes
    job_types = ci.get("jobTypes", [])
    if "Full-time" not in job_types:
        errors.append(
            f"'Full-time' not in careerInterests.jobTypes. "
            f"Current jobTypes: {job_types}"
        )

    # Check 2: Salesforce SWE New Grad saved
    saved = current_user.get("savedJobIds", [])
    if "job_17" not in saved:
        errors.append(
            f"job_17 (Salesforce SWE New Grad, Technology) not saved. "
            f"Current savedJobIds: {saved}"
        )

    # Check 3: Startup Grind Labs Full-Stack saved
    if "job_21" not in saved:
        errors.append(
            f"job_21 (Startup Grind Labs Full-Stack, Technology) not saved. "
            f"Current savedJobIds: {saved}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Full-time added to job type preferences. Active full-time Technology "
        "industry jobs saved: job_17 (Salesforce) and job_21 (Startup Grind Labs)."
    )
