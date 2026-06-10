"""
Task: Read all your unread top-match messages, then save all active jobs from those
employers that you haven't already saved.

Unread top-match messages: msg_01 (Google), msg_03 (Meta), msg_08 (Apple).
Google active jobs: job_01, job_02, job_22 (none saved in seed).
Meta active jobs: job_07 (already saved), job_26 (not saved).
Apple active jobs: job_06, job_25 (none saved).

Verify:
(1) msg_01, msg_03, msg_08 all isRead==True.
(2) job_01, job_02, job_22, job_06, job_25, job_26 all in savedJobIds.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: All unread top-match messages are now read
    messages = state.get("messages", [])
    top_match_msgs = {
        "msg_01": "Google - SWE Intern top match",
        "msg_03": "Meta - ML Engineer Intern",
        "msg_08": "Apple - Pathways invitation",
    }
    still_unread = []
    for msg_id, msg_desc in top_match_msgs.items():
        msg = next((m for m in messages if m.get("id") == msg_id), None)
        if msg is None:
            errors.append(f"Message {msg_id} ({msg_desc}) not found.")
            continue
        if msg.get("isRead") != True:
            still_unread.append(f"{msg_desc} ({msg_id})")
    if still_unread:
        errors.append(f"Top-match messages still unread: {', '.join(still_unread)}")

    # Check 2: All active jobs from those employers are saved
    saved_job_ids = state.get("currentUser", {}).get("savedJobIds", [])
    required_jobs = {
        "job_01": "Google SWE Intern",
        "job_02": "Google APM Intern",
        "job_22": "Google UX Design Intern",
        "job_06": "Apple Hardware Engineering Intern",
        "job_25": "Apple ML/AI Intern",
        "job_26": "Meta Product Design Intern",
    }
    missing_jobs = []
    for job_id, job_title in required_jobs.items():
        if job_id not in saved_job_ids:
            missing_jobs.append(f"{job_title} ({job_id})")
    if missing_jobs:
        errors.append(
            f"Active jobs not saved: {', '.join(missing_jobs)}. "
            f"Current savedJobIds: {saved_job_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All unread top-match messages read (msg_01, msg_03, msg_08) and "
        "all active jobs from those employers saved "
        "(job_01, job_02, job_22, job_06, job_25, job_26)."
    )
