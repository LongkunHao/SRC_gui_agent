"""
Task: Sign up for the JPMorgan Markets & Trading Panel.
Verify: evt_08 has rsvped == True and rsvpCount > 92.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    events = state.get("events", [])

    evt = next((e for e in events if e.get("id") == "evt_08"), None)
    if evt is None:
        return False, "Event evt_08 (JPMorgan Markets & Trading Panel) not found in events list."

    if evt.get("rsvped") != True:
        return False, (
            f"Event evt_08 (JPMorgan Markets & Trading Panel) is not RSVP'd. "
            f"rsvped={evt.get('rsvped')}"
        )

    rsvp_count = evt.get("rsvpCount", 0)
    if rsvp_count <= 92:
        return False, (
            f"Event evt_08 rsvpCount is {rsvp_count}, expected > 92. "
            f"The RSVP action may not have incremented the count."
        )

    return True, (
        f"JPMorgan Markets & Trading Panel (evt_08) is RSVP'd. rsvpCount={rsvp_count}."
    )
