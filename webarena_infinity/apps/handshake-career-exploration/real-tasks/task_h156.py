"""
Task: The highest-paid active internship on Handshake by hourly rate is from
an AI company you already follow. RSVP to that employer's upcoming event.
Then like the feed post from the student who argues you don't need FAANG
for a great tech career.

Discovery: Highest hourly internship → job_12 Anthropic $60/hr (followed).
Anthropic event: evt_06 (AI Alignment Research Talk, virtual).
Anti-FAANG post: post_12 (Jordan Taylor, 412 likes).

Verify:
(1) evt_06 rsvped
(2) post_12 likes > 412
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    events = state.get("events", [])
    posts = state.get("feedPosts", [])

    # Check 1: evt_06 RSVPed
    evt_06 = next((e for e in events if e.get("id") == "evt_06"), None)
    if evt_06 is None:
        errors.append("evt_06 not found.")
    elif not evt_06.get("rsvped"):
        errors.append("evt_06 (Anthropic Research Talk) not RSVP'd.")

    # Check 2: post_12 liked
    post_12 = next((p for p in posts if p.get("id") == "post_12"), None)
    if post_12 is None:
        errors.append("post_12 not found.")
    elif post_12.get("likes", 0) <= 412:
        errors.append(
            f"post_12 likes not incremented. "
            f"Expected > 412, got {post_12.get('likes')}"
        )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Anthropic event RSVP'd (highest-paid internship employer). "
        "Jordan Taylor's anti-FAANG post liked."
    )
