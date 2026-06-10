"""
Task: Create a feed post for everyone on Handshake about tips for networking
at career fairs. Then find the Q&A question about what to wear to a virtual
career fair and mark its answer as helpful. Finally, leave a comment on the
feed post from the student who shared career fair tips.

Discovery:
  Virtual career fair attire Q&A → qa_04, answer ans_06 (helpful=29).
  Career fair tips post → post_16 (Nathan Brooks).

Verify:
(1) New post from user with audience 'everyone' about networking/career fair
(2) ans_06 helpful > 29
(3) post_16 has a new comment
"""

import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, f"Failed to fetch state: HTTP {resp.status_code}"

    state = resp.json()
    errors = []
    user = state.get("currentUser", {})
    posts = state.get("feedPosts", [])
    questions = state.get("qaQuestions", [])

    # Check 1: new post about networking + career fair
    user_id = user.get("id", "")
    found_post = any(
        p.get("authorId") == user_id
        and p.get("audience") == "everyone"
        and (
            "networking" in p.get("content", "").lower()
            or "career fair" in p.get("content", "").lower()
        )
        for p in posts
    )
    if not found_post:
        errors.append(
            "No new post from user with audience 'everyone' "
            "about networking or career fairs."
        )

    # Check 2: ans_06 helpful incremented
    qa_04 = next((q for q in questions if q.get("id") == "qa_04"), None)
    if qa_04 is None:
        errors.append("qa_04 not found.")
    else:
        ans_06 = next(
            (a for a in qa_04.get("answers", []) if a.get("id") == "ans_06"),
            None,
        )
        if ans_06 is None:
            errors.append("ans_06 not found in qa_04.")
        elif ans_06.get("helpful", 0) <= 29:
            errors.append(
                f"ans_06 helpful not incremented. "
                f"Expected > 29, got {ans_06.get('helpful')}"
            )

    # Check 3: post_16 has new comment
    post_16 = next((p for p in posts if p.get("id") == "post_16"), None)
    if post_16 is None:
        errors.append("post_16 not found.")
    else:
        comments = post_16.get("comments", [])
        if len(comments) < 1:
            errors.append("No comments on post_16.")

    if errors:
        return False, " | ".join(errors)
    return True, (
        "Career fair networking post created. "
        "Virtual career fair attire answer marked helpful. "
        "Nathan Brooks' career fair tips post commented on."
    )
