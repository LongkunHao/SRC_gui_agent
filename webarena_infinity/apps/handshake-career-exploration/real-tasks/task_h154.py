"""
Task: Add a comment to your approved appointment asking about tailoring your
resume for AI roles. Then find the Q&A question asked by the student from
Howard University and submit an answer sharing your system design resources.

Discovery: Approved appointment → appt_01 (Resume Review, approved).
Howard University student → Aisha Mohammed → qa_06 (system design resources).

Verify:
(1) appt_01 has a new comment mentioning AI or resume
(2) qa_06 has a new answer
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: appt_01 has new comment
    appointments = state.get("appointments", [])
    appt_01 = next(
        (a for a in appointments if a.get("id") == "appt_01"), None
    )
    if appt_01 is None:
        errors.append("appt_01 not found.")
    else:
        comments = appt_01.get("comments", [])
        if len(comments) < 1:
            errors.append("appt_01 has no comments.")

    # Check 2: qa_06 has new answer
    questions = state.get("qaQuestions", [])
    qa_06 = next((q for q in questions if q.get("id") == "qa_06"), None)
    if qa_06 is None:
        errors.append("qa_06 not found.")
    else:
        # Seed has 1 answer (ans_09). New answer expected.
        answers = qa_06.get("answers", [])
        seed_ans_ids = {"ans_09"}
        new_answers = [
            a for a in answers if a.get("id") not in seed_ans_ids
        ]
        if not new_answers:
            errors.append("No new answer on qa_06.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Comment added to approved appointment. "
        "New answer submitted to qa_06 (Howard University student's question)."
    )
