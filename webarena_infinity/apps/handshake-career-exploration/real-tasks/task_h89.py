"""
Task: Read all unread top-match messages. Two senders host upcoming events (one virtual
info session, one tech talk). RSVP both, save unsaved active jobs from both.

Discovery: Unread top-match: msg_01 (Google), msg_03 (Meta), msg_08 (Apple).
Google hosts evt_04 (Tech Talk). Meta hosts evt_02 (Virtual Info Session).
Apple has no upcoming event.
Google unsaved active jobs: job_01, job_02, job_22. Meta unsaved: job_26 (job_07 already saved).

Verify:
(1) msg_01.isRead == True
(2) msg_03.isRead == True
(3) msg_08.isRead == True
(4) evt_02.rsvped == True
(5) evt_04.rsvped == True
(6) job_01, job_02, job_22, job_26 all in savedJobIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1-3: All unread top-match messages are now read
    messages = state.get("messages", [])

    unread_msgs = {
        "msg_01": "Google - SWE Intern top match",
        "msg_03": "Meta - ML Engineer Intern positions",
        "msg_08": "Apple - Pathways invitation",
    }

    for msg_id, msg_desc in unread_msgs.items():
        msg = next((m for m in messages if m.get("id") == msg_id), None)
        if msg is None:
            errors.append(f"Message {msg_id} ({msg_desc}) not found in messages.")
        elif msg.get("isRead") is not True:
            errors.append(
                f"Message {msg_id} ({msg_desc}) is still unread. "
                f"isRead={msg.get('isRead')}"
            )

    # Check 4-5: RSVP to both events
    events = state.get("events", [])

    required_rsvps = {
        "evt_02": "AI/ML Careers at Meta - Virtual Info Session",
        "evt_04": "Google Tech Talk: Future of AI",
    }

    for evt_id, evt_title in required_rsvps.items():
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            errors.append(f"Event {evt_id} ({evt_title}) not found in events.")
        elif evt.get("rsvped") is not True:
            errors.append(
                f"Event {evt_id} ({evt_title}) is not RSVP'd. "
                f"rsvped={evt.get('rsvped')}"
            )

    # Check 6: All unsaved active jobs from Google and Meta are saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])

    required_jobs = {
        "job_01": "Google SWE Intern",
        "job_02": "Google APM Intern",
        "job_22": "Google UX Design Intern",
        "job_26": "Meta ML Engineer Intern",
    }

    missing_jobs = []
    for job_id, job_title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")

    if missing_jobs:
        errors.append(
            f"Jobs not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All unread top-match messages read (msg_01, msg_03, msg_08). "
        "Both events RSVP'd (evt_02 Meta, evt_04 Google). "
        "All unsaved active jobs saved (job_01, job_02, job_22, job_26)."
    )
