"""
Task: Pivot your career interests toward consulting: change your career community to
'Business & Finance', add 'Consultant' and 'Business Analyst' to your preferred roles,
add 'Consulting' to your industries, and add 'Sales' to your job functions. Save your changes.
Verify: careerCommunity=='Business & Finance', 'Consultant' in roles,
'Business Analyst' in roles, 'Consulting' in industries, 'Sales' in jobFunctions.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    career = state.get("currentUser", {}).get("careerInterests", {})

    errors = []

    # Check career community
    community = career.get("careerCommunity", "")
    if community != "Business & Finance":
        errors.append(
            f"careerCommunity is '{community}', expected 'Business & Finance'"
        )

    # Check roles
    roles = career.get("roles", [])
    if "Consultant" not in roles:
        errors.append(f"'Consultant' not found in roles: {roles}")
    if "Business Analyst" not in roles:
        errors.append(f"'Business Analyst' not found in roles: {roles}")

    # Check industries
    industries = career.get("industries", [])
    if "Consulting" not in industries:
        errors.append(f"'Consulting' not found in industries: {industries}")

    # Check job functions
    job_functions = career.get("jobFunctions", [])
    if "Sales" not in job_functions:
        errors.append(f"'Sales' not found in jobFunctions: {job_functions}")

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Career interests updated correctly: careerCommunity='{community}', "
        f"roles={roles}, industries={industries}, jobFunctions={job_functions}"
    )
