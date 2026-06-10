"""
Task: Cancel your case interview prep appointment. On the same date it was
scheduled, schedule a Salary Negotiation appointment instead at the earliest
available time, by phone. Then add a comment to your remaining requested
appointment explaining you'd like to focus on system design questions.

Discovery: Case interview prep → appt_08 (Mar 28, James Chen, requested).
Mar 28 available: 9AM, 11AM, 1PM. Staff: staff_03, staff_05.
Remaining requested: appt_02 (Mock Technical, David Kim, Mar 21).
Salary Negotiation category: Networking & Professional Development.

Verify:
(1) appt_08 status = 'cancelled'
(2) New appointment: type 'Salary Negotiation', date '2026-03-28',
    time '9:00 AM', medium 'Phone'
(3) appt_02 has a new comment
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    appointments = state.get("appointments", [])

    # Check 1: appt_08 cancelled
    appt_08 = next(
        (a for a in appointments if a.get("id") == "appt_08"), None
    )
    if appt_08 is None:
        errors.append("appt_08 not found.")
    elif appt_08.get("status") != "cancelled":
        errors.append(
            f"appt_08 status is '{appt_08.get('status')}', "
            "expected 'cancelled'."
        )

    # Check 2: new Salary Negotiation appointment
    seed_ids = {
        "appt_01", "appt_02", "appt_03", "appt_04",
        "appt_05", "appt_06", "appt_07", "appt_08",
    }
    new_appts = [a for a in appointments if a.get("id") not in seed_ids]

    sal_appt = None
    for a in new_appts:
        if "Salary Negotiation" in a.get("type", ""):
            sal_appt = a
            break

    if sal_appt is None:
        errors.append("No new Salary Negotiation appointment found.")
    else:
        if sal_appt.get("date") != "2026-03-28":
            errors.append(
                f"Salary Negotiation date is '{sal_appt.get('date')}', "
                "expected '2026-03-28'."
            )
        if sal_appt.get("time") != "9:00 AM":
            errors.append(
                f"Salary Negotiation time is '{sal_appt.get('time')}', "
                "expected '9:00 AM'."
            )
        if "phone" not in sal_appt.get("medium", "").lower():
            errors.append(
                f"Salary Negotiation medium is '{sal_appt.get('medium')}', "
                "expected 'Phone'."
            )

    # Check 3: appt_02 has new comment
    appt_02 = next(
        (a for a in appointments if a.get("id") == "appt_02"), None
    )
    if appt_02 is None:
        errors.append("appt_02 not found.")
    else:
        comments = appt_02.get("comments", [])
        if len(comments) < 1:
            errors.append("appt_02 has no comments.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Case interview prep cancelled. Salary Negotiation scheduled "
        "for March 28 at 9 AM by phone. Comment added to mock technical appt."
    )
