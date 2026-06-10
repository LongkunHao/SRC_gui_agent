"""
Task: Refocus your career entirely on finance.

Verify:
- careerCommunity == "Business & Finance"
- roles == exactly ["Financial Analyst", "Business Analyst", "Consultant"]
  (order may vary, but only these 3)
- industries == exactly ["Finance", "Consulting"] (order may vary, but only these 2)
- "Engineering" NOT in jobFunctions, "Finance & Accounting" IN jobFunctions
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    career = state.get("currentUser", {}).get("careerInterests", {})
    errors = []

    # Check 1: careerCommunity == "Business & Finance"
    community = career.get("careerCommunity", "")
    if community != "Business & Finance":
        errors.append(
            f"careerCommunity is '{community}', expected 'Business & Finance'."
        )

    # Check 2: roles == exactly {"Financial Analyst", "Business Analyst", "Consultant"}
    roles = career.get("roles", [])
    expected_roles = {"Financial Analyst", "Business Analyst", "Consultant"}
    current_roles_set = set(roles)

    missing_roles = expected_roles - current_roles_set
    extra_roles = current_roles_set - expected_roles

    if missing_roles:
        errors.append(
            f"Missing required roles: {missing_roles}. Current roles: {roles}"
        )
    if extra_roles:
        errors.append(
            f"Unexpected extra roles found: {extra_roles}. "
            f"Expected exactly: {expected_roles}. Current roles: {roles}"
        )

    # Check 3: industries == exactly {"Finance", "Consulting"}
    industries = career.get("industries", [])
    expected_industries = {"Finance", "Consulting"}
    current_industries_set = set(industries)

    missing_industries = expected_industries - current_industries_set
    extra_industries = current_industries_set - expected_industries

    if missing_industries:
        errors.append(
            f"Missing required industries: {missing_industries}. "
            f"Current industries: {industries}"
        )
    if extra_industries:
        errors.append(
            f"Unexpected extra industries found: {extra_industries}. "
            f"Expected exactly: {expected_industries}. Current industries: {industries}"
        )

    # Check 4: jobFunctions - "Engineering" NOT in, "Finance & Accounting" IN
    job_functions = career.get("jobFunctions", [])

    if "Engineering" in job_functions:
        errors.append(
            f"'Engineering' is still in jobFunctions but should have been removed. "
            f"Current jobFunctions: {job_functions}"
        )

    if "Finance & Accounting" not in job_functions:
        errors.append(
            f"'Finance & Accounting' not found in jobFunctions. "
            f"Current jobFunctions: {job_functions}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Career refocused on finance: careerCommunity='Business & Finance', "
        f"roles={roles}, industries={industries}, "
        f"'Finance & Accounting' in jobFunctions, 'Engineering' removed."
    )
