"""
Task: Find the active job with the most applicants on Handshake.
Follow its employer, RSVP to their upcoming event, and bookmark their feed post.

Discovery: Most applicants active job: job_05 (McKinsey BA Intern, 3890).
Employer: emp_04 (McKinsey). Event: evt_01. Post: post_09.

Verify:
(1) emp_04 in followedEmployerIds
(2) evt_01 RSVP'd
(3) post_09 bookmarked
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    followed = state.get("currentUser", {}).get("followedEmployerIds", [])
    if "emp_04" not in followed:
        errors.append(f"emp_04 (McKinsey) not followed. Current: {followed}")

    events = state.get("events", [])
    evt_01 = next((e for e in events if e.get("id") == "evt_01"), None)
    if evt_01 is None:
        errors.append("evt_01 not found.")
    elif not evt_01.get("rsvped"):
        errors.append(f"evt_01 not RSVP'd. rsvped={evt_01.get('rsvped')}")

    posts = state.get("feedPosts", [])
    post_09 = next((p for p in posts if p.get("id") == "post_09"), None)
    if post_09 is None:
        errors.append("post_09 not found.")
    elif not post_09.get("bookmarked"):
        errors.append(f"post_09 not bookmarked.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "McKinsey identified (most applicants: job_05). "
        "Followed, event RSVP'd, post bookmarked."
    )
