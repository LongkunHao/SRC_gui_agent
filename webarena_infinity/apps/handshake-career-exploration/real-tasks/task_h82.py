"""
Task: Find Resume Writing counselor. Comment on approved appt with them. Schedule
LinkedIn Profile Review with them for March 14 at 9 AM in person.

Discovery: Michael Okafor (staff_06) specializes in Resume Writing. appt_01 is
approved with him.

Verify:
(1) appt_01 has a new comment from Maya Chen mentioning "LinkedIn" (case-insensitive)
(2) A new appointment exists with: category="Resume & Cover Letter",
    type="LinkedIn Profile Review", staffId="staff_06" OR staffName="Michael Okafor",
    date="2026-03-14", time="9:00 AM", medium="In Person"
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    appointments = state.get("appointments", [])

    # Check 1: appt_01 has a new comment from Maya Chen mentioning LinkedIn
    appt_01 = next((a for a in appointments if a.get("id") == "appt_01"), None)
    if appt_01 is None:
        errors.append("Appointment appt_01 not found in state.")
    else:
        comments = appt_01.get("comments", [])
        found_comment = False
        for comment in comments:
            author = comment.get("author", "")
            text = comment.get("text", "").lower()
            if "maya" in author.lower() and "linkedin" in text:
                found_comment = True
                break
        if not found_comment:
            errors.append(
                f"No comment from Maya Chen mentioning 'LinkedIn' on appt_01. "
                f"Current comments: {[{'author': c.get('author'), 'text': c.get('text', '')[:80]} for c in comments]}"
            )

    # Check 2: New LinkedIn Profile Review appointment with Michael Okafor
    matching = [
        a for a in appointments
        if a.get("id") != "appt_01"
        and a.get("category") == "Resume & Cover Letter"
        and a.get("type") == "LinkedIn Profile Review"
        and a.get("date") == "2026-03-14"
        and a.get("time") == "9:00 AM"
        and a.get("medium") == "In Person"
    ]
    if not matching:
        errors.append(
            "No LinkedIn Profile Review appointment found for March 14, 2026 "
            "at 9:00 AM in person under Resume & Cover Letter category."
        )
    else:
        appt = matching[0]
        if appt.get("staffId") != "staff_06" and appt.get("staffName") != "Michael Okafor":
            errors.append(
                f"LinkedIn Profile Review appointment should be with Michael Okafor (staff_06). "
                f"Got staffId='{appt.get('staffId')}', staffName='{appt.get('staffName')}'."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Comment mentioning LinkedIn left on appt_01 (Michael Okafor). "
        "LinkedIn Profile Review scheduled with Michael Okafor for March 14 "
        "at 9:00 AM in person."
    )
