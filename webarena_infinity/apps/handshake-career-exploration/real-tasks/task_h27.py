"""
Task: Schedule an application review appointment for March 13, 2026 at 10:00 AM
by phone, then post a question in Q&A asking about the best way to follow up
after submitting job applications.

Verify:
- Appointment: category="Job & Internship Search", type="Application Review",
  date="2026-03-13", time="10:00 AM", medium="Phone", status="requested"
- Q&A: new question by Maya Chen containing "follow up" or "follow-up" and
  "application" (case-insensitive)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: Application review appointment
    appointments = state.get("appointments", [])
    found_appt = False

    for appt in appointments:
        if (
            appt.get("category") == "Job & Internship Search"
            and appt.get("type") == "Application Review"
            and appt.get("date") == "2026-03-13"
            and appt.get("time") == "10:00 AM"
            and appt.get("medium") == "Phone"
            and appt.get("status") == "requested"
        ):
            found_appt = True
            break

    if not found_appt:
        appt_summaries = [
            {
                "id": a.get("id"),
                "category": a.get("category"),
                "type": a.get("type"),
                "date": a.get("date"),
                "time": a.get("time"),
                "medium": a.get("medium"),
                "status": a.get("status"),
            }
            for a in appointments
        ]
        errors.append(
            f"No appointment found matching: category='Job & Internship Search', "
            f"type='Application Review', date='2026-03-13', time='10:00 AM', "
            f"medium='Phone', status='requested'. "
            f"Current appointments: {appt_summaries}"
        )

    # Check 2: Q&A question about following up after applications
    qa_questions = state.get("qaQuestions", [])
    current_user = state.get("currentUser", {})
    user_name = current_user.get("fullName", "")
    user_id = current_user.get("id", "")

    found_question = False
    for q in qa_questions:
        author_name = q.get("authorName", "")
        author_id = q.get("authorId", "")

        is_by_user = (
            author_name == user_name
            or author_name == "Maya Chen"
            or author_id == user_id
            or author_id == "stu_8f3a2c81"
        )
        if not is_by_user:
            continue

        question_text = q.get("question", "").lower()
        has_follow_up = "follow up" in question_text or "follow-up" in question_text
        has_application = "application" in question_text

        if has_follow_up and has_application:
            found_question = True
            break

    if not found_question:
        user_questions = [
            {"id": q.get("id"), "question": q.get("question", "")[:80]}
            for q in qa_questions
            if q.get("authorName") == user_name
            or q.get("authorName") == "Maya Chen"
            or q.get("authorId") == user_id
            or q.get("authorId") == "stu_8f3a2c81"
        ]
        errors.append(
            f"No Q&A question by Maya Chen found containing 'follow up'/'follow-up' "
            f"and 'application'. User questions: {user_questions}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Application Review appointment scheduled for 2026-03-13 at 10:00 AM by Phone, "
        "and Q&A question about following up after applications posted."
    )
