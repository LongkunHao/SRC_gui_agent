"""
Task: Change profile visibility to 'Limited', update phone to '(650) 555-0300',
add 'Volunteering' to post-graduation plans, save, then create a post for your
school about volunteer opportunities.

Verify:
(1) profileVisibility == 'Limited'
(2) phone == '(650) 555-0300'
(3) 'Volunteering' in careerInterests.postGraduation
(4) New post by Maya Chen with audience='school' mentioning volunteering/volunteer.
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
    if current_user.get("profileVisibility") != "Limited":
        errors.append(
            f"profileVisibility should be 'Limited', "
            f"got '{current_user.get('profileVisibility')}'."
        )

    # Check 2: Phone
    if current_user.get("phone") != "(650) 555-0300":
        errors.append(
            f"phone should be '(650) 555-0300', "
            f"got '{current_user.get('phone')}'."
        )

    # Check 3: Volunteering in post-graduation plans
    if "Volunteering" not in ci.get("postGraduation", []):
        errors.append(
            f"'Volunteering' not in postGraduation. "
            f"Current: {ci.get('postGraduation')}"
        )

    # Check 4: School post about volunteering
    posts = state.get("feedPosts", [])
    volunteer_posts = [
        p for p in posts
        if p.get("authorName") == "Maya Chen"
        and p.get("audience") == "school"
        and "volunteer" in p.get("content", "").lower()
    ]
    if not volunteer_posts:
        errors.append(
            "No school-audience post from Maya Chen mentioning volunteering found."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Profile visibility set to Limited, phone updated, Volunteering added "
        "to post-grad plans, and school post about volunteering created."
    )
