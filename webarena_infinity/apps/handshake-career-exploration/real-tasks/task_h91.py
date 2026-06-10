"""
Task: Schedule general career advising with Dr. Williams for March 19, 1 PM virtually.
Comment on completed January internship planning appointment about applying broadly.

Discovery: Dr. Patricia Williams = staff_01. appt_04 is completed Jan 15 Internship Planning.
March 19 has staff_01 available, 1:00 PM is available.

Verify:
(1) New appointment: category="Career Counseling", type="General Career Advising",
    staffName contains "Patricia Williams" OR staffId="staff_01", date="2026-03-19",
    time="1:00 PM", medium="Virtual on Handshake"
(2) appt_04 has new comment from Maya Chen (not from staff)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: New appointment with Dr. Patricia Williams
    appointments = state.get("appointments", [])
    found_appointment = False

    for appt in appointments:
        staff_match = (
            appt.get("staffId") == "staff_01"
            or "Patricia Williams" in (appt.get("staffName") or "")
        )
        date_match = appt.get("date") == "2026-03-19"
        time_match = appt.get("time") == "1:00 PM"
        medium_match = appt.get("medium") == "Virtual on Handshake"

        if staff_match and date_match and time_match and medium_match:
            category = appt.get("category", "")
            appt_type = appt.get("type", "")

            if category != "Career Counseling":
                errors.append(
                    f"Found matching appointment but category is "
                    f"'{category}', expected 'Career Counseling'"
                )
            if appt_type != "General Career Advising":
                errors.append(
                    f"Found matching appointment but type is "
                    f"'{appt_type}', expected 'General Career Advising'"
                )
            found_appointment = True
            break

    if not found_appointment and not errors:
        errors.append(
            f"No appointment found with Dr. Patricia Williams (staff_01) on 2026-03-19 "
            f"at 1:00 PM via Virtual on Handshake. "
            f"Current appointments: {[{k: a.get(k) for k in ['staffName', 'date', 'time', 'medium']} for a in appointments]}"
        )

    # Check 2: appt_04 has new comment from Maya Chen
    appt_04 = next((a for a in appointments if a.get("id") == "appt_04"), None)
    if appt_04 is None:
        errors.append("Appointment appt_04 not found in state.")
    else:
        comments = appt_04.get("comments", [])
        # Seed has 1 comment from Dr. Patricia Williams. Look for a new one from Maya Chen.
        maya_comments = [
            c for c in comments
            if "maya" in (c.get("author") or "").lower()
        ]
        if not maya_comments:
            errors.append(
                f"No comment from Maya Chen found on appt_04 (Internship Planning). "
                f"Current comments: {[{'author': c.get('author'), 'text': c.get('text', '')[:80]} for c in comments]}"
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "General Career Advising appointment with Dr. Patricia Williams scheduled for "
        "2026-03-19 at 1:00 PM virtually. Comment from Maya Chen added to appt_04."
    )
