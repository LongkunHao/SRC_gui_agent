"""
Task: Find the student who posted career fair tips in the feed. Go to Q&A and mark their
answer as helpful, then leave a comment on their feed post thanking them for the advice.
Verify: (1) Nathan Brooks answered qa_12 as ans_14 (seed helpful=45). ans_14.helpful > 45.
(2) post_16 (Nathan Brooks - career fair tips) has a comment by Maya Chen.
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: ans_14 on qa_12 has helpful > 45
    questions = state.get("qaQuestions", [])
    qa_12 = next((q for q in questions if q.get("id") == "qa_12"), None)
    if qa_12 is None:
        errors.append("Q&A question qa_12 not found in state.")
    else:
        ans_14 = next(
            (a for a in qa_12.get("answers", []) if a.get("id") == "ans_14"), None
        )
        if ans_14 is None:
            errors.append("Answer ans_14 not found in qa_12.")
        else:
            helpful = ans_14.get("helpful", 0)
            if helpful <= 45:
                errors.append(
                    f"ans_14 (Nathan Brooks on qa_12) helpful={helpful}, expected > 45."
                )

    # Check 2: post_16 has a comment by Maya Chen
    feed_posts = state.get("feedPosts", [])
    post_16 = next((p for p in feed_posts if p.get("id") == "post_16"), None)
    if post_16 is None:
        errors.append("Post post_16 (Nathan Brooks - career fair tips) not found in feedPosts.")
    else:
        comments = post_16.get("comments", [])
        found_comment = False
        for comment in comments:
            author = comment.get("authorName", "")
            if "maya" in author.lower():
                found_comment = True
                break
        if not found_comment:
            errors.append(
                f"No comment from Maya Chen found on post_16 (career fair tips). "
                f"Current comments: {[{'authorName': c.get('authorName'), 'text': c.get('text', '')[:80]} for c in comments]}"
            )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "ans_14 (Nathan Brooks) marked as helpful on qa_12. "
        "Comment by Maya Chen found on post_16 (career fair tips)."
    )
