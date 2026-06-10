"""
Task: RSVP to all upcoming events that are hosted by employers you currently follow.

Seed followed: emp_01, emp_03, emp_05, emp_07, emp_10, emp_12, emp_15.
Events from these (upcoming only):
- evt_02 (emp_07 - Meta)
- evt_04 (emp_01 - Google)
- evt_06 (emp_15 - Anthropic)
evt_12 (emp_05) is past, so skip.

Verify: evt_02.rsvped==True, evt_04.rsvped==True, evt_06.rsvped==True
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    events = state.get("events", [])

    required_events = {
        "evt_02": "AI/ML Careers at Meta - Virtual Info Session",
        "evt_04": "Google Tech Talk",
        "evt_06": "Anthropic Research Talk: AI Alignment",
    }

    not_rsvped = []
    missing = []

    for evt_id, evt_title in required_events.items():
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            missing.append(f"{evt_title} ({evt_id})")
            continue
        if evt.get("rsvped") != True:
            not_rsvped.append(f"{evt_title} ({evt_id})")

    if missing:
        return False, f"Events not found: {', '.join(missing)}"

    if not_rsvped:
        return False, (
            f"Not all upcoming events from followed employers are RSVP'd. "
            f"Not RSVP'd: {', '.join(not_rsvped)}"
        )

    return True, (
        "All upcoming events from followed employers are RSVP'd: "
        "evt_02 (Meta), evt_04 (Google), evt_06 (Anthropic)."
    )
