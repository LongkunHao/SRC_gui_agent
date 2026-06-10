import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    # Check that emp_17 (Palantir Technologies) is in currentUser.followedEmployerIds
    current_user = state.get("currentUser", {})
    followed_ids = current_user.get("followedEmployerIds", [])

    if "emp_17" not in followed_ids:
        return False, f"emp_17 (Palantir) not found in followedEmployerIds: {followed_ids}"

    # Check that emp_17 followCount > 14300
    employers = state.get("employers", [])
    emp_17 = None
    for employer in employers:
        if employer.get("id") == "emp_17":
            emp_17 = employer
            break

    if emp_17 is None:
        return False, "Employer emp_17 (Palantir Technologies) not found in state."

    follow_count = emp_17.get("followCount", 0)
    if follow_count <= 14300:
        return False, f"Employer emp_17 followCount is {follow_count}, expected > 14300."

    return True, f"Successfully followed Palantir Technologies. followCount={follow_count} > 14300."
