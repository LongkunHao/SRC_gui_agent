import requests


def verify(server_url: str) -> tuple[bool, str]:
    resp = requests.get(f"{server_url}/api/state")
    if resp.status_code != 200:
        return False, "Could not retrieve application state."
    state = resp.json()

    errors = []

    # ---- Check 1: Answers marked as helpful ----
    questions = state.get("qaQuestions", [])

    # ans_13 on qa_11 (diversity programs) - seed helpful=78, expect > 78
    qa_11 = next((q for q in questions if q.get("id") == "qa_11"), None)
    if qa_11 is None:
        errors.append("Q&A question qa_11 not found in state.")
    else:
        ans_13 = next((a for a in qa_11.get("answers", []) if a.get("id") == "ans_13"), None)
        if ans_13 is None:
            errors.append("Answer ans_13 not found in qa_11.")
        else:
            helpful = ans_13.get("helpful", 0)
            if helpful <= 78:
                errors.append(f"ans_13 (diversity programs) helpful={helpful}, expected > 78.")

    # ans_07 and ans_08 on qa_05 (salary negotiation) - seed helpful=89 and 72
    qa_05 = next((q for q in questions if q.get("id") == "qa_05"), None)
    if qa_05 is None:
        errors.append("Q&A question qa_05 not found in state.")
    else:
        answers_05 = qa_05.get("answers", [])
        ans_07 = next((a for a in answers_05 if a.get("id") == "ans_07"), None)
        if ans_07 is None:
            errors.append("Answer ans_07 not found in qa_05.")
        else:
            helpful = ans_07.get("helpful", 0)
            if helpful <= 89:
                errors.append(f"ans_07 (salary negotiation) helpful={helpful}, expected > 89.")

        ans_08 = next((a for a in answers_05 if a.get("id") == "ans_08"), None)
        if ans_08 is None:
            errors.append("Answer ans_08 not found in qa_05.")
        else:
            helpful = ans_08.get("helpful", 0)
            if helpful <= 72:
                errors.append(f"ans_08 (salary negotiation) helpful={helpful}, expected > 72.")

    # ---- Check 2: Bookmark posts by Q&A answerers ----
    feed_posts = state.get("feedPosts", [])

    # Posts that must be bookmarked:
    # post_12 (Jordan Taylor) - not bookmarked in seed
    # post_06 (Aisha Mohammed) - not bookmarked in seed
    # post_10 (Emma Rodriguez) - not bookmarked in seed
    # post_14 (David Lee) - already bookmarked in seed, should remain
    # post_08 (Kevin O'Brien) - already bookmarked in seed, should remain
    required_bookmarks = {
        "post_12": "Jordan Taylor",
        "post_06": "Aisha Mohammed",
        "post_10": "Emma Rodriguez",
    }

    for post_id, author_name in required_bookmarks.items():
        post = next((p for p in feed_posts if p.get("id") == post_id), None)
        if post is None:
            errors.append(f"Post {post_id} ({author_name}) not found in feedPosts.")
        else:
            if post.get("bookmarked") != True:
                errors.append(
                    f"Post {post_id} ({author_name}) is not bookmarked. "
                    f"bookmarked={post.get('bookmarked')}"
                )

    if errors:
        return False, " | ".join(errors)

    return True, (
        "All answers marked as helpful (ans_07, ans_08, ans_13) and "
        "posts by Q&A answerers bookmarked (post_06, post_10, post_12)."
    )
