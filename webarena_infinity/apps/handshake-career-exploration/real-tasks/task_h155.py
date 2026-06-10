"""
Task: Change your profile visibility to 'Public'. Update your bio to mention
that you're looking for full-time positions after graduation. Then create a
feed post visible to everyone introducing yourself as open to full-time AI
opportunities.

Verify:
(1) profileVisibility = 'Public'
(2) bio contains 'full-time' (case-insensitive)
(3) New post from user with audience 'everyone' mentioning 'full-time' or 'AI'
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    posts = state.get("feedPosts", [])

    # Check 1: profile visibility
    vis = user.get("profileVisibility", "")
    if vis != "Public":
        errors.append(
            f"profileVisibility is '{vis}', expected 'Public'."
        )

    # Check 2: bio mentions full-time
    bio = user.get("bio", "")
    if "full-time" not in bio.lower() and "full time" not in bio.lower():
        errors.append(
            "Bio does not mention 'full-time'. "
            f"Current bio: '{bio[:100]}...'"
        )

    # Check 3: new post about full-time / AI
    user_id = user.get("id", "")
    found_post = any(
        p.get("authorId") == user_id
        and p.get("audience") == "everyone"
        and (
            "full-time" in p.get("content", "").lower()
            or "full time" in p.get("content", "").lower()
            or "ai" in p.get("content", "").lower()
        )
        for p in posts
    )
    if not found_post:
        errors.append(
            "No new post from user with audience 'everyone' "
            "mentioning full-time or AI."
        )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Profile visibility set to Public. Bio updated with full-time mention. "
        "New post about full-time AI opportunities created."
    )
