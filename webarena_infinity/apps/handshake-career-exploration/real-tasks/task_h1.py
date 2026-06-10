"""
Task: Follow all consulting firms on Handshake.
Verify: emp_04 (McKinsey), emp_08 (Deloitte), emp_11 (Bain) are all in currentUser.followedEmployerIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    followed = current_user.get("followedEmployerIds", [])

    consulting_employers = {
        "emp_04": "McKinsey & Company",
        "emp_08": "Deloitte",
        "emp_11": "Bain & Company",
    }

    missing = []
    for emp_id, emp_name in consulting_employers.items():
        if emp_id not in followed:
            missing.append(f"{emp_name} ({emp_id})")

    if missing:
        return False, (
            f"Not all consulting firms are followed. Missing: {', '.join(missing)}. "
            f"Currently following: {followed}"
        )

    return True, (
        f"All consulting firms are followed: McKinsey (emp_04), Deloitte (emp_08), "
        f"Bain & Company (emp_11). Currently following: {followed}"
    )
