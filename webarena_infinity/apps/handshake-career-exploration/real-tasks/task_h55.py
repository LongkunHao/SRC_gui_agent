"""
Task: A student posted about their portfolio website and also answered a Q&A question
about virtual career fairs. Like their feed post and mark their Q&A answer as helpful.

Discovery: Emma Rodriguez posted post_10 (portfolio website, 89 likes).
She authored ans_06 on qa_04 (virtual career fair attire, 29 helpful).

Verify:
(1) post_10.likes > 89.
(2) ans_06.helpful > 29.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: post_10 liked
    feed_posts = state.get("feedPosts", [])
    post_10 = next((p for p in feed_posts if p.get("id") == "post_10"), None)
    if post_10 is None:
        errors.append("Post post_10 (Emma Rodriguez portfolio) not found.")
    else:
        likes = post_10.get("likes", 0)
        if likes <= 89:
            errors.append(
                f"post_10 (Emma Rodriguez) likes={likes}, expected > 89 (seed=89)."
            )

    # Check 2: ans_06 marked helpful
    qa_questions = state.get("qaQuestions", [])
    qa_04 = next((q for q in qa_questions if q.get("id") == "qa_04"), None)
    if qa_04 is None:
        errors.append("Question qa_04 (virtual career fair attire) not found.")
    else:
        ans_06 = next((a for a in qa_04.get("answers", []) if a.get("id") == "ans_06"), None)
        if ans_06 is None:
            errors.append("Answer ans_06 (Emma Rodriguez) not found in qa_04.")
        else:
            helpful = ans_06.get("helpful", 0)
            if helpful <= 29:
                errors.append(
                    f"ans_06 (Emma Rodriguez) helpful={helpful}, expected > 29 (seed=29)."
                )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "Emma Rodriguez's feed post (post_10) liked and "
        "Q&A answer (ans_06) marked as helpful."
    )
