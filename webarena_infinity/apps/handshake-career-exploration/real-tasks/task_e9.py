"""
Task: Follow Goldman Sachs.
Verify: emp_06 is in currentUser.followedEmployerIds AND emp_06 followCount > 29500.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    followed = current_user.get("followedEmployerIds", [])

    if "emp_06" not in followed:
        return False, (
            f"Goldman Sachs (emp_06) is not in currentUser.followedEmployerIds. "
            f"Currently following: {followed}"
        )

    employers = state.get("employers", [])
    gs = next((e for e in employers if e.get("id") == "emp_06"), None)
    if gs is None:
        return False, "Employer emp_06 (Goldman Sachs) not found in employers list."

    follow_count = gs.get("followCount", 0)
    if follow_count <= 29500:
        return False, (
            f"Goldman Sachs (emp_06) followCount is {follow_count}, expected > 29500. "
            f"The follow action may not have incremented the count."
        )

    return True, (
        f"Goldman Sachs (emp_06) is followed. followCount={follow_count}."
    )
