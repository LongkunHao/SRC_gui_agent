"""
Task: Research Meta across the platform: save all their active jobs you haven't saved,
RSVP to their upcoming virtual info session, and like their feed post.

Meta (emp_07):
- Active jobs: job_07 (already saved), job_26 (not saved).
- Event: evt_02 (AI/ML Careers Virtual Info Session).
- Feed post: post_03 (256 likes).

Verify:
(1) job_26 in savedJobIds.
(2) evt_02.rsvped == True.
(3) post_03.likes > 256.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Meta's unsaved job is now saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_26" not in saved_job_ids:
        errors.append(
            f"job_26 (Meta Product Design Intern) not in savedJobIds. "
            f"Current: {saved_job_ids}"
        )

    # Check 2: Meta virtual info session RSVP'd
    events = state.get("events", [])
    evt_02 = next((e for e in events if e.get("id") == "evt_02"), None)
    if evt_02 is None:
        errors.append("Event evt_02 (Meta AI/ML Virtual Info Session) not found.")
    elif evt_02.get("rsvped") != True:
        errors.append(
            f"Event evt_02 (Meta Virtual Info Session) not RSVP'd. "
            f"rsvped={evt_02.get('rsvped')}"
        )

    # Check 3: Meta feed post liked
    feed_posts = state.get("feedPosts", [])
    post_03 = next((p for p in feed_posts if p.get("id") == "post_03"), None)
    if post_03 is None:
        errors.append("Post post_03 (Meta) not found in feedPosts.")
    else:
        likes = post_03.get("likes", 0)
        if likes <= 256:
            errors.append(
                f"post_03 (Meta) likes={likes}, expected > 256 (seed=256)."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Meta research complete: job_26 saved, evt_02 RSVP'd, post_03 liked."
    )
