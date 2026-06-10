"""
Task: RSVP to every upcoming Workshop event. Then follow the employer that
hosts the only Panel event on the platform.

Discovery:
  Workshops (upcoming): evt_05 (Resume Workshop, Mar 10),
                         evt_09 (Interview Prep, Mar 8).
  Panel: evt_08 (JPM Markets & Trading Panel) → JPMorgan (emp_02).

Verify:
(1) evt_05 rsvped
(2) evt_09 rsvped
(3) emp_02 in followedEmployerIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    events = state.get("events", [])

    # Check 1-2: workshop events RSVPed
    for evt_id in ["evt_05", "evt_09"]:
        evt = next((e for e in events if e.get("id") == evt_id), None)
        if evt is None:
            errors.append(f"{evt_id} not found.")
        elif not evt.get("rsvped"):
            errors.append(f"{evt_id} not RSVP'd.")

    # Check 3: follow JPMorgan
    followed = user.get("followedEmployerIds", [])
    if "emp_02" not in followed:
        errors.append("emp_02 (JPMorgan Chase) not in followedEmployerIds.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Both workshop events RSVP'd. "
        "JPMorgan Chase followed (hosts the only Panel event)."
    )
