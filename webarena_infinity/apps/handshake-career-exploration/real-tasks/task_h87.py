"""
Task: Focus East Coast. Remove all locations except New York NY. Unfollow all CA employers.
Save career interests.

Discovery: CA employers currently followed: emp_01 (Google, Mountain View CA),
emp_05 (Apple, Cupertino CA), emp_07 (Meta, Menlo Park CA), emp_10 (Stripe, SF CA),
emp_15 (Anthropic, SF CA).

Verify:
(1) careerInterests.locations == ['New York, NY'] (only NY remains)
(2) emp_01 NOT in followedEmployerIds
(3) emp_05 NOT in followedEmployerIds
(4) emp_07 NOT in followedEmployerIds
(5) emp_10 NOT in followedEmployerIds
(6) emp_15 NOT in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    current_user = state.get("currentUser", {})
    career_interests = current_user.get("careerInterests", {})

    # Check 1: locations should be exactly ['New York, NY']
    locations = career_interests.get("locations", [])
    if locations != ["New York, NY"]:
        errors.append(
            f"careerInterests.locations is {locations}, expected ['New York, NY']"
        )

    # Check 2-6: CA employers must NOT be in followedEmployerIds
    followed = current_user.get("followedEmployerIds", [])

    ca_employers = {
        "emp_01": "Google (Mountain View, CA)",
        "emp_05": "Apple (Cupertino, CA)",
        "emp_07": "Meta (Menlo Park, CA)",
        "emp_10": "Stripe (San Francisco, CA)",
        "emp_15": "Anthropic (San Francisco, CA)",
    }

    still_followed = []
    for emp_id, emp_desc in ca_employers.items():
        if emp_id in followed:
            still_followed.append(f"{emp_desc} ({emp_id})")

    if still_followed:
        errors.append(
            f"CA employers still followed: {', '.join(still_followed)}. "
            f"Current followedEmployerIds: {followed}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Locations correctly set to {locations}. "
        f"All CA employers unfollowed (emp_01, emp_05, emp_07, emp_10, emp_15). "
        f"Current followedEmployerIds: {followed}"
    )
