"""
Task: Set your profile visibility to 'Employers', remove 'Part-time' from your job type
preferences, add 'Full-time' instead, and add 'Los Angeles, CA' to your preferred locations.
Save your changes.
Verify: (1) profileVisibility == 'Employers'
(2) 'Part-time' NOT in careerInterests.jobTypes
(3) 'Full-time' IN careerInterests.jobTypes
(4) 'Los Angeles, CA' IN careerInterests.locations
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    career = current_user.get("careerInterests", {})
    errors = []

    # Check 1: Profile visibility
    visibility = current_user.get("profileVisibility", "")
    if visibility != "Employers":
        errors.append(
            f"profileVisibility is '{visibility}', expected 'Employers'."
        )

    # Check 2: Part-time NOT in jobTypes
    job_types = career.get("jobTypes", [])
    if "Part-time" in job_types:
        errors.append(
            f"'Part-time' should have been removed from jobTypes but is still present: {job_types}"
        )

    # Check 3: Full-time IN jobTypes
    if "Full-time" not in job_types:
        errors.append(
            f"'Full-time' not found in jobTypes: {job_types}"
        )

    # Check 4: Los Angeles, CA in locations
    locations = career.get("locations", [])
    if "Los Angeles, CA" not in locations:
        errors.append(
            f"'Los Angeles, CA' not found in preferred locations: {locations}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Profile visibility set to 'Employers'. 'Part-time' removed and 'Full-time' added "
        f"to jobTypes: {job_types}. 'Los Angeles, CA' in locations: {locations}."
    )
