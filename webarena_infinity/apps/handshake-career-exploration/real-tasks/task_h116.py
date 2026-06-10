"""
Task: Submit an answer to the Q&A question about MBB GPA importance,
then schedule a career change guidance appointment for March 10, 2026
at 3:00 PM, in person.

Discovery: qa_08 about MBB GPA. Career Change Guidance under Career Counseling.
March 10 has 3:00 PM available.

Verify:
(1) qa_08 has new answer from Maya Chen
(2) New appointment: type="Career Change Guidance", date="2026-03-10",
    time="3:00 PM", medium="In Person"
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: New answer on qa_08
    questions = state.get("qaQuestions", [])
    qa_08 = next((q for q in questions if q.get("id") == "qa_08"), None)
    if qa_08 is None:
        errors.append("qa_08 not found.")
    else:
        maya_answer = any(
            "maya" in a.get("authorName", "").lower()
            for a in qa_08.get("answers", [])
        )
        if not maya_answer:
            errors.append("No answer from Maya Chen on qa_08.")

    # Check 2: Career Change Guidance appointment
    appointments = state.get("appointments", [])
    matching = [
        a for a in appointments
        if a.get("type") == "Career Change Guidance"
        and a.get("date") == "2026-03-10"
        and a.get("time") == "3:00 PM"
        and "in person" in a.get("medium", "").lower()
    ]
    if not matching:
        errors.append(
            "No Career Change Guidance appointment for March 10 at 3:00 PM in person."
        )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Answer submitted to qa_08. Career Change Guidance appointment "
        "scheduled for March 10 at 3:00 PM in person."
    )
