import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check that emp_18 (Teach For America) is in currentUser.followedEmployerIds
    current_user = state.get("currentUser", {})
    followed_ids = current_user.get("followedEmployerIds", [])

    if "emp_18" not in followed_ids:
        return False, f"emp_18 (Teach For America) not found in followedEmployerIds: {followed_ids}"

    # Check that emp_18 followCount > 8900
    employers = state.get("employers", [])
    emp_18 = None
    for employer in employers:
        if employer.get("id") == "emp_18":
            emp_18 = employer
            break

    if emp_18 is None:
        return False, "Employer emp_18 (Teach For America) not found in state."

    follow_count = emp_18.get("followCount", 0)
    if follow_count <= 8900:
        return False, f"Employer emp_18 followCount is {follow_count}, expected > 8900."

    return True, f"Successfully followed Teach For America. followCount={follow_count} > 8900."
