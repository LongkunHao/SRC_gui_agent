"""
Task: The student who asked about consulting internships before tech also
shared a FAANG study plan in the feed. Like their feed post and submit an
answer to their consulting question sharing your perspective.

Discovery: qa_03 by Kevin O'Brien (MIT). post_08 by Kevin O'Brien (FAANG study plan).

Verify:
(1) post_08 likes > 534 (seed)
(2) qa_03 has new answer from Maya Chen
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    posts = state.get("feedPosts", [])
    post_08 = next((p for p in posts if p.get("id") == "post_08"), None)
    if post_08 is None:
        errors.append("post_08 not found.")
    elif post_08.get("likes", 0) <= 534:
        errors.append(
            f"post_08 likes not incremented. Expected > 534, got {post_08.get('likes')}"
        )

    questions = state.get("qaQuestions", [])
    qa_03 = next((q for q in questions if q.get("id") == "qa_03"), None)
    if qa_03 is None:
        errors.append("qa_03 not found.")
    else:
        maya_answer = any(
            "maya" in a.get("authorName", "").lower()
            for a in qa_03.get("answers", [])
        )
        if not maya_answer:
            errors.append("No answer from Maya Chen on qa_03.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Kevin O'Brien identified (qa_03 author = post_08 author). "
        "Post liked and consulting question answered."
    )
