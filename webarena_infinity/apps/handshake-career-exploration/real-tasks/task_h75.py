"""
Task: Cancel your requested technical mock interview and reschedule it with the
same coach for March 25, 2026 at 11:00 AM, virtually.

Seed: appt_02 (Mock Interview - Technical, David Kim/staff_04, requested).
Cancel appt_02, create new appointment with same type/coach on March 25.

March 25: staff_04 available at 11:00 AM.

Verify:
(1) appt_02.status == 'cancelled'.
(2) New appointment: Interview Preparation / Mock Interview - Technical,
    staff_04, 2026-03-25, 11:00 AM, Virtual on Handshake.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    appointments = state.get("appointments", [])

    # Check 1: Original appointment cancelled
    appt_02 = next((a for a in appointments if a.get("id") == "appt_02"), None)
    if appt_02 is None:
        errors.append("Appointment appt_02 not found.")
    elif appt_02.get("status") != "cancelled":
        errors.append(
            f"appt_02 should be cancelled. status='{appt_02.get('status')}'."
        )

    # Check 2: New appointment scheduled
    matching = [
        a for a in appointments
        if a.get("id") != "appt_02"
        and a.get("category") == "Interview Preparation"
        and a.get("type") == "Mock Interview - Technical"
        and a.get("date") == "2026-03-25"
        and a.get("time") == "11:00 AM"
        and a.get("medium") == "Virtual on Handshake"
    ]
    if not matching:
        errors.append(
            "No rescheduled Mock Interview - Technical found for March 25, "
            "2026 at 11:00 AM virtually."
        )
    else:
        appt = matching[0]
        if appt.get("staffId") != "staff_04" and appt.get("staffName") != "David Kim":
            errors.append(
                f"Rescheduled appointment should be with David Kim. "
                f"Got staffName='{appt.get('staffName')}'."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Technical mock interview cancelled (appt_02) and rescheduled with "
        "David Kim for March 25 at 11:00 AM virtually."
    )
