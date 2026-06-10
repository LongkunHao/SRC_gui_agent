"""
Task: Schedule a Networking Strategy appointment with Sarah Thompson for the
earliest date after March 17 when she's available. Choose the first available
time slot. Make it by phone.

Discovery: Sarah Thompson = staff_05.
Available dates with staff_05 after March 17:
  Mar 18 (10AM, 11AM, 2PM), Mar 21, Mar 26, Mar 28.
Earliest: March 18. First time: 10:00 AM.
Category: Networking & Professional Development.

Verify:
(1) New appointment with type 'Networking Strategy'
(2) Date '2026-03-18', time '10:00 AM'
(3) Medium 'Phone'
(4) Staff is Sarah Thompson / staff_05
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    appointments = state.get("appointments", [])
    seed_ids = {
        "appt_01", "appt_02", "appt_03", "appt_04",
        "appt_05", "appt_06", "appt_07", "appt_08",
    }
    new_appts = [a for a in appointments if a.get("id") not in seed_ids]

    match = None
    for a in new_appts:
        atype = a.get("type", "")
        if "Networking Strategy" in atype or "networking strategy" in atype.lower():
            match = a
            break

    if match is None:
        errors.append("No new Networking Strategy appointment found.")
    else:
        if match.get("date") != "2026-03-18":
            errors.append(
                f"Appointment date is '{match.get('date')}', "
                "expected '2026-03-18'."
            )
        if match.get("time") != "10:00 AM":
            errors.append(
                f"Appointment time is '{match.get('time')}', "
                "expected '10:00 AM'."
            )
        if "phone" not in match.get("medium", "").lower():
            errors.append(
                f"Appointment medium is '{match.get('medium')}', "
                "expected 'Phone'."
            )
        staff_name = match.get("staffName", "")
        staff_id = match.get("staffId", "")
        if "Sarah Thompson" not in staff_name and staff_id != "staff_05":
            errors.append(
                f"Staff is '{staff_name}' ({staff_id}), "
                "expected Sarah Thompson / staff_05."
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Networking Strategy appointment scheduled with Sarah Thompson "
        "on March 18 at 10:00 AM by phone."
    )
