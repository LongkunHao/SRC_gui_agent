"""
Task: Schedule a cover letter review appointment with Sarah Thompson for March 11, 2026
at 1:00 PM virtually, then update your website URL to 'mayachen.design'.
Verify: (1) Appointment with staffName='Sarah Thompson' or staffId='staff_05',
date='2026-03-11', time='1:00 PM', medium='Virtual on Handshake',
category='Resume & Cover Letter', type='Cover Letter Review', status='requested'.
(2) currentUser.websiteUrl == 'mayachen.design'.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Appointment
    appointments = state.get("appointments", [])
    found_appointment = False

    for appt in appointments:
        staff_match = (
            appt.get("staffId") == "staff_05"
            or appt.get("staffName") == "Sarah Thompson"
        )
        date_match = appt.get("date") == "2026-03-11"
        time_match = appt.get("time") == "1:00 PM"
        medium_match = appt.get("medium") == "Virtual on Handshake"

        if staff_match and date_match and time_match and medium_match:
            if appt.get("status") != "requested":
                errors.append(
                    f"Found matching appointment but status is "
                    f"'{appt.get('status')}', expected 'requested'."
                )
            if appt.get("category") != "Resume & Cover Letter":
                errors.append(
                    f"Found matching appointment but category is "
                    f"'{appt.get('category')}', expected 'Resume & Cover Letter'."
                )
            if appt.get("type") != "Cover Letter Review":
                errors.append(
                    f"Found matching appointment but type is "
                    f"'{appt.get('type')}', expected 'Cover Letter Review'."
                )
            found_appointment = True
            break

    if not found_appointment and not errors:
        errors.append(
            f"No appointment found with Sarah Thompson (staff_05) on 2026-03-11 "
            f"at 1:00 PM via Virtual on Handshake. "
            f"Current appointments: {[{k: a.get(k) for k in ['staffName', 'date', 'time', 'medium', 'status']} for a in appointments]}"
        )

    # Check 2: Website URL
    website_url = state.get("currentUser", {}).get("websiteUrl", "")
    if website_url != "mayachen.design":
        errors.append(
            f"websiteUrl is '{website_url}', expected 'mayachen.design'."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Cover letter review appointment with Sarah Thompson scheduled for "
        "2026-03-11 at 1:00 PM virtually. Website URL updated to 'mayachen.design'."
    )
