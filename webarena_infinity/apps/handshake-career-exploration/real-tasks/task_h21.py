"""
Task: One of your unread messages is a top-match recruiting message from an employer
that also hosts a tech talk on Handshake. Save all of that employer's active jobs
and RSVP to their tech talk.

The answer is Google (emp_01). msg_01 is unread top-match recruiting, and Google
hosts evt_04 (Tech Talk).

Verify:
- job_01, job_02, job_22 are all in currentUser.savedJobIds
- evt_04.rsvped == True
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: All active Google jobs are saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    google_active_jobs = {
        "job_01": "Software Engineering Intern, Summer 2026",
        "job_02": "Associate Product Manager Intern",
        "job_22": "UX Design Intern",
    }

    missing_jobs = []
    for job_id, job_title in google_active_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")

    if missing_jobs:
        errors.append(
            f"Not all active Google jobs are saved. "
            f"Missing: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    # Check 2: evt_04 (Google Tech Talk) is RSVP'd
    events = state.get("events", [])
    evt_04 = next((e for e in events if e.get("id") == "evt_04"), None)
    if evt_04 is None:
        errors.append("Event evt_04 (Google Tech Talk) not found in events list.")
    elif evt_04.get("rsvped") != True:
        errors.append(
            f"Event evt_04 (Google Tech Talk) is not RSVP'd. "
            f"rsvped={evt_04.get('rsvped')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All active Google jobs saved (job_01, job_02, job_22) and "
        "Google Tech Talk (evt_04) is RSVP'd."
    )
