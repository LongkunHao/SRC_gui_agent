"""
Task: NSBE student also answered diversity Q&A. Submit own answer to that question,
bookmark student's post.

Discovery: Aisha Mohammed posted about NSBE (post_06). She answered qa_11
(diversity programs, ans_13).

Verify:
(1) qa_11 has new answer from Maya Chen (authorName contains "Maya")
(2) post_06.bookmarked == True
(3) "post_06" in savedPostIds
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []

    # Check 1: qa_11 has a new answer from Maya Chen
    questions = state.get("qaQuestions", [])
    qa_11 = next((q for q in questions if q.get("id") == "qa_11"), None)

    if qa_11 is None:
        errors.append("Q&A question qa_11 not found in state.")
    else:
        answers = qa_11.get("answers", [])
        # Look for a new answer from Maya Chen (skip seed answer ans_13)
        maya_answer = None
        for answer in answers:
            if answer.get("id") == "ans_13":
                continue  # skip the existing seed answer from Aisha
            author = answer.get("authorName", "")
            if "Maya" in author:
                maya_answer = answer
                break

        if maya_answer is None:
            errors.append(
                f"No new answer from Maya Chen found on qa_11. "
                f"Current answers: {[{'id': a.get('id'), 'authorName': a.get('authorName')} for a in answers]}"
            )

    # Check 2: post_06 bookmarked
    feed_posts = state.get("feedPosts", [])
    post_06 = next((p for p in feed_posts if p.get("id") == "post_06"), None)

    if post_06 is None:
        errors.append("Post post_06 (Aisha Mohammed - NSBE) not found in feedPosts.")
    elif post_06.get("bookmarked") is not True:
        errors.append(
            f"post_06 (Aisha Mohammed - NSBE) is not bookmarked. "
            f"bookmarked={post_06.get('bookmarked')}"
        )

    # Check 3: post_06 in savedPostIds
    saved_post_ids = state.get("currentUser", {}).get("savedPostIds", [])
    if "post_06" not in saved_post_ids:
        errors.append(
            f"post_06 not in savedPostIds. Current savedPostIds: {saved_post_ids}"
        )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "New answer from Maya Chen submitted on qa_11 (diversity programs). "
        "Post post_06 (Aisha Mohammed - NSBE) is bookmarked and in savedPostIds."
    )
