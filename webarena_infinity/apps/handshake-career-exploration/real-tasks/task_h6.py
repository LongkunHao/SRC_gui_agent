"""
Task: Follow all finance industry employers on Handshake.
Verify: emp_02 (JPMorgan Chase) and emp_06 (Goldman Sachs) are in currentUser.followedEmployerIds.
These are the only employers with industry='Finance'.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    followed = current_user.get("followedEmployerIds", [])

    finance_employers = {
        "emp_02": "JPMorgan Chase",
        "emp_06": "Goldman Sachs",
    }

    missing = []
    for emp_id, emp_name in finance_employers.items():
        if emp_id not in followed:
            missing.append(f"{emp_name} ({emp_id})")

    if missing:
        return False, (
            f"Not all finance employers are followed. Missing: {', '.join(missing)}. "
            f"Currently following: {followed}"
        )

    return True, (
        f"All finance employers are followed: JPMorgan Chase (emp_02), "
        f"Goldman Sachs (emp_06). Currently following: {followed}"
    )
