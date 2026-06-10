"""
Task: Set your profile visibility to 'Private', add 'Military' to your post-graduation
plans in career interests, remove 'Remote' from your preferred locations, and save.

Seed: profileVisibility='Community', postGraduation=['Working', 'Grad school'],
      locations=['San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX', 'Remote'].

Verify:
(1) profileVisibility == 'Private'.
(2) 'Military' in postGraduation.
(3) 'Remote' NOT in locations.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    current_user = state.get("currentUser", {})
    ci = current_user.get("careerInterests", {})
    errors = []

    # Check 1: Profile visibility
    visibility = current_user.get("profileVisibility", "")
    if visibility != "Private":
        errors.append(
            f"profileVisibility='{visibility}', expected 'Private'."
        )

    # Check 2: Military in post-graduation plans
    post_grad = ci.get("postGraduation", [])
    if "Military" not in post_grad:
        errors.append(f"'Military' not in postGraduation. Current: {post_grad}")

    # Check 3: Remote removed from locations
    locations = ci.get("locations", [])
    if "Remote" in locations:
        errors.append(f"'Remote' still in locations. Current: {locations}")

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Profile visibility set to Private, Military added to postGraduation, "
        "and Remote removed from locations."
    )
