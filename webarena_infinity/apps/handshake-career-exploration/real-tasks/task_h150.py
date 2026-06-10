"""
Task: Add the city where Palantir is headquartered to your preferred locations
in career interests. Then add 'Cybersecurity' to your industries, and save
Palantir's active internship.

Discovery: Palantir (emp_17) HQ: Denver, CO.
Palantir internship: job_19 (Forward Deployed Engineer Intern).

Verify:
(1) 'Denver, CO' in locations
(2) 'Cybersecurity' in industries
(3) job_19 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    ci = user.get("careerInterests", {})

    # Check 1: Denver, CO in locations
    locations = ci.get("locations", [])
    if "Denver, CO" not in locations:
        errors.append(f"'Denver, CO' not in locations. Current: {locations}")

    # Check 2: Cybersecurity in industries
    industries = ci.get("industries", [])
    if "Cybersecurity" not in industries:
        errors.append(
            f"'Cybersecurity' not in industries. Current: {industries}"
        )

    # Check 3: job_19 saved
    saved = user.get("savedJobIds", [])
    if "job_19" not in saved:
        errors.append(f"job_19 not in savedJobIds. Current: {saved}")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Denver, CO added to locations. Cybersecurity added to industries. "
        "Palantir FDE Intern (job_19) saved."
    )
