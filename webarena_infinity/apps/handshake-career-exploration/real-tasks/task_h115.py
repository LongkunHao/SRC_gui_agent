"""
Task: In Q&A, mark as helpful every approved non-anonymous answer that
currently has fewer than 40 helpful votes.

Discovery: Approved, visibility='full', helpful < 40:
  ans_05 (Sarah Kim, helpful=38)
  ans_06 (Emma Rodriguez, helpful=29)
  ans_12 (Marcus Johnson, helpful=35)

Verify:
(1) ans_05 helpful > 38
(2) ans_06 helpful > 29
(3) ans_12 helpful > 35
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    questions = state.get("qaQuestions", [])

    checks = [
        ("qa_03", "ans_05", 38),
        ("qa_04", "ans_06", 29),
        ("qa_09", "ans_12", 35),
    ]

    for qid, aid, seed_helpful in checks:
        q = next((q for q in questions if q.get("id") == qid), None)
        if q is None:
            errors.append(f"{qid} not found.")
            continue
        ans = next((a for a in q.get("answers", []) if a.get("id") == aid), None)
        if ans is None:
            errors.append(f"{aid} not found in {qid}.")
        elif ans.get("helpful", 0) <= seed_helpful:
            errors.append(
                f"{aid} helpful not incremented. Expected > {seed_helpful}, "
                f"got {ans.get('helpful')}"
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "All approved non-anonymous answers with < 40 helpful marked: "
        "ans_05, ans_06, ans_12."
    )
