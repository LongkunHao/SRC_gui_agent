"""
Task: A student mentioned attending the NSBE conference in their feed post. Find
their answer in the Q&A section and mark it as helpful.

Aisha Mohammed (post_06) mentioned NSBE. She has ans_13 on qa_11 (seed helpful=78).

Verify: ans_13.helpful > 78
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    questions = state.get("qaQuestions", [])

    qa_11 = next((q for q in questions if q.get("id") == "qa_11"), None)
    if qa_11 is None:
        return False, "Q&A question qa_11 not found in state."

    answers = qa_11.get("answers", [])
    ans_13 = next((a for a in answers if a.get("id") == "ans_13"), None)
    if ans_13 is None:
        return False, (
            f"Answer ans_13 not found in qa_11. "
            f"Current answers: {[a.get('id') for a in answers]}"
        )

    helpful = ans_13.get("helpful", 0)
    if helpful <= 78:
        return False, (
            f"ans_13 (Aisha Mohammed on qa_11) has helpful={helpful}, expected > 78 "
            f"(seed value is 78). The answer was not marked as helpful."
        )

    return True, (
        f"ans_13 (Aisha Mohammed on qa_11) marked as helpful. "
        f"helpful={helpful} (seed was 78)."
    )
