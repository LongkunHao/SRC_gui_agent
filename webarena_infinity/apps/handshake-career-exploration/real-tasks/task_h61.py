"""
Task: One of your messages mentions an upcoming campus presentation. RSVP to that
event and schedule a case interview prep appointment with the interview coach for
March 17, 2026 at 3:00 PM, virtually.

Discovery: msg_04 from McKinsey mentions campus presentation -> evt_01 (McKinsey
Campus Presentation - Stanford). Interview coach -> David Kim (staff_04).

Verify:
(1) evt_01.rsvped == True.
(2) New appointment: Interview Preparation / Case Interview Prep, staff_04 (David Kim),
    2026-03-17, 3:00 PM, Virtual on Handshake.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: McKinsey campus presentation RSVP'd
    events = state.get("events", [])
    evt_01 = next((e for e in events if e.get("id") == "evt_01"), None)
    if evt_01 is None:
        errors.append("Event evt_01 (McKinsey Campus Presentation) not found.")
    elif evt_01.get("rsvped") != True:
        errors.append(
            f"Event evt_01 (McKinsey Campus Presentation) not RSVP'd. "
            f"rsvped={evt_01.get('rsvped')}"
        )

    # Check 2: Case interview prep appointment scheduled
    appointments = state.get("appointments", [])
    matching = [
        a for a in appointments
        if a.get("category") == "Interview Preparation"
        and a.get("type") == "Case Interview Prep"
        and a.get("date") == "2026-03-17"
        and a.get("time") == "3:00 PM"
        and a.get("medium") == "Virtual on Handshake"
    ]
    if not matching:
        errors.append(
            "No Case Interview Prep appointment found for March 17, 2026 at 3:00 PM "
            "virtually. Expected category='Interview Preparation', "
            "type='Case Interview Prep', date='2026-03-17', time='3:00 PM', "
            "medium='Virtual on Handshake'."
        )
    else:
        appt = matching[0]
        if appt.get("staffId") != "staff_04" and appt.get("staffName") != "David Kim":
            errors.append(
                f"Appointment counselor should be David Kim (interview coach). "
                f"Got staffName='{appt.get('staffName')}', staffId='{appt.get('staffId')}'."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "McKinsey campus presentation (evt_01) RSVP'd. "
        "Case interview prep appointment scheduled with David Kim for March 17 at 3:00 PM virtually."
    )
