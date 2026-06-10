"""
Task: Find the employer with the most active job listings on Handshake, RSVP to their
upcoming event, and bookmark their feed post.

Discovery: Google (emp_01) has 3 active jobs (job_01, job_02, job_22) — the most.
Google hosts evt_04 (Tech Talk) and has post_01 in the feed.

Verify:
(1) evt_04.rsvped == True
(2) post_01.bookmarked == True
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Google Tech Talk RSVP'd
    events = state.get("events", [])
    evt_04 = next((e for e in events if e.get("id") == "evt_04"), None)
    if evt_04 is None:
        errors.append("Event evt_04 (Google Tech Talk) not found.")
    elif evt_04.get("rsvped") != True:
        errors.append(
            f"Event evt_04 (Google Tech Talk) not RSVP'd. rsvped={evt_04.get('rsvped')}"
        )

    # Check 2: Google feed post bookmarked
    feed_posts = state.get("feedPosts", [])
    post_01 = next((p for p in feed_posts if p.get("id") == "post_01"), None)
    if post_01 is None:
        errors.append("Post post_01 (Google) not found in feedPosts.")
    elif post_01.get("bookmarked") != True:
        errors.append(
            f"Post post_01 (Google) not bookmarked. bookmarked={post_01.get('bookmarked')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Google identified as employer with most active listings. "
        "Tech Talk (evt_04) RSVP'd and feed post (post_01) bookmarked."
    )
