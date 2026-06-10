"""
Task: Most-liked student post author answered system design Q&A. Submit own answer
to that Q, like the post.

Discovery: Kevin O'Brien has most-liked student post (post_08, 534 likes). He
answered qa_06 (system design resources).

Verify:
(1) qa_06 has a new answer from Maya Chen (author name includes "Maya")
(2) post_08.likes > 534
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: qa_06 has a new answer from Maya Chen
    questions = state.get("qaQuestions", [])
    qa_06 = next((q for q in questions if q.get("id") == "qa_06"), None)
    if qa_06 is None:
        errors.append("Q&A question qa_06 (system design resources) not found.")
    else:
        answers = qa_06.get("answers", [])
        maya_answers = [
            a for a in answers
            if "maya" in a.get("authorName", "").lower()
        ]
        if not maya_answers:
            errors.append(
                f"No answer from Maya Chen on qa_06 (system design). "
                f"Current answer authors: {[a.get('authorName') for a in answers]}"
            )

    # Check 2: post_08 liked (likes > 534)
    posts = state.get("feedPosts", [])
    post_08 = next((p for p in posts if p.get("id") == "post_08"), None)
    if post_08 is None:
        errors.append("Post post_08 (Kevin O'Brien) not found.")
    elif post_08.get("likes", 0) <= 534:
        errors.append(
            f"post_08 (Kevin O'Brien) not liked. "
            f"likes={post_08.get('likes')}, expected > 534."
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Kevin O'Brien identified as most-liked student post author (post_08). "
        "His system design Q&A (qa_06) answered by Maya Chen and post liked."
    )
