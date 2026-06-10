"""
Task: Create a new Q&A question asking about housing options near tech
companies in San Francisco. Then find the only unanswered Q&A question
and submit your own answer to it.

Discovery: Unanswered question → qa_10 (finance recruiting timelines, 0 answers).

Verify:
(1) New Q&A question with 'housing' and 'San Francisco' in text
(2) qa_10 has a new answer
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    questions = state.get("qaQuestions", [])
    user = state.get("currentUser", {})

    # Check 1: new question about housing + SF
    seed_q_ids = {
        "qa_01", "qa_02", "qa_03", "qa_04", "qa_05", "qa_06",
        "qa_07", "qa_08", "qa_09", "qa_10", "qa_11", "qa_12",
    }
    new_questions = [q for q in questions if q.get("id") not in seed_q_ids]
    found_housing_q = any(
        "housing" in q.get("question", "").lower()
        and "san francisco" in q.get("question", "").lower()
        for q in new_questions
    )
    if not found_housing_q:
        errors.append(
            "No new Q&A question found mentioning 'housing' and 'San Francisco'."
        )

    # Check 2: qa_10 has a new answer
    qa_10 = next((q for q in questions if q.get("id") == "qa_10"), None)
    if qa_10 is None:
        errors.append("qa_10 not found.")
    else:
        answers = qa_10.get("answers", [])
        if len(answers) < 1:
            errors.append("qa_10 still has no answers.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "New Q&A question about SF housing created. "
        "qa_10 (unanswered finance timelines) now has an answer."
    )
