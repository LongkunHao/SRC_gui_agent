"""
Task: Schedule a graduate school advising appointment with Maria Rodriguez for
March 18, 2026 at 10:00 AM, virtually, and update your post-graduation plans to
include 'Grad school'. Save your career interests.
Verify: (1) An appointment exists with category='Graduate School',
type='Grad School Advising', staffName='Maria Rodriguez' (or staffId='staff_03'),
date='2026-03-18', time='10:00 AM', medium='Virtual on Handshake', status='requested'.
(2) 'Grad school' in currentUser.careerInterests.postGraduation.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check appointment
    appointments = state.get("appointments", [])
    found_appointment = False

    for appt in appointments:
        staff_match = (
            appt.get("staffId") == "staff_03"
            or appt.get("staffName") == "Maria Rodriguez"
        )
        date_match = appt.get("date") == "2026-03-18"
        time_match = appt.get("time") == "10:00 AM"
        medium_match = appt.get("medium") == "Virtual on Handshake"
        status_match = appt.get("status") == "requested"
        category_match = appt.get("category") == "Graduate School"
        type_match = appt.get("type") == "Grad School Advising"

        if staff_match and date_match and time_match and medium_match:
            if not status_match:
                errors.append(
                    f"Found matching appointment but status is "
                    f"'{appt.get('status')}', expected 'requested'"
                )
            if not category_match:
                errors.append(
                    f"Found matching appointment but category is "
                    f"'{appt.get('category')}', expected 'Graduate School'"
                )
            if not type_match:
                errors.append(
                    f"Found matching appointment but type is "
                    f"'{appt.get('type')}', expected 'Grad School Advising'"
                )
            found_appointment = True
            break

    if not found_appointment and not errors:
        errors.append(
            f"No appointment found with Maria Rodriguez (staff_03) on 2026-03-18 "
            f"at 10:00 AM via Virtual on Handshake. "
            f"Current appointments: {[{k: a.get(k) for k in ['staffName', 'date', 'time', 'medium', 'status']} for a in appointments]}"
        )

    # Check post-graduation plans
    career = state.get("currentUser", {}).get("careerInterests", {})
    post_grad = career.get("postGraduation", [])
    if "Grad school" not in post_grad:
        errors.append(
            f"'Grad school' not in postGraduation: {post_grad}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        f"Graduate school advising appointment with Maria Rodriguez scheduled for "
        f"2026-03-18 at 10:00 AM virtually. 'Grad school' is in postGraduation."
    )
