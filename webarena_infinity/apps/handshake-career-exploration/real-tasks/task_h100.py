"""
Task: Cancel both requested appointments. Schedule behavioral mock with
interview coach March 21 3PM in person. Update phone. School post about interviews.

Discovery: Requested appointments: appt_02 (Mock Interview - Technical with David Kim)
and appt_08 (Case Interview Prep with James Chen). Interview coach = David Kim (staff_04).
March 21 at 3 PM with staff_04 available.

Verify:
(1) appt_02.status == "cancelled"
(2) appt_08.status == "cancelled"
(3) New appointment: type="Mock Interview - Behavioral", staffId="staff_04" OR
    staffName contains "David Kim", date="2026-03-21", time="3:00 PM", medium="In Person"
(4) currentUser.phone == "(650) 555-0250"
(5) New feed post with audience="school" containing keyword "interview" (case-insensitive)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    appointments = state.get("appointments", [])

    # Check 1: appt_02.status == "cancelled"
    appt_02 = None
    for appt in appointments:
        if appt.get("id") == "appt_02":
            appt_02 = appt
            break
    if appt_02 is None:
        errors.append("appt_02 not found in appointments")
    else:
        if appt_02.get("status") != "cancelled":
            errors.append(f"appt_02.status is '{appt_02.get('status')}', expected 'cancelled'")

    # Check 2: appt_08.status == "cancelled"
    appt_08 = None
    for appt in appointments:
        if appt.get("id") == "appt_08":
            appt_08 = appt
            break
    if appt_08 is None:
        errors.append("appt_08 not found in appointments")
    else:
        if appt_08.get("status") != "cancelled":
            errors.append(f"appt_08.status is '{appt_08.get('status')}', expected 'cancelled'")

    # Check 3: New appointment with specific attributes
    found_new_appt = False
    for appt in appointments:
        if appt.get("id") in ("appt_02", "appt_08"):
            continue
        appt_type = appt.get("type", "")
        staff_id = appt.get("staffId", "")
        staff_name = appt.get("staffName", "")
        appt_date = appt.get("date", "")
        appt_time = appt.get("time", "")
        appt_medium = appt.get("medium", "")

        type_match = "Behavioral" in appt_type or "behavioral" in appt_type
        staff_match = staff_id == "staff_04" or "David Kim" in staff_name
        date_match = "2026-03-21" in appt_date or "03/21/2026" in appt_date or "March 21" in appt_date
        time_match = "3:00 PM" in appt_time or "15:00" in appt_time or "3:00 pm" in appt_time.lower()
        medium_match = appt_medium.lower().replace("-", " ") == "in person" or "in person" in appt_medium.lower()

        if type_match and staff_match and date_match and time_match and medium_match:
            found_new_appt = True
            break

    if not found_new_appt:
        errors.append(
            "No new appointment found matching: type='Mock Interview - Behavioral', "
            "staff=David Kim/staff_04, date=2026-03-21, time=3:00 PM, medium=In Person"
        )

    # Check 4: currentUser.phone == "(650) 555-0250"
    current_user = state.get("currentUser", {})
    phone = current_user.get("phone", "")
    if phone != "(650) 555-0250":
        errors.append(f"currentUser.phone is '{phone}', expected '(650) 555-0250'")

    # Check 5: New feed post with audience="school" containing "interview"
    feed_posts = state.get("feedPosts", [])
    found_school_post = False
    for post in feed_posts:
        author = post.get("authorName", "")
        audience = post.get("audience", "")
        content = post.get("content", "").lower()
        title = post.get("title", "").lower()

        if "Maya" in author and audience == "school":
            if "interview" in content or "interview" in title:
                found_school_post = True
                break

    if not found_school_post:
        errors.append("No feed post from Maya Chen with audience='school' containing 'interview' found")

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All checks passed: appt_02 and appt_08 cancelled, new behavioral mock interview scheduled, "
        "phone updated, school post about interviews created."
    )
