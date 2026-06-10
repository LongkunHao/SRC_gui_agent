"""
Task: Schedule a personal statement review with Maria Rodriguez for March 28, 2026
at 11:00 AM in person, then post a Q&A question asking about the timeline for
grad school applications in computer science.

March 28 availability: staff_03 (Maria Rodriguez) available, times include 11:00 AM.

Verify:
(1) New appointment: Graduate School / Personal Statement Review, staff_03,
    2026-03-28, 11:00 AM, In Person.
(2) New Q&A question about grad school application timelines.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Personal statement review appointment
    appointments = state.get("appointments", [])
    matching = [
        a for a in appointments
        if a.get("category") == "Graduate School"
        and a.get("type") == "Personal Statement Review"
        and a.get("date") == "2026-03-28"
        and a.get("time") == "11:00 AM"
        and a.get("medium") == "In Person"
    ]
    if not matching:
        errors.append(
            "No Personal Statement Review appointment found for March 28, 2026 "
            "at 11:00 AM in person."
        )
    else:
        appt = matching[0]
        if appt.get("staffId") != "staff_03" and appt.get("staffName") != "Maria Rodriguez":
            errors.append(
                f"Appointment should be with Maria Rodriguez. "
                f"Got staffName='{appt.get('staffName')}'."
            )

    # Check 2: Q&A question about grad school timelines
    questions = state.get("qaQuestions", [])
    grad_questions = [
        q for q in questions
        if q.get("authorName") == "Maya Chen"
        and ("grad school" in q.get("question", "").lower()
             or "graduate school" in q.get("question", "").lower())
        and ("timeline" in q.get("question", "").lower()
             or "application" in q.get("question", "").lower()
             or "when" in q.get("question", "").lower())
    ]
    if not grad_questions:
        errors.append(
            "No Q&A question from Maya Chen about grad school application timelines found."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Personal Statement Review scheduled with Maria Rodriguez for March 28 at "
        "11:00 AM in person. Q&A question about grad school timelines posted."
    )
