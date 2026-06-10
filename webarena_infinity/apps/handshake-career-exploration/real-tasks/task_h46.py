"""
Task: A student started a PM interview study group in the feed and also answered a
Q&A question. Mark their Q&A answer as helpful and like their feed post.

Discovery: David Lee wrote post_14 (PM study group, 276 likes).
He authored ans_10 on qa_07 (Meta work-life balance, 44 helpful).

Verify:
(1) ans_10.helpful > 44 (seed).
(2) post_14.likes > 276 (seed).
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: ans_10 marked helpful
    qa_questions = state.get("qaQuestions", [])
    qa_07 = next((q for q in qa_questions if q.get("id") == "qa_07"), None)
    if qa_07 is None:
        errors.append("Question qa_07 (Meta work-life balance) not found.")
    else:
        ans_10 = next((a for a in qa_07.get("answers", []) if a.get("id") == "ans_10"), None)
        if ans_10 is None:
            errors.append("Answer ans_10 (David Lee) not found in qa_07.")
        else:
            helpful = ans_10.get("helpful", 0)
            if helpful <= 44:
                errors.append(
                    f"ans_10 (David Lee) helpful={helpful}, expected > 44 (seed=44)."
                )

    # Check 2: post_14 liked
    feed_posts = state.get("feedPosts", [])
    post_14 = next((p for p in feed_posts if p.get("id") == "post_14"), None)
    if post_14 is None:
        errors.append("Post post_14 (David Lee PM study group) not found.")
    else:
        likes = post_14.get("likes", 0)
        if likes <= 276:
            errors.append(
                f"post_14 (David Lee) likes={likes}, expected > 276 (seed=276)."
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "David Lee's Q&A answer (ans_10) marked helpful and "
        "his feed post (post_14) liked."
    )
