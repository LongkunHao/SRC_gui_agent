"""
Task: RSVP to both upcoming Tech Talks, then save all active jobs from
each employer hosting those talks.

Discovery: Tech Talks: evt_04 (Google), evt_06 (Anthropic).
Google active jobs: job_01, job_02, job_22.
Anthropic active jobs: job_12, job_29.

Verify:
(1) evt_04 RSVP'd
(2) evt_06 RSVP'd
(3) job_01, job_02, job_22, job_12, job_29 in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    events = state.get("events", [])
    for evt_id in ["evt_04", "evt_06"]:
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            errors.append(f"{evt_id} not found.")
        elif not evt.get("rsvped"):
            errors.append(f"{evt_id} not RSVP'd.")

    saved = state.get("currentUser", {}).get("savedJobIds", [])
    for jid in ["job_01", "job_02", "job_22", "job_12", "job_29"]:
        if jid not in saved:
            errors.append(f"{jid} not in savedJobIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Both Tech Talks RSVP'd and all active jobs from Google and Anthropic saved."
    )
