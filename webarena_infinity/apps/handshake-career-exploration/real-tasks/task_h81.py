"""
Task: Your most recent unread message says you're a top-15% match. Read it, save all
that employer's active jobs you haven't saved, RSVP to their tech talk, and bookmark
their feed post.

Discovery: msg_01 from Google (most recent unread, top-match). Google active jobs:
job_01, job_02, job_22. Google tech talk: evt_04. Google post: post_01.

Verify:
(1) msg_01.isRead == True
(2) job_01, job_02, job_22 all in savedJobIds
(3) evt_04.rsvped == True
(4) post_01.bookmarked == True AND post_01 in savedPostIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: msg_01 read
    messages = state.get("messages", [])
    msg_01 = next((m for m in messages if m.get("id") == "msg_01"), None)
    if msg_01 is None:
        errors.append("Message msg_01 (Google top-match) not found.")
    elif msg_01.get("isRead") != True:
        errors.append(
            f"msg_01 (Google) not read. isRead={msg_01.get('isRead')}"
        )

    # Check 2: All Google active jobs saved
    saved = state.get("currentUser", {}).get("savedJobIds", [])
    required_jobs = {
        "job_01": "Google SWE Intern",
        "job_02": "Google APM Intern",
        "job_22": "Google UX Design Intern",
    }
    for job_id, title in required_jobs.items():
        if job_id not in saved:
            errors.append(
                f"{job_id} ({title}) not saved. Current savedJobIds: {saved}"
            )

    # Check 3: Google tech talk RSVP'd
    events = state.get("events", [])
    evt_04 = next((e for e in events if e.get("id") == "evt_04"), None)
    if evt_04 is None:
        errors.append("Event evt_04 (Google Tech Talk) not found.")
    elif evt_04.get("rsvped") != True:
        errors.append(
            f"evt_04 (Google Tech Talk) not RSVP'd. rsvped={evt_04.get('rsvped')}"
        )

    # Check 4: Google feed post bookmarked and in savedPostIds
    posts = state.get("feedPosts", [])
    post_01 = next((p for p in posts if p.get("id") == "post_01"), None)
    if post_01 is None:
        errors.append("Post post_01 (Google) not found.")
    elif post_01.get("bookmarked") != True:
        errors.append(
            f"post_01 (Google) not bookmarked. bookmarked={post_01.get('bookmarked')}"
        )

    saved_posts = state.get("currentUser", {}).get("savedPostIds", [])
    if "post_01" not in saved_posts:
        errors.append(
            f"post_01 not in savedPostIds. Current savedPostIds: {saved_posts}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Google identified from top-15% match message (msg_01). Message read, "
        "all active jobs saved (job_01, job_02, job_22), tech talk (evt_04) "
        "RSVP'd, and feed post (post_01) bookmarked and saved."
    )
