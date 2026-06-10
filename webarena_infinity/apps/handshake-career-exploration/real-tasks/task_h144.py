"""
Task: Find every Q&A question that has exactly one answer and mark that
answer as helpful.

Discovery: Single-answer questions:
  qa_03 (ans_05, helpful=38), qa_04 (ans_06, helpful=29),
  qa_06 (ans_09, helpful=56), qa_07 (ans_10, helpful=44),
  qa_08 (ans_11, helpful=63), qa_09 (ans_12, helpful=35),
  qa_11 (ans_13, helpful=78), qa_12 (ans_14, helpful=45).

Verify: Each answer's helpful count > seed value.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    questions = state.get("qaQuestions", [])

    expected = [
        ("qa_03", "ans_05", 38),
        ("qa_04", "ans_06", 29),
        ("qa_06", "ans_09", 56),
        ("qa_07", "ans_10", 44),
        ("qa_08", "ans_11", 63),
        ("qa_09", "ans_12", 35),
        ("qa_11", "ans_13", 78),
        ("qa_12", "ans_14", 45),
    ]

    for q_id, ans_id, seed_helpful in expected:
        q = next((q for q in questions if q.get("id") == q_id), None)
        if q is None:
            errors.append(f"{q_id} not found.")
            continue
        ans = next(
            (a for a in q.get("answers", []) if a.get("id") == ans_id),
            None,
        )
        if ans is None:
            errors.append(f"{ans_id} not found in {q_id}.")
        elif ans.get("helpful", 0) <= seed_helpful:
            errors.append(
                f"{ans_id} helpful not incremented. "
                f"Expected > {seed_helpful}, got {ans.get('helpful')}"
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All 8 single-answer Q&A questions had their answer marked helpful."
    )
