"""
Task: Stop following Stripe.
Verify: emp_10 is NOT in currentUser.followedEmployerIds AND emp_10 followCount < 18200.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    followed = current_user.get("followedEmployerIds", [])

    if "emp_10" in followed:
        return False, (
            f"Stripe (emp_10) is still in currentUser.followedEmployerIds. "
            f"The user has not unfollowed Stripe."
        )

    employers = state.get("employers", [])
    stripe = next((e for e in employers if e.get("id") == "emp_10"), None)
    if stripe is None:
        return False, "Employer emp_10 (Stripe) not found in employers list."

    follow_count = stripe.get("followCount", 0)
    if follow_count >= 18200:
        return False, (
            f"Stripe (emp_10) followCount is {follow_count}, expected < 18200. "
            f"The unfollow action may not have decremented the count."
        )

    return True, (
        f"Stripe (emp_10) has been unfollowed. followCount={follow_count}."
    )
