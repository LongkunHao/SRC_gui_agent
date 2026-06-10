"""
Task: Read all unread messages and RSVP to the Interview Prep workshop on behavioral questions.
Verify: (1) msg_01 (Google), msg_03 (Meta), msg_06 (Stripe), msg_08 (Apple) all have
isRead==True. (2) evt_09 (Interview Prep: Behavioral Questions Masterclass) has rsvped==True.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check all unread messages are now read
    messages = state.get("messages", [])
    unread_msg_ids = {
        "msg_01": "Google - top match for SWE Intern",
        "msg_03": "Meta - ML Engineer Intern positions",
        "msg_06": "Stripe - Backend Engineer Intern",
        "msg_08": "Apple - Pathways invitation",
    }

    still_unread = []
    for msg_id, msg_desc in unread_msg_ids.items():
        msg = next((m for m in messages if m.get("id") == msg_id), None)
        if msg is None:
            errors.append(f"Message {msg_id} ({msg_desc}) not found in messages list.")
            continue
        if msg.get("isRead") != True:
            still_unread.append(f"{msg_desc} ({msg_id})")

    if still_unread:
        errors.append(
            f"Messages still unread: {', '.join(still_unread)}"
        )

    # Check RSVP to Interview Prep: Behavioral Questions Masterclass (evt_09)
    events = state.get("events", [])
    evt = next((e for e in events if e.get("id") == "evt_09"), None)
    if evt is None:
        errors.append(
            "Event evt_09 (Interview Prep: Behavioral Questions Masterclass) "
            "not found in events list."
        )
    elif evt.get("rsvped") != True:
        errors.append(
            f"Event evt_09 (Interview Prep: Behavioral Questions Masterclass) "
            f"is not RSVP'd. rsvped={evt.get('rsvped')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"All unread messages (msg_01, msg_03, msg_06, msg_08) are now read. "
        f"Interview Prep workshop (evt_09) is RSVP'd."
    )
