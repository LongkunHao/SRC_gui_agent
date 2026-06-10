"""
Task: Find the Q&A question about Google's interview process. Mark the non-anonymous
answer as helpful, then bookmark Google's post in the feed.

qa_01 about Google SWE interview. Non-anonymous answer: ans_01 (Tyler Wong,
seed helpful=67).

Verify:
- ans_01.helpful > 67
- post_01.bookmarked == True
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: ans_01 on qa_01 marked as helpful
    questions = state.get("qaQuestions", [])
    qa_01 = next((q for q in questions if q.get("id") == "qa_01"), None)
    if qa_01 is None:
        errors.append("Q&A question qa_01 not found in state.")
    else:
        answers = qa_01.get("answers", [])
        ans_01 = next((a for a in answers if a.get("id") == "ans_01"), None)
        if ans_01 is None:
            errors.append(
                f"Answer ans_01 not found in qa_01. "
                f"Current answers: {[a.get('id') for a in answers]}"
            )
        else:
            helpful = ans_01.get("helpful", 0)
            if helpful <= 67:
                errors.append(
                    f"ans_01 (Tyler Wong on qa_01) has helpful={helpful}, "
                    f"expected > 67 (seed value is 67). "
                    f"The answer was not marked as helpful."
                )

    # Check 2: post_01 (Google) is bookmarked
    feed_posts = state.get("feedPosts", [])
    post_01 = next((p for p in feed_posts if p.get("id") == "post_01"), None)
    if post_01 is None:
        errors.append("Post post_01 (Google) not found in feedPosts.")
    elif post_01.get("bookmarked") != True:
        errors.append(
            f"Post post_01 (Google) is not bookmarked. "
            f"bookmarked={post_01.get('bookmarked')}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "ans_01 (Tyler Wong on qa_01) marked as helpful and "
        "post_01 (Google) is bookmarked."
    )
