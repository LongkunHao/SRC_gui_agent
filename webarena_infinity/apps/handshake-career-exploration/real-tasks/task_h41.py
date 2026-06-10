"""
Task: The student whose feed post received the most likes also contributed an answer
in Q&A. Mark their answer as helpful.

Discovery: Kevin O'Brien has post_08 with 534 likes (highest among students).
He authored ans_09 on qa_06 (system design resources).

Verify: ans_09.helpful > 56 (seed value).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()

    # Find qa_06 and ans_09
    qa_questions = state.get("qaQuestions", [])
    qa_06 = next((q for q in qa_questions if q.get("id") == "qa_06"), None)
    if qa_06 is None:
        return False, "Question qa_06 (system design resources) not found."

    answers = qa_06.get("answers", [])
    ans_09 = next((a for a in answers if a.get("id") == "ans_09"), None)
    if ans_09 is None:
        return False, "Answer ans_09 (Kevin O'Brien) not found in qa_06."

    helpful = ans_09.get("helpful", 0)
    if helpful <= 56:
        return False, (
            f"ans_09 (Kevin O'Brien) helpful={helpful}, expected > 56 (seed=56). "
            f"Answer was not marked as helpful."
        )

    return True, (
        f"Kevin O'Brien's Q&A answer (ans_09) marked as helpful "
        f"(helpful={helpful}, seed was 56)."
    )
