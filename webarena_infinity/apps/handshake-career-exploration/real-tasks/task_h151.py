"""
Task: A student from UC Berkeley posted about a PM interview study group in
the feed and also answered a Q&A question about Meta's work-life balance.
Leave a comment on that student's feed post. Then mark that student's Q&A
answer as helpful.

Discovery: David Lee (UC Berkeley) → post_14 (PM study group),
ans_10 on qa_07 (Meta WLB, helpful=44).

Verify:
(1) post_14 has a new comment from current user
(2) ans_10 helpful > 44
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    posts = state.get("feedPosts", [])
    questions = state.get("qaQuestions", [])
    user_id = state.get("currentUser", {}).get("id", "")

    # Check 1: post_14 has new comment
    post_14 = next((p for p in posts if p.get("id") == "post_14"), None)
    if post_14 is None:
        errors.append("post_14 not found.")
    else:
        seed_comment_ids = {"cmt_13", "cmt_14", "cmt_15"}
        new_comments = [
            c for c in post_14.get("comments", [])
            if c.get("id") not in seed_comment_ids
        ]
        if not new_comments:
            errors.append("No new comment on post_14.")

    # Check 2: ans_10 helpful incremented
    qa_07 = next((q for q in questions if q.get("id") == "qa_07"), None)
    if qa_07 is None:
        errors.append("qa_07 not found.")
    else:
        ans_10 = next(
            (a for a in qa_07.get("answers", []) if a.get("id") == "ans_10"),
            None,
        )
        if ans_10 is None:
            errors.append("ans_10 not found in qa_07.")
        elif ans_10.get("helpful", 0) <= 44:
            errors.append(
                f"ans_10 helpful not incremented. "
                f"Expected > 44, got {ans_10.get('helpful')}"
            )

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Commented on David Lee's PM study group post. "
        "Marked his Meta WLB answer as helpful."
    )
