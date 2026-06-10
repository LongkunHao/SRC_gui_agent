"""
Task: RSVP to all upcoming virtual events.
Verify: evt_02 (Meta AI/ML), evt_06 (Anthropic AI Alignment), evt_07 (Virtual Career Fair),
evt_10 (Salesforce Futureforce) all have rsvped == True. These are all events with
isVirtual=true and status='upcoming'.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    events = state.get("events", [])

    virtual_upcoming = {
        "evt_02": "AI/ML Careers at Meta - Virtual Info Session",
        "evt_06": "Anthropic Research Talk: AI Alignment",
        "evt_07": "Virtual Career Fair - Technology Focus",
        "evt_10": "Salesforce Futureforce: Building Your Career in Cloud",
    }

    not_rsvped = []
    missing = []

    for evt_id, evt_title in virtual_upcoming.items():
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            missing.append(f"{evt_title} ({evt_id})")
            continue
        if evt.get("rsvped") != True:
            not_rsvped.append(f"{evt_title} ({evt_id})")

    if missing:
        return False, (
            f"Events not found: {', '.join(missing)}"
        )

    if not_rsvped:
        return False, (
            f"Not all upcoming virtual events are RSVP'd. "
            f"Not RSVP'd: {', '.join(not_rsvped)}"
        )

    return True, (
        f"All upcoming virtual events are RSVP'd: evt_02, evt_06, evt_07, evt_10."
    )
