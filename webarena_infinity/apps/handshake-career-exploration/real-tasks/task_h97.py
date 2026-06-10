"""
Task: Find single most helpful answer across all Q&A. Mark it helpful.
Then find most-viewed question and submit own answer.

Discovery: Most helpful individual answer: ans_07 on qa_05 (89 helpful).
Most viewed question: qa_05 (1567 views). Both happen to be on the same question.

Verify:
(1) ans_07 on qa_05 has helpful > 89
(2) qa_05 has new answer from Maya Chen (authorName contains "Maya")
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    qa_questions = state.get("qaQuestions", [])

    # Find qa_05
    qa_05 = None
    for q in qa_questions:
        if q.get("id") == "qa_05":
            qa_05 = q
            break

    if qa_05 is None:
        errors.append("qa_05 not found in qaQuestions")
    else:
        # Check 1: ans_07 on qa_05 has helpful > 89
        answers = qa_05.get("answers", [])
        ans_07 = None
        for ans in answers:
            if ans.get("id") == "ans_07":
                ans_07 = ans
                break
        if ans_07 is None:
            errors.append("ans_07 not found in qa_05.answers")
        else:
            helpful = ans_07.get("helpful", 0)
            if helpful <= 89:
                errors.append(f"ans_07.helpful is {helpful}, expected > 89")

        # Check 2: qa_05 has new answer from Maya Chen
        found_maya_answer = False
        for ans in answers:
            author = ans.get("authorName", "")
            if "Maya" in author:
                found_maya_answer = True
                break
        if not found_maya_answer:
            errors.append("No new answer from Maya Chen found on qa_05")

    if errors:
        return False, " | ".join(errors)

    return True, "All checks passed: ans_07 helpful count incremented, Maya Chen's answer added to qa_05."
