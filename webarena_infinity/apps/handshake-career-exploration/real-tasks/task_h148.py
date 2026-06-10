"""
Task: Three employers have posted about their hiring or internship programs
in the feed: Google, Meta, and Anthropic. Bookmark the post from whichever
of those three has the most followers on Handshake, and RSVP to that same
employer's upcoming event.

Discovery: Google (45200) > Meta (38900) > Anthropic (15600).
Google's post: post_01. Google's event: evt_04 (Tech Talk).

Verify:
(1) post_01 bookmarked + in savedPostIds
(2) evt_04 rsvped
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
    events = state.get("events", [])

    # Check 1: post_01 bookmarked
    post_01 = next((p for p in posts if p.get("id") == "post_01"), None)
    if post_01 is None:
        errors.append("post_01 not found.")
    elif not post_01.get("bookmarked"):
        errors.append("post_01 not bookmarked.")

    if "post_01" not in user.get("savedPostIds", []):
        errors.append("post_01 not in savedPostIds.")

    # Check 2: evt_04 RSVPed
    evt_04 = next((e for e in events if e.get("id") == "evt_04"), None)
    if evt_04 is None:
        errors.append("evt_04 not found.")
    elif not evt_04.get("rsvped"):
        errors.append("evt_04 not RSVP'd.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Google post bookmarked (most followers among Google/Meta/Anthropic). "
        "Google Tech Talk RSVP'd."
    )
