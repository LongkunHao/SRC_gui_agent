"""
Task: One of your messages mentions a phone screen invitation. Find that employer,
then RSVP to their upcoming event and save any of their active jobs you haven't saved yet.

Discovery: msg_02 from Anthropic (emp_15) mentions "Phone Screen Invite".
Anthropic event: evt_06 (AI Alignment Research Talk).
Anthropic active jobs: job_12 (already saved in seed), job_29 (not saved).

Verify:
(1) evt_06.rsvped == True.
(2) job_29 in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Anthropic event RSVP'd
    events = state.get("events", [])
    evt_06 = next((e for e in events if e.get("id") == "evt_06"), None)
    if evt_06 is None:
        errors.append("Event evt_06 (Anthropic Research Talk) not found.")
    elif evt_06.get("rsvped") != True:
        errors.append(
            f"Event evt_06 (Anthropic Research Talk) not RSVP'd. "
            f"rsvped={evt_06.get('rsvped')}"
        )

    # Check 2: Anthropic's unsaved active job is now saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    if "job_29" not in saved_job_ids:
        errors.append(
            f"job_29 (Anthropic Policy Research Intern) not in savedJobIds. "
            f"Current: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Anthropic identified from phone screen message (msg_02). "
        "Event (evt_06) RSVP'd and unsaved job (job_29) saved."
    )
