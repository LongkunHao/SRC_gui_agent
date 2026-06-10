"""
Task: Find the second-most-viewed question in Q&A. It has two answers —
mark the one with fewer helpful votes as helpful.

Discovery: Most viewed: qa_05 (1567). Second: qa_01 (1245).
qa_01 answers: ans_01 (helpful=67), ans_02 (helpful=43).
Fewer = ans_02.

Verify:
(1) ans_02 helpful > 43 (seed value)
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    questions = state.get("qaQuestions", [])

    qa_01 = next((q for q in questions if q.get("id") == "qa_01"), None)
    if qa_01 is None:
        return False, "qa_01 not found."

    ans_02 = next((a for a in qa_01.get("answers", []) if a.get("id") == "ans_02"), None)
    if ans_02 is None:
        return False, "ans_02 not found in qa_01."

    if ans_02.get("helpful", 0) <= 43:
        return False, (
            f"ans_02 helpful not incremented. "
            f"Expected > 43, got {ans_02.get('helpful')}"
        )

    return True, (
        "Second-most-viewed question (qa_01) found. "
        "Less-helpful answer (ans_02) marked helpful."
    )
